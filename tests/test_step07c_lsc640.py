from __future__ import annotations

import hashlib
import json
import math
import subprocess
import unittest

import numpy as np

from kernel_helpers import ROOT

from lsc_kernel.lsc640 import GalliumCaptureCrossSection, LSC640Evaluator
from lsc_kernel.lsc640.determination import RESULT_PATH, execute_once, verify_frozen_result
from lsc_kernel.lsc640.errors import (
    NoRefitViolation,
    PredictionInputError,
    UnsupportedDomainError,
    UnsupportedModelProfileError,
)
from lsc_kernel.lsc640.golden import load_golden_spec, materialize_case, verify_golden_vectors
from lsc_kernel.lsc640.prefit import run_prefit_audit
from lsc_kernel.lsc640.reference import NaturalSplineReference


def sha256(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authoritative_payload(isotope: str, alpha_0: float, experiment_id: str = "TEST") -> dict[str, object]:
    source = json.loads(
        (ROOT / "external_physics/gallium_capture/source_lines_prc108_035502.json").read_text(encoding="utf-8")
    )
    factors = {
        "source_activity_bq": 1.0,
        "exposure_seconds": 1.0,
        "conventional_probability": 1.0,
        "geometry_factor": 1.0,
        "detector_efficiency": 1.0,
    }
    return {
        "schema_version": "1.0.0",
        "model_version": "6.4.0",
        "model_profile": "A2/C/A",
        "input_classification": "AUTHORIZED_SOURCE_INPUT",
        "experiment_id": experiment_id,
        "observation_id": "SOFTWARE_TEST",
        "source_isotope": isotope,
        "alpha_0": alpha_0,
        "lines": [{**row, **factors} for row in source["isotopes"][isotope]],
        "analysis_context": {
            "role": "NON_PHYSICAL_TEST",
            "covariance_scenario_id": "NONE_PREDICTION_ONLY",
            "nuisance_policy_id": "NONE_PREDICTION_ONLY",
            "observed_outcomes_included": False,
            "BEST2_observed_data_accessed": False,
        },
    }


class CrossSectionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cross_section = GalliumCaptureCrossSection.from_repository(ROOT)

    def test_every_provenance_binding_matches(self) -> None:
        manifest = json.loads(
            (ROOT / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json").read_text(encoding="utf-8")
        )
        for row in manifest["original_files"] + manifest["production_payloads"]:
            self.assertEqual(sha256(ROOT / row["path"]), row["sha256"])

    def test_payload_shape_order_positivity_and_exact_knots(self) -> None:
        cs = self.cross_section
        self.assertEqual(cs.energies.shape, (58,))
        self.assertTrue(np.all(np.diff(cs.energies) > 0.0))
        self.assertTrue(np.all(cs.values > 0.0))
        for energy, expected in zip(cs.energies, cs.values, strict=True):
            self.assertAlmostEqual(cs.sigma(float(energy)), float(expected), places=9)

    def test_derivative_formula_and_log_finite_difference_agree(self) -> None:
        cs = self.cross_section
        for energy in (0.4264, 0.4323, 0.6, 0.7465, 0.7524, 0.8107, 0.8138):
            analytic = energy * cs.derivative(energy) / cs.sigma(energy)
            step = 1e-6
            finite = (
                math.log(cs.sigma(energy * math.exp(step)))
                - math.log(cs.sigma(energy * math.exp(-step)))
            ) / (2.0 * step)
            self.assertAlmostEqual(cs.response(energy), analytic, places=14)
            self.assertAlmostEqual(cs.response(energy), finite, places=8)

    def test_unsupported_domain_and_alpha_fail_closed(self) -> None:
        with self.assertRaises(UnsupportedDomainError):
            self.cross_section.sigma(0.239)
        with self.assertRaises(UnsupportedDomainError):
            self.cross_section.sigma(30.001)
        with self.assertRaises(UnsupportedDomainError):
            self.cross_section.validate_alpha(0.1)

    def test_source_lines_are_complete_and_normalized(self) -> None:
        cr = self.cross_section.authoritative_lines("Cr51")
        ar = self.cross_section.authoritative_lines("Ar37")
        self.assertEqual((len(cr), len(ar)), (6, 3))
        self.assertAlmostEqual(sum(float(row["branching_fraction"]) for row in cr), 1.0, places=15)
        self.assertAlmostEqual(sum(float(row["branching_fraction"]) for row in ar), 1.0, places=15)


class EvaluatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evaluator = LSC640Evaluator.from_repository(ROOT)

    def test_null_limit_is_exact_for_both_sources(self) -> None:
        for isotope in ("Cr51", "Ar37"):
            output = self.evaluator.predict(authoritative_payload(isotope, 0.0))
            self.assertEqual(output["R_pred"], 1.0)
            self.assertTrue(all(row["S_a"] == 0.0 for row in output["per_line"]))

    def test_positive_and_negative_alpha(self) -> None:
        positive = self.evaluator.predict(authoritative_payload("Cr51", 0.05))
        negative = self.evaluator.predict(authoritative_payload("Cr51", -0.05))
        self.assertGreater(positive["R_pred"], 1.0)
        self.assertLess(negative["R_pred"], 1.0)
        self.assertAlmostEqual(positive["R_pred"] + negative["R_pred"], 2.0, places=14)

    def test_universal_sharing_ignores_label_only(self) -> None:
        first = self.evaluator.predict(authoritative_payload("Cr51", 0.02, "LABEL_A"))
        second = self.evaluator.predict(authoritative_payload("Cr51", 0.02, "LABEL_B"))
        self.assertEqual(first["mean_F_m"], second["mean_F_m"])
        self.assertEqual(first["R_pred"], second["R_pred"])

    def test_tensor_axis_and_anisotropic_amplitude_are_rejected(self) -> None:
        for key, value in (
            ("tensor", [[1.0, 0.0, 0.0]] * 3),
            ("preferred_axis", [1.0, 0.0, 0.0]),
            ("anisotropic_amplitude", 0.1),
        ):
            payload = authoritative_payload("Cr51", 0.0)
            payload[key] = value
            with self.subTest(key=key):
                with self.assertRaises(UnsupportedModelProfileError):
                    self.evaluator.predict(payload)

    def test_authoritative_line_mutation_is_rejected(self) -> None:
        payload = authoritative_payload("Cr51", 0.0)
        payload["lines"][0]["energy_mev"] += 1e-6
        with self.assertRaises(PredictionInputError):
            self.evaluator.predict(payload)

    def test_evaluator_is_bitwise_deterministic(self) -> None:
        payload = authoritative_payload("Ar37", 0.05)
        self.assertEqual(self.evaluator.predict_json(payload), self.evaluator.predict_json(payload))

    def test_output_contains_required_hashes_and_provenance(self) -> None:
        output = self.evaluator.predict(authoritative_payload("Cr51", 0.0))
        for field in (
            "model_sha256",
            "response_specification_sha256",
            "cross_section_payload_sha256",
            "source_line_payload_sha256",
            "input_sha256",
        ):
            self.assertRegex(str(output[field]), r"^[0-9a-f]{64}$")
        self.assertEqual(output["anisotropic_sector"], "DISABLED")


class GoldenAndReferenceTests(unittest.TestCase):
    def test_all_fifteen_golden_vectors_pass(self) -> None:
        result = verify_golden_vectors(ROOT)
        self.assertEqual(result["vector_count"], 15)
        self.assertEqual(result["passed"], 15)
        self.assertEqual(result["failed"], 0)

    def test_production_and_independent_reference_agree_on_grid(self) -> None:
        cs = GalliumCaptureCrossSection.from_repository(ROOT)
        reference = NaturalSplineReference.from_csv(
            ROOT / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"
        )
        for energy in np.linspace(0.4264, 0.8138, 101):
            self.assertAlmostEqual(cs.sigma(float(energy)), reference.evaluate(float(energy)), places=11)
            self.assertAlmostEqual(cs.response(float(energy)), reference.response(float(energy)), places=10)

    def test_golden_inputs_are_deterministically_materialized(self) -> None:
        spec = load_golden_spec(ROOT)
        for case in spec["vectors"]:
            first = materialize_case(ROOT, spec, case)
            second = materialize_case(ROOT, spec, case)
            self.assertEqual(first, second)


class PreFitAndDeterminationTests(unittest.TestCase):
    def test_prefit_gate_passes_and_best2_is_untouched(self) -> None:
        receipt = run_prefit_audit(ROOT)
        self.assertEqual(receipt["status"], "PASS")
        self.assertFalse(receipt["BEST2_observed_data_accessed"])

    def test_protocol_has_one_parameter_one_run_and_frozen_holdout(self) -> None:
        protocol = json.loads((ROOT / "LSC_6_4_0_ALPHA0_DETERMINATION_PROTOCOL.json").read_text())
        self.assertEqual(protocol["allowed_execution_count"], 1)
        self.assertEqual(protocol["parameter"]["symbol"], "alpha_0")
        self.assertFalse(protocol["parameter"]["refit_between_experiments"])
        self.assertFalse(protocol["development_data"]["holdout_in_objective"])
        self.assertEqual(protocol["covariance"]["classification"], "ASSUMPTION_BASED_SENSITIVITY_ONLY")

    def test_frozen_result_reproduces_and_refit_is_rejected(self) -> None:
        result_file = ROOT / RESULT_PATH
        if not result_file.exists():
            self.skipTest("The single authorized determination has not been executed yet.")
        result = verify_frozen_result(ROOT)
        self.assertEqual(result["verdict"], "LSC_6_4_0_PARAMETER_DETERMINATION_FAILED")
        self.assertEqual(result["boundary_status"], "BOUNDARY_DOMINATED")
        self.assertFalse(result["parameter_bundle_frozen"])
        with self.assertRaises(NoRefitViolation):
            execute_once(ROOT)


class SafetyAndHistoricalIntegrityTests(unittest.TestCase):
    def test_exactly_one_lsc_physical_parameter_and_no_hidden_fit(self) -> None:
        contract = json.loads((ROOT / "LSC_6_4_0_IMPLEMENTATION_CONTRACT.json").read_text())
        self.assertEqual(contract["recommended_configuration"]["physical_free_parameter_count"], 1)
        production = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "src/lsc_kernel/lsc640/cross_section.py",
                "src/lsc_kernel/lsc640/contracts.py",
                "src/lsc_kernel/lsc640/evaluator.py",
            )
        )
        for forbidden in ("minimize(", "least_squares(", "curve_fit(", "mcmc", "random_search"):
            self.assertNotIn(forbidden, production.lower())

    def test_best2_remains_future_blind_without_prediction(self) -> None:
        response = json.loads((ROOT / "spec/LSC_6_4_0_RESPONSE_A2.json").read_text())
        self.assertEqual(response["BEST2"]["status"], "FUTURE_ONLY_FUTURE_BLIND")
        self.assertFalse(response["BEST2"]["observed_data_accessed"])
        self.assertFalse(response["BEST2"]["prediction_generated"])

    def test_historical_630_head_and_tree_are_unchanged(self) -> None:
        historical = ROOT / "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research"
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=historical, check=True, capture_output=True, text=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--short"], cwd=historical, check=True, capture_output=True, text=True
        ).stdout.strip()
        self.assertEqual(head, "6ffa07bdde533fcc2a550e36c762b8edd9236c47")
        self.assertEqual(status, "")


if __name__ == "__main__":
    unittest.main()
