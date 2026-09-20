from __future__ import annotations

import hashlib
import json
import math
import subprocess
import unittest

import numpy as np

from kernel_helpers import ROOT

from lsc_kernel.lsc650 import ExactGalliumCaptureCrossSection, LSC650Evaluator
from lsc_kernel.lsc650.cross_section import canonical_hash
from lsc_kernel.lsc650.determination import RESULT_PATH, execute_once, verify_frozen_result
from lsc_kernel.lsc650.errors import (
    NoRefitViolation,
    PredictionInputError,
    UnsupportedDomainError,
    UnsupportedModelProfileError,
)
from lsc_kernel.lsc650.golden import load_golden_spec, materialize_case, verify_golden_vectors
from lsc_kernel.lsc650.prefit import run_prefit_audit
from lsc_kernel.lsc650.reference import NaturalSplineReference650, reference_exact_prediction


def sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_payload(isotope: str, alpha: float, experiment: str = "TEST") -> dict[str, object]:
    lines_doc = json.loads((ROOT / "external_physics/gallium_capture/source_lines_prc108_035502.json").read_text())
    factors = {"source_activity_bq": 1.0, "exposure_seconds": 1.0, "conventional_probability": 1.0, "geometry_factor": 1.0, "detector_efficiency": 1.0}
    return {
        "schema_version": "1.0.0",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "response_variant": "EXACT_CAPTURE_ARGUMENT_DILATION",
        "cross_section_scenario_id": "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE",
        "source_line_payload_sha256": "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e",
        "input_classification": "AUTHORIZED_SOURCE_INPUT",
        "experiment_id": experiment,
        "observation_id": "SOFTWARE_TEST",
        "source_isotope": isotope,
        "alpha_0": alpha,
        "parameter_source": {"kind": "PREFIT_AUTHORIZED_DEVELOPMENT", "bundle_sha256": None},
        "lines": [{**row, **factors} for row in lines_doc["isotopes"][isotope]],
        "analysis_context": {"role": "NON_PHYSICAL_TEST", "covariance_scenario_id": "NONE_PREDICTION_ONLY", "nuisance_policy_id": "NONE_PREDICTION_ONLY", "observed_outcomes_included": False, "BEST2_observed_data_accessed": False},
    }


class ScientificFreezeTests(unittest.TestCase):
    def test_owner_authorization_and_version_boundary(self) -> None:
        text = (ROOT / "OWNER_AUTHORIZATION_LSC_6_5_0.md").read_text()
        self.assertIn("OWNER AUTHORIZATION: **APPROVED**", text)
        self.assertIn("A2-exact / C / A", text)
        contract = json.loads((ROOT / "LSC_6_5_0_IMPLEMENTATION_CONTRACT.json").read_text())
        self.assertTrue(contract["state"]["owner_authorized"])
        self.assertEqual(contract["lineage"]["6_3_1_status"], "ABANDONED_BEFORE_RELEASE")
        self.assertEqual(contract["lineage"]["6_4_0_status"], "DEVELOPMENT_PARAMETER_DETERMINATION_FAILED_IMMUTABLE")

    def test_scientific_freeze_exactly_one_parameter_and_tensor_off(self) -> None:
        freeze = json.loads((ROOT / "LSC_6_5_0_SCIENTIFIC_FREEZE.json").read_text())
        self.assertEqual(freeze["parameter_contract"]["physical_parameter_count"], 1)
        self.assertEqual(freeze["parameter_contract"]["symbol"], "alpha_0")
        self.assertEqual(freeze["model_profile"]["tensor"], "DISABLED")
        self.assertEqual(freeze["model_profile"]["preferred_axis"], "NONE")
        self.assertFalse(freeze["exact_response"]["production_uses_derivative"])
        self.assertFalse(freeze["fit_policy"]["step07c_boundary_solution_is_input"])

    def test_6_4_adverse_freeze_still_matches_every_artifact(self) -> None:
        freeze = json.loads((ROOT / "LSC_6_4_0_ADVERSE_RESULT_FREEZE.json").read_text())
        for row in freeze["artifacts"]:
            self.assertEqual(sha256(ROOT / row["path"]), row["sha256"], row["path"])


class ExactKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cs = ExactGalliumCaptureCrossSection.from_repository(ROOT)
        cls.evaluator = LSC650Evaluator(cls.cs)

    def test_payload_provenance_support_and_domain(self) -> None:
        self.assertEqual(self.cs.identity.payload_sha256, "55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5")
        self.assertEqual(self.cs.support, (0.24, 30.0))
        energies = [float(row["energy_mev"]) for rows in self.cs.source_lines["isotopes"].values() for row in rows]
        self.assertEqual(self.cs.alpha_domain(energies), (-0.5747389495096434, 3.607238025076703))

    def test_null_limit_is_exact(self) -> None:
        for isotope in ("Cr51", "Ar37"):
            output = self.evaluator.predict(source_payload(isotope, 0.0))
            self.assertEqual(output["R_pred"], 1.0)
            self.assertTrue(all(row["K_m"] == 1.0 and row["S_m"] == 0.0 for row in output["per_line"]))

    def test_first_order_limit_matches_6_4_generator(self) -> None:
        step = 1e-6
        for energy in (0.4264, 0.7465, 0.8138):
            finite = (self.cs.exact_ratio(energy, step)[0] - self.cs.exact_ratio(energy, -step)[0]) / (2.0 * step)
            self.assertAlmostEqual(finite, self.cs.linear_generator(energy), places=8)

    def test_scale_group_composition(self) -> None:
        for energy, a, b in ((0.4264, 0.1, 0.2), (0.7465, -0.1, 0.05), (0.8138, 0.3, -0.2)):
            direct = self.cs.exact_ratio(energy, a + b)[0]
            first, shifted, _ = self.cs.exact_ratio(energy, a)
            second = self.cs.exact_ratio(shifted, b)[0]
            self.assertAlmostEqual(direct, first * second, places=13)

    def test_baseline_accounting_counts_sigma_once(self) -> None:
        payload = source_payload("Cr51", -0.2)
        output = self.evaluator.predict(payload)
        direct = math.fsum(float(row["conventional_prefactor"]) * self.cs.sigma(float(row["transformed_cross_section_argument_mev"])) for row in output["per_line"])
        self.assertAlmostEqual(float(output["exact_numerator"]), direct, places=13)

    def test_universal_sharing_depends_on_physical_inputs_not_label(self) -> None:
        first = self.evaluator.predict(source_payload("Cr51", -0.1, "LABEL_A"))
        second = self.evaluator.predict(source_payload("Cr51", -0.1, "LABEL_B"))
        self.assertEqual(first["R_pred"], second["R_pred"])
        self.assertEqual(first["per_line"], second["per_line"])

    def test_profile_and_provenance_violations_fail_closed(self) -> None:
        for key, value in (("tensor", [[0.0] * 3] * 3), ("preferred_axis", [1.0, 0.0, 0.0]), ("anisotropic_amplitude", 0.1), ("beta_0", 0.2)):
            payload = source_payload("Cr51", 0.0)
            payload[key] = value
            with self.subTest(key=key), self.assertRaises(UnsupportedModelProfileError):
                self.evaluator.predict(payload)
        mutated = source_payload("Cr51", 0.0)
        mutated["lines"][0]["energy_mev"] += 1e-6
        with self.assertRaises(PredictionInputError):
            self.evaluator.predict(mutated)
        out_of_domain = source_payload("Cr51", -0.5747389495096434 - 1e-12)
        with self.assertRaises(UnsupportedDomainError):
            self.evaluator.predict(out_of_domain)

    def test_production_evaluator_is_bitwise_deterministic(self) -> None:
        payload = source_payload("Ar37", 0.2)
        self.assertEqual(self.evaluator.predict_json(payload), self.evaluator.predict_json(payload))


class IndependentReferenceAndGoldenTests(unittest.TestCase):
    def test_all_twenty_nine_golden_vectors_pass(self) -> None:
        receipt = verify_golden_vectors(ROOT)
        self.assertEqual((receipt["passed"], receipt["failed"], receipt["vector_count"]), (29, 0, 29))

    def test_production_and_independent_reference_agree(self) -> None:
        evaluator = LSC650Evaluator.from_repository(ROOT)
        reference = NaturalSplineReference650.from_csv(ROOT / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv")
        for isotope in ("Cr51", "Ar37"):
            for alpha in (-0.4, -0.1, 0.0, 0.2, 1.0):
                payload = source_payload(isotope, alpha)
                production = evaluator.predict(payload)
                independent = reference_exact_prediction(reference, payload["lines"], alpha)
                self.assertAlmostEqual(float(production["R_pred"]), float(independent["R_pred"]), places=11)

    def test_golden_materialization_is_deterministic(self) -> None:
        specification = load_golden_spec(ROOT)
        for case in specification["vectors"]:
            self.assertEqual(materialize_case(ROOT, specification, case), materialize_case(ROOT, specification, case))


class ProtocolAndSafetyTests(unittest.TestCase):
    def test_protocol_is_one_run_and_does_not_reuse_6_4_bound(self) -> None:
        protocol = json.loads((ROOT / "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json").read_text())
        self.assertEqual(protocol["allowed_execution_count"], 1)
        self.assertFalse(protocol["bounds"]["old_6_4_result_or_bound_used"])
        self.assertEqual(protocol["bounds"]["fit_bound"], [-0.5747389495096434, 3.607238025076703])
        self.assertFalse(protocol["development_data"]["holdout_in_objective"])
        self.assertEqual(protocol["covariance"]["classification"], "ASSUMPTION_BASED_SENSITIVITY_ONLY")
        self.assertFalse(protocol["optimizer"]["unconstrained_diagnostic_predeclared"])

    def test_prefit_gate_and_frozen_result_when_present(self) -> None:
        freeze_path = ROOT / "LSC_6_5_0_PREFIT_FREEZE.json"
        if not freeze_path.exists():
            self.skipTest("The pre-fit freeze has not yet been materialized.")
        receipt = run_prefit_audit(ROOT)
        self.assertEqual(receipt["status"], "PASS")
        self.assertFalse(receipt["old_6_4_result_used"])
        if (ROOT / RESULT_PATH).exists():
            result = verify_frozen_result(ROOT)
            self.assertEqual(result["fit_execution_count"], 1)
            self.assertFalse(result["unconstrained_diagnostic_performed"])
            with self.assertRaises(NoRefitViolation):
                execute_once(ROOT)

    def test_production_evaluator_has_no_optimizer_or_hidden_fit(self) -> None:
        production = "\n".join((ROOT / relative).read_text() for relative in (
            "src/lsc_kernel/lsc650/cross_section.py",
            "src/lsc_kernel/lsc650/contracts.py",
            "src/lsc_kernel/lsc650/evaluator.py",
        ))
        for forbidden in ("minimize_scalar", "least_squares", "curve_fit", "mcmc", "random_search"):
            self.assertNotIn(forbidden, production.lower())

    def test_best2_remains_untouched(self) -> None:
        manifest = json.loads((ROOT / "model_development/LSC_6_5_0_DEVELOPMENT_DATA_MANIFEST.json").read_text())
        self.assertFalse(manifest["BEST2_observed_data_accessed"])
        self.assertFalse(manifest["BEST2_observed_data_included"])
        self.assertFalse(manifest["BEST2_prediction_generated"])

    def test_historical_630_head_and_tree_remain_unchanged(self) -> None:
        historical = ROOT / "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research"
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=historical, check=True, capture_output=True, text=True).stdout.strip()
        status = subprocess.run(["git", "status", "--short"], cwd=historical, check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, "6ffa07bdde533fcc2a550e36c762b8edd9236c47")
        self.assertEqual(status, "")


class ParameterFreezeAndReleaseCandidateTests(unittest.TestCase):
    def test_frozen_parameter_bundle_matches_completed_result(self) -> None:
        bundle = json.loads((ROOT / "LSC_6_5_0_PARAMETER_BUNDLE.json").read_text())
        result = json.loads((ROOT / RESULT_PATH).read_text())
        self.assertTrue(result["success"])
        self.assertEqual(result["boundary_status"], "INTERIOR")
        self.assertEqual(result["identifiability"], "IDENTIFIABLE_ONE_DIMENSIONAL")
        self.assertEqual(bundle["parameter"]["value"], result["alpha_0_estimate"])
        self.assertEqual(bundle["parameter"]["uncertainty"]["interval"], result["certified_profile_delta_chi_square_1_interval"])
        self.assertTrue(bundle["no_refit"])
        self.assertEqual(bundle["development_exposure"], ["MODEL_EXPOSED", "POST_6_4_DEVELOPMENT", "RETROSPECTIVE_NON_BLIND", "DEVELOPMENT_DATA"])

    def test_canonical_model_hash_recomputes(self) -> None:
        identity = json.loads((ROOT / "LSC_6_5_0_MODEL_IDENTITY.json").read_text())
        expected = canonical_hash({"model_version": "6.5.0", "configuration": "EXACT_FINITE_A2/C/A", "components": identity["components"]})
        self.assertEqual(expected, identity["model_sha256"])
        self.assertEqual((ROOT / "LSC_6_5_0_MODEL_SHA256").read_text().strip(), expected)

    def test_incidents_are_preserved_without_scientific_change(self) -> None:
        incidents = [
            json.loads((ROOT / "LSC_6_5_0_PREFIT_EXECUTION_INCIDENT.json").read_text()),
            json.loads((ROOT / "LSC_6_5_0_PREFIT_EXECUTION_INCIDENT_R2.json").read_text()),
        ]
        self.assertTrue(all(item["result_file_created"] is False for item in incidents))
        self.assertTrue(all(item["scientific_outcome_available_to_decision_maker"] is False for item in incidents))
        self.assertTrue(all(item["scientific_or_methodological_change_authorized"] is False for item in incidents))

    def test_rc_manifest_and_sha256s_pass_without_cache(self) -> None:
        rc = ROOT / "release_candidate/LSC-6.5.0-rc1"
        self.assertTrue((rc / "MANIFEST.json").is_file())
        self.assertFalse(any(path.name == "__pycache__" or path.suffix == ".pyc" for path in rc.rglob("*")))
        for line in (rc / "SHA256SUMS.txt").read_text().splitlines():
            expected, relative = line.split("  ", 1)
            self.assertEqual(sha256(rc / relative), expected, relative)
        rc_manifest = json.loads((rc / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json").read_text())
        self.assertEqual(rc_manifest["original_files"], [])
        self.assertFalse(rc_manifest["release_candidate_source_policy"]["original_publications_redistributed"])

    def test_smoke_did_not_load_holdout_or_best2_outcome(self) -> None:
        smoke = json.loads((ROOT / "LSC_6_5_0_RETROSPECTIVE_SMOKE_REPORT.json").read_text())
        self.assertEqual(smoke["status"], "PASS_TECHNICAL_PIPELINE_ONLY")
        self.assertFalse(smoke["observed_outcome_loaded"])
        self.assertFalse(smoke["holdout_statistic_computed"])
        self.assertFalse(smoke["BEST2_observed_data_accessed"])


if __name__ == "__main__":
    unittest.main()
