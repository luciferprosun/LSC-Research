from __future__ import annotations

import csv
import json
import subprocess
import unittest

from kernel_helpers import ROOT

from lsc_kernel.decision.boundary import (
    HISTORICAL_COMMIT,
    HISTORICAL_VERSION_DOI,
    PublicationReadinessLevel,
    RecoverabilityVerdict,
    SuccessorContentClass,
    assert_blindness_label,
    assert_public_claim_allowed,
    assert_publication_ready,
    assert_successor_content_classification,
    assert_successor_identity,
    publication_boundary,
    recoverability_decision,
)
from lsc_kernel.errors import (
    BlindnessLabelRejected,
    HistoricalIdentityReassignmentRejected,
    PublicationBoundaryViolation,
    PublicClaimNotAuthorized,
    SuccessorClassificationError,
)
from lsc_kernel.io.hashes import sha256_file


class RecoverabilityDecisionTests(unittest.TestCase):
    def test_recoverability_levels_are_independent(self) -> None:
        decision = recoverability_decision()
        self.assertEqual(decision["identity_recoverability"], RecoverabilityVerdict.FULLY_RECOVERABLE)
        self.assertEqual(decision["symbolic_recoverability"], RecoverabilityVerdict.FULLY_RECOVERABLE)
        self.assertEqual(
            decision["numerical_recoverability"],
            RecoverabilityVerdict.NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE,
        )
        self.assertFalse(decision["questions"]["Q4_numerically_executable_without_new_decisions"])
        self.assertFalse(decision["scientific_state"]["MODEL_FALSIFIED"])

    def test_historical_commit_cannot_be_reassigned_to_successor(self) -> None:
        with self.assertRaises(HistoricalIdentityReassignmentRejected):
            assert_successor_identity(version="6.3.1", source_commit=HISTORICAL_COMMIT)

    def test_historical_doi_cannot_be_reassigned_to_successor(self) -> None:
        with self.assertRaises(HistoricalIdentityReassignmentRejected):
            assert_successor_identity(version="6.3.1", version_doi=HISTORICAL_VERSION_DOI)

    def test_distinct_unpublished_successor_identity_is_structurally_allowed(self) -> None:
        assert_successor_identity(version="6.3.1", source_commit=None, version_doi=None)


class ClaimAndVersionBoundaryTests(unittest.TestCase):
    def test_supported_historical_identity_claim_is_allowed(self) -> None:
        assert_public_claim_allowed("model_identity_recovered")

    def test_blocked_capability_cannot_become_public_claim(self) -> None:
        with self.assertRaises(PublicClaimNotAuthorized):
            assert_public_claim_allowed("numerical_predictions_reproducible")

    def test_new_numerical_value_cannot_be_authentic_6_3_0(self) -> None:
        with self.assertRaises(SuccessorClassificationError):
            assert_successor_content_classification(
                requested_class=SuccessorContentClass.UNCHANGED_FROM_6_3_0_AUTHENTIC,
                newly_specified=True,
            )

    def test_new_numerical_value_can_be_explicit_successor_content(self) -> None:
        assert_successor_content_classification(
            requested_class=SuccessorContentClass.NEW_NUMERICAL_SPECIFICATION_6_3_1,
            newly_specified=True,
        )


class ExposureAndPublicationGateTests(unittest.TestCase):
    def test_model_exposed_dataset_cannot_be_strict_blind(self) -> None:
        with self.assertRaises(BlindnessLabelRejected):
            assert_blindness_label(exposure_class="MODEL_EXPOSED", blindness_level="BLIND_STRICT")

    def test_historical_non_blind_label_is_allowed(self) -> None:
        assert_blindness_label(
            exposure_class="MODEL_EXPOSED", blindness_level="NON_BLIND_HISTORICAL"
        )

    def test_publication_not_ready_without_executable_bundle(self) -> None:
        with self.assertRaises(PublicationBoundaryViolation):
            assert_publication_ready({"complete_parameter_vector": False})

    def test_current_boundary_stops_at_p1(self) -> None:
        boundary = publication_boundary()
        readiness = boundary["publication_readiness"]
        self.assertEqual(
            readiness["maximum_current_level"],
            PublicationReadinessLevel.P1_SPECIFICATION_BOUNDARY_READY,
        )
        self.assertFalse(readiness["executable_successor_ready"])
        self.assertFalse(boundary["publication_authorized"])

    def test_best2_remains_future_blind(self) -> None:
        boundary = publication_boundary()
        best2 = next(row for row in boundary["future_blind_targets"] if row["dataset_id"] == "BEST2_FUTURE")
        self.assertEqual(best2["status"], "FUTURE_ONLY")
        self.assertEqual(best2["blindness"], "FUTURE_BLIND")
        self.assertFalse(boundary["BEST2_prediction_authorized"])


class Step06ArtifactAndIntegrityTests(unittest.TestCase):
    def test_required_step06_artifacts_exist(self) -> None:
        required = {
            "docs/decision/STEP_06_RECOVERABILITY_PUBLICATION_BOUNDARY_REPORT.md",
            "docs/decision/LSC_6_3_0_RECOVERABILITY_DECISION.md",
            "docs/decision/LSC_6_3_0_PRESERVATION_POLICY.md",
            "docs/decision/LSC_6_3_0_ALLOWED_CLAIMS.csv",
            "docs/decision/LSC_6_3_1_GENESIS_CONTRACT.md",
            "docs/decision/LSC_6_3_1_EXECUTABLE_RELEASE_REQUIREMENTS.md",
            "docs/decision/LEGACY_PARAMETER_USE_POLICY.md",
            "docs/decision/6_3_1_DECISION_MATRIX.md",
            "docs/decision/CHANGELOG_6_3_1_DRAFT.md",
            "publication_boundary.json",
            "STEP_07_INPUT_CONTRACT.json",
            "decision/step06_golden_status.json",
        }
        self.assertFalse([relative for relative in sorted(required) if not (ROOT / relative).is_file()])

    def test_claim_csv_matches_machine_boundary(self) -> None:
        with (ROOT / "docs/decision/LSC_6_3_0_ALLOWED_CLAIMS.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 12)
        self.assertEqual(
            {row["allowed_in_publication"] for row in rows}, {"True", "False"}
        )
        self.assertTrue(all(set(row) == {"claim", "status", "reason", "evidence", "allowed_in_publication"} for row in rows))

    def test_step07_contract_is_bound_to_publication_boundary(self) -> None:
        contract = json.loads((ROOT / "STEP_07_INPUT_CONTRACT.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["publication_boundary_sha256"], sha256_file(ROOT / "publication_boundary.json"))
        self.assertFalse(contract["prediction_authorized"])
        self.assertFalse(contract["numerical_validation_authorized"])
        self.assertFalse(contract["publication_authorized"])

    def test_kernel_status_has_step06_boundary(self) -> None:
        status = json.loads((ROOT / "frozen_core/manifests/kernel_status.json").read_text(encoding="utf-8"))
        self.assertTrue(status["recoverability_decision_frozen"])
        self.assertTrue(status["historical_6_3_0_preserved"])
        self.assertTrue(status["publication_boundary_defined"])
        self.assertTrue(status["successor_version_required"])
        self.assertEqual(status["successor_version_candidate"], "6.3.1")
        self.assertEqual(status["historical_validation_class"], "RETROSPECTIVE_NON_BLIND")
        self.assertFalse(status["executable_successor_ready"])
        self.assertFalse(status["publication_ready"])

    def test_historical_repository_head_and_key_sources_are_unchanged(self) -> None:
        historical = ROOT / "LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research"
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=historical, check=True, capture_output=True, text=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--short"], cwd=historical, check=True, capture_output=True, text=True
        ).stdout.strip()
        self.assertEqual(head, HISTORICAL_COMMIT)
        self.assertEqual(status, "")
        self.assertEqual(
            sha256_file(historical / "canonical/LSC_ACTIVE_EQUATION_SET.md"),
            "af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981",
        )
        self.assertEqual(
            sha256_file(historical / "canonical/LSC_FREEZE_BOUNDARY.md"),
            "b38ccc4f9f67e020b6c090e548e0bdcc2e8053097e22ac5ceb6447730e6a1f05",
        )


if __name__ == "__main__":
    unittest.main()
