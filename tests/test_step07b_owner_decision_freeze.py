from __future__ import annotations

import csv
import itertools
import json
import re
import subprocess
import unittest

from kernel_helpers import ROOT

from lsc_kernel.io.hashes import sha256_file


CONTRACT_PATH = ROOT / "LSC_6_4_0_IMPLEMENTATION_CONTRACT.json"
FREEZE_PATH = ROOT / "LSC_6_4_0_SCIENTIFIC_DECISION_FREEZE.json"
# STEP 07B.1 legitimately re-bound the decision freeze to the refined response
# package without changing its owner-pending semantics.
STEP07B_COMMIT = "34e89cb5895a8d011ac31ee84f34c201f7e309a9"
CANONICAL_DECISIONS_PATH = (
    ROOT / "docs/scientific/OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md"
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def historical_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{STEP07B_COMMIT}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def historical_json(path: str):
    return json.loads(historical_bytes(path).decode("utf-8"))


def canonical_option_titles() -> dict[str, dict[str, str]]:
    text = CANONICAL_DECISIONS_PATH.read_text(encoding="utf-8")
    result: dict[str, dict[str, str]] = {}
    matches = list(re.finditer(r"^## Decision ([123]): .+$", text, re.MULTILINE))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        options = dict(re.findall(r"^### ([ABC])\. (.+)$", block, re.MULTILINE))
        result[match.group(1)] = options
    return result


class CanonicalDecisionIntegrityTests(unittest.TestCase):
    def test_contract_contains_exactly_the_three_canonical_decisions(self) -> None:
        contract = load_json(CONTRACT_PATH)
        decisions = contract["canonical_decision_space"]
        self.assertEqual(
            set(decisions),
            {
                "decision_1_response_function",
                "decision_2_tensor_family",
                "decision_3_sharing_semantics",
            },
        )
        self.assertEqual(contract["authorization"]["owner_decisions_required"], 3)
        self.assertEqual(len(contract["new_physical_assumptions"]), 3)
        self.assertEqual(
            {row["decision_id"] for row in contract["new_physical_assumptions"]},
            set(decisions),
        )

    def test_option_titles_are_identical_to_canonical_source(self) -> None:
        contract = load_json(CONTRACT_PATH)
        source = canonical_option_titles()
        self.assertEqual(set(source), {"1", "2", "3"})
        key_by_number = {
            "1": "decision_1_response_function",
            "2": "decision_2_tensor_family",
            "3": "decision_3_sharing_semantics",
        }
        for number, key in key_by_number.items():
            actual = {
                row["id"]: row["title"]
                for row in contract["canonical_decision_space"][key]["options"]
            }
            self.assertEqual(actual, source[number])

    def test_owner_authorization_file_has_three_and_only_three_decisions(self) -> None:
        text = (ROOT / "OWNER_AUTHORIZATION_REQUIRED.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## Decision ([123])$", text, re.MULTILINE)
        self.assertEqual(headings, ["1", "2", "3"])
        self.assertEqual(text.count("**Owner authorization required:** **YES**"), 3)
        self.assertIn("owner authorization recorded: **NO**", text)
        self.assertIn("implementation authorized: **NO**", text)

    def test_no_hidden_fourth_physical_assumption(self) -> None:
        contract = load_json(CONTRACT_PATH)
        assumptions = contract["new_physical_assumptions"]
        self.assertEqual(len(assumptions), 3)
        self.assertTrue(
            all(
                row["classification"] == "NEW_PHYSICAL_ASSUMPTION_6_4_0"
                for row in assumptions
            )
        )
        self.assertEqual(
            {row["recommended_option"] for row in assumptions}, {"A", "C"}
        )


class VersionGaugeAndSharingTests(unittest.TestCase):
    def test_new_physical_assumption_cannot_be_labelled_631(self) -> None:
        contract = load_json(CONTRACT_PATH)
        self.assertEqual(contract["model"]["version"], "6.4.0")
        self.assertEqual(
            contract["version_disposition"]["planned_6_3_1_executable_release"],
            "ABANDONED_BEFORE_RELEASE",
        )
        serialized = json.dumps(contract["new_physical_assumptions"], sort_keys=True)
        self.assertNotIn("6_3_1", serialized)
        self.assertNotIn("6.3.1", serialized)

    def test_gauge_conventions_are_separate_from_physical_choices(self) -> None:
        contract = load_json(CONTRACT_PATH)
        gauge = contract["classification_ledger"]["gauge_conventions"]
        physical = contract["new_physical_assumptions"]
        self.assertTrue(all(row["classification"] == "GAUGE_CONVENTION" for row in gauge))
        self.assertTrue(
            all(
                row["classification"] == "NEW_PHYSICAL_ASSUMPTION_6_4_0"
                for row in physical
            )
        )
        self.assertFalse(
            {row["object"] for row in gauge}
            & {row["decision_id"] for row in physical}
        )

    def test_experiment_nuisance_cannot_become_experiment_specific_lsc_physics(self) -> None:
        sharing = load_json(CONTRACT_PATH)["recommended_configuration"]["sharing"]
        self.assertTrue(sharing["physical_response_universal"])
        self.assertFalse(sharing["physical_parameters_refittable_between_experiments"])
        self.assertEqual(
            sharing["experiment_specific_calibration_class"],
            "NUISANCE_NOT_LSC_PHYSICS",
        )
        self.assertFalse(sharing["nuisance_promotion_to_physical_parameter"])

    def test_recommended_physical_parameter_count_is_one(self) -> None:
        contract = load_json(CONTRACT_PATH)
        recommended = contract["recommended_configuration"]
        self.assertEqual(recommended["physical_free_parameter_count"], 1)
        rows = contract["physical_parameter_schema"]
        active_free = [row for row in rows if row["free_parameter"]]
        self.assertEqual([row["symbol"] for row in active_free], ["alpha_0"])
        self.assertFalse(active_free[0]["can_be_refit_between_experiments"])


class AxisCombinationAndBest2Tests(unittest.TestCase):
    def test_no_axis_or_best_fit_direction_was_selected(self) -> None:
        axis = load_json(CONTRACT_PATH)["recommended_configuration"]["axis"]
        self.assertEqual(axis["status"], "NO_JUSTIFIED_AXIS_AVAILABLE")
        self.assertIsNone(axis["active_model_axis"])
        self.assertFalse(axis["axis_required_by_recommendation"])
        self.assertFalse(axis["sky_scan_performed"])
        self.assertFalse(axis["residual_direction_scan_performed"])
        self.assertFalse(axis["best_fit_direction_selection_performed"])

    def test_all_twenty_seven_combinations_are_assessed_once(self) -> None:
        rows = load_json(CONTRACT_PATH)["combination_assessment"]
        expected = {
            f"R-{r}/T-{t}/S-{s}"
            for r, t, s in itertools.product("ABC", repeat=3)
        }
        self.assertEqual(len(rows), 27)
        self.assertEqual({row["id"] for row in rows}, expected)
        recommended = [row for row in rows if row["adjudication"] == "RECOMMENDED"]
        self.assertEqual(
            recommended,
            [
                {
                    "id": "R-A/T-C/S-A",
                    "parameter_count": "1",
                    "adjudication": "RECOMMENDED",
                }
            ],
        )

    def test_best2_remains_future_blind_without_prediction(self) -> None:
        policy = load_json(CONTRACT_PATH)["prospective_policy"]
        self.assertEqual(policy["BEST2_status"], "FUTURE_ONLY")
        self.assertEqual(policy["BEST2_blindness"], "FUTURE_BLIND")
        self.assertEqual(policy["BEST2_capability"], "PROSPECTIVE_SCHEMA_CAPABLE")
        self.assertFalse(policy["BEST2_prediction_generated"])
        self.assertFalse(policy["BEST2_observed_data_accessed"])

    def test_trace_only_branch_does_not_claim_full_m6(self) -> None:
        tensor = load_json(CONTRACT_PATH)["recommended_configuration"]["tensor"]
        self.assertEqual(tensor["option"], "C")
        self.assertFalse(tensor["anisotropic_sector_active"])
        self.assertEqual(tensor["tensor_free_parameters"], 0)
        self.assertFalse(tensor["directional_claims_authorized"])
        self.assertFalse(tensor["full_M6_successor"])


class FreezeAndAuthorizationTests(unittest.TestCase):
    def test_freeze_hashes_bind_every_declared_source_and_artifact(self) -> None:
        freeze = load_json(FREEZE_PATH)
        for row in freeze["canonical_sources"] + freeze["generated_artifacts"]:
            self.assertEqual(__import__("hashlib").sha256(historical_bytes(row["path"])).hexdigest(), row["sha256"])
        self.assertEqual(
            freeze["decision_matrix_sha256"],
            __import__("hashlib").sha256(historical_bytes("docs/scientific/LSC_6_4_0_OWNER_DECISION_MATRIX.md")).hexdigest(),
        )
        self.assertEqual(
            freeze["implementation_contract_sha256"],
            __import__("hashlib").sha256(historical_bytes("LSC_6_4_0_IMPLEMENTATION_CONTRACT.json")).hexdigest(),
        )

    def test_step07b_implementation_was_fail_closed_until_owner_authorization(self) -> None:
        contract = historical_json("LSC_6_4_0_IMPLEMENTATION_CONTRACT.json")
        self.assertFalse(contract["owner_authorized"])
        self.assertFalse(contract["ready_for_implementation"])
        self.assertEqual(contract["authorization"]["owner_decisions_recorded"], 0)
        self.assertFalse(contract["authorization"]["required_response_equation_payload_present"])
        self.assertFalse(any(
            contract["authorization"][key]
            for key in (
                "owner_authorized",
                "implementation_authorized",
                "parameter_determination_authorized",
                "model_execution_authorized",
                "historical_evaluation_authorized",
                "prospective_prediction_authorized",
                "publication_authorized",
            )
        ))

    def test_all_e1_e12_relationships_are_explicit(self) -> None:
        equations = load_json(CONTRACT_PATH)["equation_relationship"]["equations"]
        self.assertEqual(
            [row["id"] for row in equations],
            [f"E{index}" for index in range(1, 13)],
        )
        self.assertTrue(all(row["relationship"] for row in equations))


class HistoricalIntegrityTests(unittest.TestCase):
    def test_historical_630_head_and_tree_remain_unchanged(self) -> None:
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
        self.assertEqual(
            sha256_file(historical / "canonical/LSC_ACTIVE_EQUATION_SET.md"),
            "af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981",
        )


if __name__ == "__main__":
    unittest.main()
