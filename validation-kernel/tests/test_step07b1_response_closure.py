from __future__ import annotations

import json
import math
import subprocess
import unittest

from kernel_helpers import ROOT

from lsc_kernel.io.hashes import sha256_file


CANDIDATE_PATH = ROOT / "spec/LSC_6_4_0_RESPONSE_A_CANDIDATES.json"
CONTRACT_PATH = ROOT / "LSC_6_4_0_IMPLEMENTATION_CONTRACT.json"
ALPHA_CONTRACT_PATH = ROOT / "LSC_6_4_0_ALPHA0_DETERMINATION_CONTRACT.json"
AUTHORIZATION_PATH = ROOT / "OWNER_AUTHORIZATION_6_4_0.md"
RESPONSE_FREEZE_PATH = ROOT / "LSC_6_4_0_RESPONSE_CLOSURE_FREEZE.json"
STEP07B1_COMMIT = "34e89cb5895a8d011ac31ee84f34c201f7e309a9"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def historical_text(path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{STEP07B1_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def historical_or_preserved_bytes(path: str) -> bytes:
    historical = subprocess.run(
        ["git", "show", f"{STEP07B1_COMMIT}:{path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if historical.returncode == 0:
        return historical.stdout
    # Nested historical repositories are gitlinks in the outer repository;
    # their frozen working-tree object is verified directly.
    return (ROOT / path).read_bytes()


def candidate_by_id(candidate_id: str) -> dict[str, object]:
    candidates = load_json(CANDIDATE_PATH)["candidates"]
    return next(row for row in candidates if row["candidate_id"] == candidate_id)


def validate_equation_ast(node: object) -> None:
    """Parse only the small declarative response grammar; execute no model."""
    if not isinstance(node, dict):
        raise ValueError("AST node must be an object")
    if "symbol" in node:
        if node["symbol"] != "alpha_0":
            raise ValueError("Only alpha_0 is an active physical symbol")
        return
    operation = node.get("op")
    if operation == "constant":
        value = node.get("value")
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise ValueError("Constant must be finite")
        return
    if operation == "multiply":
        validate_equation_ast(node.get("left"))
        validate_equation_ast(node.get("right"))
        return
    if operation == "log_derivative":
        if node.get("function") not in {"sigma_m", "epsilon0_a"}:
            raise ValueError("Unapproved response function")
        if node.get("variable") != "E" or node.get("dilation_map") != "E * exp(xi)":
            raise ValueError("Noncanonical dilation definition")
        if node.get("evaluation_point") != {"xi": 0.0}:
            raise ValueError("Log derivative must be evaluated at xi=0")
        return
    raise ValueError(f"Unsupported AST operation: {operation!r}")


def logarithmic_derivative(*, energy: float, value: float, derivative: float) -> float:
    if not all(math.isfinite(item) for item in (energy, value, derivative)):
        raise ValueError("FAIL_CLOSED_UNSUPPORTED_DOMAIN")
    if energy <= 0 or value <= 0:
        raise ValueError("FAIL_CLOSED_UNSUPPORTED_DOMAIN")
    return energy * derivative / value


class ResponseEquationTests(unittest.TestCase):
    def test_candidate_equations_parse_in_closed_grammar(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        self.assertEqual(specification["closure_verdict"], "RESPONSE_A_NEW_PHYSICAL_HYPOTHESIS_OPTIONS_READY")
        self.assertFalse(specification["unique_backbone_derived_response_found"])
        self.assertEqual(len(specification["candidates"]), 3)
        for row in specification["candidates"]:
            validate_equation_ast(row["equation_ast"])

    def test_dimensions_are_complete_and_consistent(self) -> None:
        rules = load_json(CANDIDATE_PATH)["common_rules"]
        self.assertEqual(rules["S_a_units"], "dimensionless")
        self.assertEqual(rules["F_a_units"], "dimensionless")
        self.assertEqual(rules["alpha_0_units"], "dimensionless")

    def test_analytic_log_derivative_fixtures(self) -> None:
        # NON_PHYSICAL_TEST_FIXTURE: sigma(E)=E^2 and epsilon(E)=E^3.
        energy = 0.75
        sigma = energy**2
        dsigma = 2.0 * energy
        epsilon = energy**3
        depsilon = 3.0 * energy**2
        self.assertAlmostEqual(
            logarithmic_derivative(energy=energy, value=sigma, derivative=dsigma),
            2.0,
            places=14,
        )
        self.assertAlmostEqual(
            logarithmic_derivative(energy=energy, value=epsilon, derivative=depsilon),
            3.0,
            places=14,
        )

    def test_normalization_is_deterministic_and_not_outcome_based(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        a1 = candidate_by_id("RESPONSE_A1_UNIVERSAL_SCALE")
        self.assertEqual(a1["normalization"]["constant"], 1.0)
        for row in specification["candidates"][1:]:
            self.assertTrue(row["normalization"]["scale_gauge_removed"])
            self.assertFalse(row["normalization"]["arbitrary_template_rescaling_allowed"])
        self.assertEqual(specification["comparison"]["forbidden_criterion"], "goodness-of-fit to BEST, SAGE, GALLEX/GNO or BEST-2")

    def test_unsupported_domains_fail_closed(self) -> None:
        for kwargs in (
            {"energy": 0.0, "value": 1.0, "derivative": 1.0},
            {"energy": 1.0, "value": 0.0, "derivative": 1.0},
            {"energy": math.nan, "value": 1.0, "derivative": 1.0},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "FAIL_CLOSED_UNSUPPORTED_DOMAIN"):
                    logarithmic_derivative(**kwargs)
        self.assertEqual(
            load_json(CANDIDATE_PATH)["common_rules"]["unsupported_behavior"],
            "FAIL_CLOSED_UNSUPPORTED_DOMAIN",
        )


class ParameterSharingAndBranchTests(unittest.TestCase):
    def test_each_candidate_is_finite_one_parameter_model(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        self.assertEqual(
            {row["parameter_count"] for row in specification["candidates"]},
            {1},
        )
        self.assertEqual(specification["common_rules"]["one_empirical_physical_parameter"], "alpha_0")

    def test_no_observation_or_experiment_specific_physical_coefficient(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        active = specification["active_branch"]
        self.assertTrue(active["universal_cross_experiment_law"])
        self.assertEqual(active["experiment_specific_physical_coefficients"], [])
        self.assertFalse(specification["common_rules"]["physical_parameter_refit_between_experiments"])
        for row in specification["candidates"]:
            equation = row["equation"]
            self.assertNotIn("alpha_experiment", equation)
            self.assertNotIn("alpha_zone", equation)

    def test_tensor_is_disabled_without_hidden_axis(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        active = specification["active_branch"]
        self.assertEqual(active["tensor_option"], "C")
        self.assertFalse(active["anisotropic_sector_active"])
        contract = load_json(CONTRACT_PATH)
        tensor = contract["recommended_configuration"]["tensor"]
        axis = contract["recommended_configuration"]["axis"]
        self.assertEqual(tensor["canonical_tensor_response"], "B_a(E,t) = 0")
        self.assertIsNone(axis["active_model_axis"])
        self.assertFalse(axis["best_fit_direction_selection_performed"])

    def test_alpha_contract_remains_pre_fit_and_unfitted(self) -> None:
        contract = load_json(ALPHA_CONTRACT_PATH)
        self.assertEqual(contract["parameter"]["symbol"], "alpha_0")
        self.assertIsNone(contract["parameter"]["value"])
        self.assertIsNone(contract["parameter"]["preregistered_lower_bound"])
        self.assertIsNone(contract["parameter"]["preregistered_upper_bound"])
        self.assertFalse(contract["authorization"]["fit_authorized"])
        self.assertFalse(contract["safety_receipt"]["fit_performed_in_step07b1"])


class AuthorizationAndSafetyTests(unittest.TestCase):
    def test_step07b1_owner_document_had_exactly_three_pending_decisions(self) -> None:
        text = historical_text("OWNER_AUTHORIZATION_6_4_0.md")
        self.assertEqual(text.count("## Decision "), 3)
        self.assertIn("OWNER AUTHORIZATION: PENDING", text)
        self.assertNotIn("OWNER AUTHORIZATION: APPROVED", text)

    def test_step07b1_implementation_contract_was_closed(self) -> None:
        contract = json.loads(historical_text("LSC_6_4_0_IMPLEMENTATION_CONTRACT.json"))
        self.assertFalse(contract["owner_authorized"])
        self.assertFalse(contract["ready_for_implementation"])
        self.assertFalse(contract["authorization"]["implementation_authorized"])
        self.assertFalse(contract["authorization"]["parameter_determination_authorized"])
        self.assertFalse(contract["authorization"]["model_execution_authorized"])

    def test_no_fit_prediction_or_best2_access(self) -> None:
        specification = load_json(CANDIDATE_PATH)
        safety = specification["safety"]
        self.assertFalse(safety["fit_performed"])
        self.assertFalse(safety["prediction_performed"])
        self.assertFalse(safety["validation_performed"])
        self.assertFalse(safety["BEST2_observed_data_accessed"])
        self.assertFalse(safety["BEST2_prediction_generated"])

    def test_contract_hash_bindings_match(self) -> None:
        contract = json.loads(historical_text("LSC_6_4_0_IMPLEMENTATION_CONTRACT.json"))
        bindings = contract["response_closure"]["source_bindings"]
        for row in bindings:
            content = subprocess.run(
                ["git", "show", f"{STEP07B1_COMMIT}:{row['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(__import__("hashlib").sha256(content).hexdigest(), row["sha256"])

    def test_response_closure_freeze_binds_sources_and_artifacts(self) -> None:
        freeze = load_json(RESPONSE_FREEZE_PATH)
        self.assertEqual(freeze["closure_verdict"], "RESPONSE_A_NEW_PHYSICAL_HYPOTHESIS_OPTIONS_READY")
        self.assertFalse(freeze["owner_authorized"])
        self.assertFalse(freeze["ready_for_implementation"])
        for row in freeze["source_evidence"] + freeze["generated_artifacts"]:
            content = historical_or_preserved_bytes(row["path"])
            self.assertEqual(__import__("hashlib").sha256(content).hexdigest(), row["sha256"])

    def test_historical_630_remains_unchanged(self) -> None:
        historical = ROOT / "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research"
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=historical,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--short"],
            cwd=historical,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(head, "6ffa07bdde533fcc2a550e36c762b8edd9236c47")
        self.assertEqual(status, "")


if __name__ == "__main__":
    unittest.main()
