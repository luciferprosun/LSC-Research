from __future__ import annotations

import csv
import json
import math
import unittest

import numpy as np

from kernel_helpers import ROOT


SPEC_PATH = ROOT / "spec/LSC_6_4_0_SCIENTIFIC_SPECIFICATION_DRAFT.yaml"


def load_spec() -> dict[str, object]:
    # JSON is a strict YAML 1.2 subset. Keeping the draft in this subset avoids
    # adding a parser dependency before a model is authorized.
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def weighted_average(values: np.ndarray, weights: np.ndarray) -> float:
    denominator = float(np.sum(weights, dtype=np.float64))
    if not math.isfinite(denominator) or denominator <= 0.0:
        raise ValueError("NON_PHYSICAL_SYMBOLIC_FIXTURE requires a positive finite N0")
    return float(np.sum(values * weights, dtype=np.float64) / denominator)


class GaugeEquivalenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.n = np.array([0.36, -0.48, 0.8], dtype=np.float64)
        self.a = np.array(
            [[0.6, 0.2, -0.1], [0.2, -0.4, 0.3], [-0.1, 0.3, -0.2]],
            dtype=np.float64,
        )

    def test_scalar_scale_and_sign_gauge(self) -> None:
        lambda0 = -0.37
        f0 = np.array([0.2, -0.5, 1.4], dtype=np.float64)
        for c0 in (2.3, -1.7):
            original = lambda0 * f0
            transformed = (c0 * lambda0) * (f0 / c0)
            np.testing.assert_allclose(original, transformed, rtol=1e-15, atol=1e-15)

    def test_anisotropic_scale_and_sign_gauge(self) -> None:
        lambda_a = 0.41
        f_a = -0.7
        q = float(self.n @ self.a @ self.n)
        original = lambda_a * f_a * q
        for c1, c2 in ((2.0, 3.0), (-2.0, 0.5), (0.25, -4.0)):
            transformed = (c1 * lambda_a) * (c2 * f_a) * float(
                self.n @ (self.a / (c1 * c2)) @ self.n
            )
            self.assertAlmostEqual(original, transformed, places=14)

    def test_orthogonal_frame_covariance(self) -> None:
        angle = 0.73
        q_matrix = np.array(
            [
                [math.cos(angle), -math.sin(angle), 0.0],
                [math.sin(angle), math.cos(angle), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        original = float(self.n @ self.a @ self.n)
        rotated_n = q_matrix @ self.n
        rotated_a = q_matrix @ self.a @ q_matrix.T
        transformed = float(rotated_n @ rotated_a @ rotated_n)
        self.assertAlmostEqual(original, transformed, places=14)

    def test_tensor_constraints_and_frobenius_gauge(self) -> None:
        self.assertTrue(np.allclose(self.a, self.a.T))
        self.assertAlmostEqual(float(np.trace(self.a)), 0.0, places=15)
        norm = float(np.linalg.norm(self.a, ord="fro"))
        normalized = self.a / norm
        self.assertAlmostEqual(float(np.linalg.norm(normalized, ord="fro")), 1.0, places=15)
        self.assertAlmostEqual(float(np.trace(normalized)), 0.0, places=15)

    def test_three_dimensional_stf_component_count(self) -> None:
        component_count = 3 * (3 + 1) // 2 - 1
        self.assertEqual(component_count, 5)
        self.assertEqual(component_count - 1, 4)  # Frobenius scale gauge removed.


class FunctionalAndIntegrationTests(unittest.TestCase):
    def test_normalized_weight_constant_and_weight_scale(self) -> None:
        weights = np.array([0.5, 1.5, 3.0], dtype=np.float64)
        ones = np.ones(3, dtype=np.float64)
        values = np.array([-0.2, 0.8, 1.3], dtype=np.float64)
        self.assertAlmostEqual(weighted_average(ones, weights), 1.0)
        self.assertAlmostEqual(
            weighted_average(values, weights), weighted_average(values, 7.0 * weights)
        )

    def test_zero_denominator_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            weighted_average(np.ones(2), np.zeros(2))

    def test_fixed_design_functional_null_space_is_not_transferable(self) -> None:
        mu = np.array([0.5, 0.5, 0.0], dtype=np.float64)
        nu = np.array([0.1, 0.2, 0.7], dtype=np.float64)
        h = np.array([1.0, -1.0, 0.0], dtype=np.float64)
        self.assertAlmostEqual(weighted_average(h, mu), 0.0)
        self.assertNotAlmostEqual(weighted_average(h, nu), 0.0)

    def test_q_weighted_anisotropic_null_space(self) -> None:
        weights = np.array([0.25, 0.75], dtype=np.float64)
        q = np.array([1.0, 2.0], dtype=np.float64)
        h = np.array([6.0, -1.0], dtype=np.float64)
        self.assertAlmostEqual(weighted_average(q * h, weights), 0.0)

    def test_exact_ratio_binding_from_linear_e2(self) -> None:
        weights = np.array([1.0, 2.0, 4.0], dtype=np.float64)
        scalar_response = np.array([0.1, -0.05, 0.2], dtype=np.float64)
        anisotropic_response = np.array([-0.02, 0.03, 0.01], dtype=np.float64)
        n0 = float(np.sum(weights))
        n_lsc = float(np.sum(weights * (1.0 + scalar_response + anisotropic_response)))
        exact_ratio = n_lsc / n0
        reduced_ratio = 1.0 + weighted_average(
            scalar_response, weights
        ) + weighted_average(anisotropic_response, weights)
        self.assertAlmostEqual(exact_ratio, reduced_ratio, places=15)

    def test_scalar_off_anisotropic_off_and_zero_limits(self) -> None:
        scalar = 0.17
        anisotropic = -0.04
        self.assertAlmostEqual(1.0 + 0.0 + 0.0, 1.0)
        self.assertAlmostEqual(1.0 + scalar + 0.0, 1.17)
        self.assertAlmostEqual(1.0 + 0.0 + anisotropic, 0.96)


class ObservableCoordinateTests(unittest.TestCase):
    def test_best_double_ratio_is_not_an_independent_third_coordinate(self) -> None:
        inner = 0.79
        outer = 0.77
        jacobian = np.array(
            [[1.0, 0.0], [0.0, 1.0], [-outer / inner**2, 1.0 / inner]],
            dtype=np.float64,
        )
        induced_covariance = jacobian @ np.eye(2, dtype=np.float64) @ jacobian.T
        self.assertEqual(np.linalg.matrix_rank(jacobian), 2)
        self.assertEqual(np.linalg.matrix_rank(induced_covariance), 2)
        self.assertAlmostEqual(outer / inner, 0.77 / 0.79)


class AdjudicationArtifactTests(unittest.TestCase):
    def test_draft_is_non_executable_640_and_preserves_equations(self) -> None:
        spec = load_spec()
        model = spec["model"]
        authorization = spec["authorization"]
        preservation = spec["preservation"]
        self.assertEqual(model["candidate_version"], "6.4.0")
        self.assertEqual(model["step07a_verdict"], "VERSION_ESCALATION_REQUIRED_6_4_0")
        self.assertEqual(model["status"], "OWNER_SCIENTIFIC_DECISION_REQUIRED")
        self.assertFalse(preservation["equations_changed_in_step07a"])
        self.assertFalse(any(authorization.values()))

    def test_tensor_draft_records_only_resolved_structure(self) -> None:
        tensor = load_spec()["tensor_contract"]
        self.assertEqual(tensor["dimension"], 3)
        self.assertEqual(tensor["independent_components_before_scale_gauge"], 5)
        self.assertEqual(tensor["independent_continuous_degrees_after_scale_gauge"], 4)
        self.assertEqual(tensor["sharing_rule"], "UNRESOLVED_PHYSICAL_CHOICE")
        self.assertEqual(tensor["physical_orientation"], "UNRESOLVED_PHYSICAL_CHOICE")

    def test_minimal_parameter_table_has_no_known_successor_value(self) -> None:
        path = ROOT / "docs/scientific/MINIMAL_PHYSICAL_PARAMETER_SET.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        active = [row for row in rows if row["active_in_minimal_set"] == "YES"]
        self.assertEqual(len(active), 4)
        self.assertTrue(all(row["numerical_value_currently_known"] == "NO" for row in active))
        self.assertTrue(all(row["version_implication"] == "6.4.0" for row in active))

    def test_decision_record_covers_all_step07_unresolved_objects(self) -> None:
        unresolved = json.loads(
            (ROOT / "STEP_07_INPUT_CONTRACT.json").read_text(encoding="utf-8")
        )["unresolved_objects"]
        record = (ROOT / "docs/scientific/SCIENTIFIC_SPECIFICATION_DECISION_RECORD.md").read_text(
            encoding="utf-8"
        )
        display_tokens = {
            "theta": "`theta`",
            "parameter_ordering": "parameter ordering",
            "lambda0": "`lambda0`",
            "lambdaA": "`lambdaA`",
            "f0_a": "`f0_a`",
            "fA_a": "`fA_a`",
            "active_tensor_components": "active tensor components",
            "tensor_orientation": "tensor orientation",
            "complete_reference_frame": "complete reference frame",
            "complete_units": "complete units",
            "eta": "`eta`",
            "covariance": "covariance",
            "numerical_configuration": "numerical configuration",
            "parameter_bounds": "parameter bounds",
            "numerical_defaults": "numerical defaults",
            "frozen_prediction_table": "frozen prediction table",
            "executable_evaluator_inputs": "executable evaluator inputs",
        }
        self.assertEqual(set(unresolved), set(display_tokens))
        self.assertFalse([name for name in unresolved if display_tokens[name] not in record])

    def test_owner_gate_contains_exactly_three_scientific_decisions(self) -> None:
        text = (ROOT / "docs/scientific/OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(sum(text.count(f"## Decision {index}:") for index in (1, 2, 3)), 3)
        for label in ("### A.", "### B.", "### C."):
            self.assertEqual(text.count(label), 3)


if __name__ == "__main__":
    unittest.main()
