from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import unittest

from kernel_helpers import ROOT

from lsc_kernel.lsc640 import GalliumCaptureCrossSection
from lsc_kernel.lsc640.errors import UnsupportedDomainError


STEP07C_COMMIT = "e53db798f1f3f448034a6e0af6399e8256189cd5"


def load_json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(relative: str) -> str:
    return sha256_bytes((ROOT / relative).read_bytes())


class AdverseResultPreservationTests(unittest.TestCase):
    def test_every_frozen_step07c_artifact_matches_file_and_git_blob(self) -> None:
        freeze = load_json("LSC_6_4_0_ADVERSE_RESULT_FREEZE.json")
        self.assertEqual(freeze["frozen_repository_commit"], STEP07C_COMMIT)
        for row in freeze["artifacts"]:
            relative = row["path"]
            expected = row["sha256"]
            self.assertEqual(sha256_file(relative), expected, relative)
            historical = subprocess.run(
                ["git", "show", f"{STEP07C_COMMIT}:{relative}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(sha256_bytes(historical), expected, relative)

    def test_adverse_values_and_nonpromotion_are_exact(self) -> None:
        result = load_json("LSC_6_4_0_ALPHA0_DETERMINATION_RESULT.json")
        freeze = load_json("LSC_6_4_0_ADVERSE_RESULT_FREEZE.json")
        frozen = freeze["frozen_outcome"]
        self.assertEqual(result["verdict"], "LSC_6_4_0_PARAMETER_DETERMINATION_FAILED")
        self.assertEqual(result["alpha_0_estimate_unconstrained_diagnostic"], frozen["unconstrained_optimum"])
        self.assertEqual(result["fit_bound"], frozen["frozen_linear_domain"])
        self.assertEqual(result["alpha_0_estimate_constrained"], frozen["constrained_result"])
        self.assertEqual(result["boundary_status"], "BOUNDARY_DOMINATED")
        self.assertFalse(result["parameter_bundle_frozen"])
        self.assertFalse(frozen["release_candidate_created"])
        self.assertFalse(frozen["refit_authorized"])

    def test_claim_matrix_does_not_promote_failure(self) -> None:
        with (ROOT / "docs/scientific/LSC_6_4_0_CLAIMS_MATRIX.csv").open(newline="", encoding="utf-8") as handle:
            rows = {row["claim"]: row for row in csv.DictReader(handle)}
        self.assertEqual(rows["The determination was boundary dominated"]["allowed_in_publication"], "YES")
        self.assertEqual(rows["LSC 6.4.0 was fit successfully"]["allowed_in_publication"], "NO")
        self.assertEqual(rows["The boundary value is the LSC 6.4.0 alpha_0 parameter"]["status"], "PROHIBITED")
        self.assertEqual(rows["LSC 6.4.0 was falsified"]["allowed_in_publication"], "NO")


class ExactDilationScientificTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cross_section = GalliumCaptureCrossSection.from_repository(ROOT)
        cls.spec = load_json("spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml")
        cls.lines = load_json("external_physics/gallium_capture/source_lines_prc108_035502.json")["isotopes"]
        cls.all_energies = [
            float(row["energy_mev"])
            for isotope_rows in cls.lines.values()
            for row in isotope_rows
        ]

    def test_null_limit_is_exact(self) -> None:
        for energy in self.all_energies:
            self.assertEqual(self.cross_section.finite_dilation_ratio(energy, 0.0), 1.0)

    def test_first_derivative_at_zero_is_linear_a2_generator(self) -> None:
        step = 1e-6
        for energy in self.all_energies:
            derivative = (
                self.cross_section.finite_dilation_ratio(energy, step)
                - self.cross_section.finite_dilation_ratio(energy, -step)
            ) / (2.0 * step)
            self.assertAlmostEqual(derivative, self.cross_section.response(energy), places=8)

    def test_scale_flow_composition(self) -> None:
        for energy, alpha, beta in (
            (0.4264, 0.10, 0.20),
            (0.7465, -0.10, 0.05),
            (0.8138, 0.30, -0.20),
        ):
            direct = self.cross_section.finite_dilation_ratio(energy, alpha + beta)
            composed = (
                self.cross_section.finite_dilation_ratio(energy, alpha)
                * self.cross_section.finite_dilation_ratio(energy * math.exp(alpha), beta)
            )
            self.assertAlmostEqual(direct, composed, places=14)

    def test_data_independent_support_domain_is_exact(self) -> None:
        low, high = self.cross_section.domain
        expected_lower = math.log(low / min(self.all_energies))
        expected_upper = math.log(high / max(self.all_energies))
        declared = self.spec["domain"]["canonical_Cr51_Ar37_alpha_domain_closed"]
        self.assertEqual(declared, [expected_lower, expected_upper])
        for energy in self.all_energies:
            self.assertGreaterEqual(energy * math.exp(expected_lower), low - 4.0 * math.ulp(low))
            self.assertLessEqual(energy * math.exp(expected_upper), high + 4.0 * math.ulp(high))
        with self.assertRaises(UnsupportedDomainError):
            self.cross_section.finite_dilation_ratio(min(self.all_energies), expected_lower - 1e-12)
        with self.assertRaises(UnsupportedDomainError):
            self.cross_section.finite_dilation_ratio(max(self.all_energies), expected_upper + 1e-12)

    def test_exact_response_is_positive_and_finite_inside_support(self) -> None:
        lower, upper = self.spec["domain"]["canonical_Cr51_Ar37_alpha_domain_closed"]
        predefined_property_cases = (lower + 1e-12, -0.25, 0.0, 0.25, 1.0, upper - 1e-12)
        for alpha in predefined_property_cases:
            for energy in self.all_energies:
                ratio = self.cross_section.finite_dilation_ratio(energy, alpha)
                self.assertTrue(math.isfinite(ratio))
                self.assertGreater(ratio, 0.0)

    def test_baseline_measure_counts_cross_section_once(self) -> None:
        energies = [0.4264, 0.7465, 0.8138]
        conventional_prefactors = [0.2, 0.5, 0.3]
        alpha = -0.2
        denominator = sum(
            factor * self.cross_section.sigma(energy)
            for factor, energy in zip(conventional_prefactors, energies, strict=True)
        )
        numerator_direct = sum(
            factor * self.cross_section.sigma(energy * math.exp(alpha))
            for factor, energy in zip(conventional_prefactors, energies, strict=True)
        )
        numerator_measure = sum(
            factor
            * self.cross_section.sigma(energy)
            * self.cross_section.finite_dilation_ratio(energy, alpha)
            for factor, energy in zip(conventional_prefactors, energies, strict=True)
        )
        self.assertAlmostEqual(numerator_direct, numerator_measure, places=13)
        self.assertAlmostEqual(numerator_direct / denominator, numerator_measure / denominator, places=14)

    def test_one_parameter_universal_tensor_off_profile(self) -> None:
        contract = self.spec["parameter_contract"]
        profile = self.spec["model_profile"]
        self.assertEqual(contract["physical_parameter_count"], 1)
        self.assertEqual([row["symbol"] for row in contract["parameters"]], ["alpha_0"])
        self.assertEqual(contract["additional_polynomial_coefficients"], [])
        self.assertEqual(contract["experiment_specific_physical_coefficients"], [])
        self.assertEqual(profile["sharing"], "UNIVERSAL_CROSS_EXPERIMENT")
        self.assertEqual(profile["anisotropic_sector"], "DISABLED")
        self.assertIsNone(profile["tensor"])
        self.assertIsNone(profile["preferred_axis"])

    def test_candidate_x_dilates_only_cross_section_argument(self) -> None:
        hypothesis = self.spec["physical_hypothesis"]
        self.assertEqual(hypothesis["dilated_object"], "capture-cross-section argument only")
        for key in (
            "source_line_energy_is_rewritten",
            "source_spectrum_is_dilated",
            "oscillation_probability_is_dilated",
            "detector_response_is_dilated",
            "geometry_is_dilated",
            "time_or_activity_is_dilated",
        ):
            self.assertFalse(hypothesis[key])


class SuccessorBoundaryTests(unittest.TestCase):
    def test_version_and_owner_gate(self) -> None:
        spec = load_json("spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml")
        self.assertEqual(spec["model"]["version"], "6.5.0")
        self.assertEqual(spec["model"]["predecessor_verdict"], "LSC_6_4_0_PARAMETER_DETERMINATION_FAILED")
        self.assertFalse(spec["authorization"]["owner_authorized"])
        self.assertFalse(spec["authorization"]["implementation_authorized"])
        self.assertFalse(spec["authorization"]["parameter_determination_authorized"])

    def test_future_protocol_is_draft_and_no_new_fit_exists(self) -> None:
        protocol = load_json("LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL_DRAFT.json")
        self.assertFalse(protocol["protocol_is_frozen_for_execution"])
        self.assertFalse(protocol["fit_authorized"])
        self.assertFalse(protocol["fit_executed_in_step07d"])
        self.assertFalse(protocol["safety_receipt"]["alpha_scan_performed_in_step07d"])
        self.assertFalse(protocol["safety_receipt"]["historical_holdout_evaluated_in_step07d"])
        self.assertFalse(protocol["safety_receipt"]["BEST2_observed_data_accessed"])
        historical_tree = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "c522e344f7c0e43352626a7e435099c1da174286"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertNotIn("LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json", historical_tree)
        self.assertFalse(any(path.startswith("src/lsc_kernel/lsc650/") for path in historical_tree))

    def test_draft_protocol_hash_bindings_match(self) -> None:
        protocol = load_json("LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL_DRAFT.json")
        for binding in protocol["scientific_bindings"].values():
            expected = binding.get("sha256", binding.get("current_sha256"))
            historical = subprocess.run(
                ["git", "show", f"c522e344f7c0e43352626a7e435099c1da174286:{binding['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(sha256_bytes(historical), expected)

    def test_exposure_and_best2_boundaries(self) -> None:
        spec = load_json("spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml")
        self.assertIn("POST_6_4_DEVELOPMENT", spec["exposure"]["BEST_inner"])
        self.assertIn("MODEL_EXPOSED", spec["exposure"]["BEST_outer_GALLEX_SAGE"])
        self.assertNotIn("STRICT_BLIND", spec["exposure"]["BEST_outer_GALLEX_SAGE"])
        self.assertEqual(spec["exposure"]["BEST2"], ["FUTURE_ONLY", "FUTURE_BLIND"])
        self.assertFalse(spec["authorization"]["BEST2_observed_data_accessed"])
        self.assertFalse(spec["authorization"]["BEST2_prediction_generated"])

    def test_historical_630_head_and_tree_remain_unchanged(self) -> None:
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
