from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

from kernel_helpers import ROOT

from lsc_kernel.acquisition.adjudication import (
    CandidateEvidence,
    EvidenceTier,
    ExposureClass,
    assess_frozen_bundle,
    validate_non_physical_structural_fixture,
)
from lsc_kernel.acquisition.evidence import verify_evidence_freeze
from lsc_kernel.acquisition.gates import (
    ExternalMappingEvidence,
    T12Prerequisites,
    assert_collaboration_covariance_authorized,
    assert_step05_prediction_authorized,
)
from lsc_kernel.acquisition.registry import blocker_registry
from lsc_kernel.io.publication_paths import scan_publication_paths
from lsc_kernel.errors import (
    CollaborationCovarianceUnavailable,
    ExternalVetoBlockedMappingMissing,
    HistoricalCompositeRejected,
    PostDataArtifactRejected,
    StepBoundaryPredictionBlocked,
    T12PrerequisiteMissing,
    UnverifiedCandidateRejected,
)


class ProvenanceAdjudicationTests(unittest.TestCase):
    def candidate(self, **changes: object) -> CandidateEvidence:
        values: dict[str, object] = {
            "object_id": "lambda0",
            "source_path": "release/config.json",
            "source_sha256": "a" * 64,
            "evidence_tier": EvidenceTier.EXACT_FROZEN_RELEASE_MACHINE_CONFIG,
            "exposure_class": ExposureClass.PRE_TARGET_DATA,
            "exact_frozen_lineage": True,
            "machine_readable": True,
        }
        values.update(changes)
        return CandidateEvidence(**values)  # type: ignore[arg-type]

    def test_authentic_candidate_is_admissible(self) -> None:
        self.candidate().assert_admissible_as_frozen()

    def test_post_data_candidate_cannot_become_frozen(self) -> None:
        with self.assertRaises(PostDataArtifactRejected):
            self.candidate(
                exposure_class=ExposureClass.POST_DATA,
                evidence_tier=EvidenceTier.HISTORICAL_CANDIDATE,
                exact_frozen_lineage=False,
            ).assert_admissible_as_frozen()

    def test_unknown_exposure_cannot_silently_become_clean(self) -> None:
        with self.assertRaises(UnverifiedCandidateRejected):
            self.candidate(
                exposure_class=ExposureClass.UNKNOWN_EXPOSURE
            ).assert_admissible_as_clean_frozen_predictor()

    def test_exact_frozen_object_and_clean_prediction_status_are_distinct(self) -> None:
        candidate = self.candidate(exposure_class=ExposureClass.POST_DATA)
        candidate.assert_admissible_as_frozen()
        self.assertTrue(candidate.authentic_frozen_object)
        self.assertFalse(candidate.admissible_as_clean_frozen_predictor)

    def test_digitisation_cannot_be_promoted(self) -> None:
        with self.assertRaises(UnverifiedCandidateRejected):
            self.candidate(evidence_tier=EvidenceTier.INFERENCE_OR_DIGITISATION).assert_admissible_as_frozen()

    def test_malformed_source_hash_cannot_be_promoted(self) -> None:
        with self.assertRaises(UnverifiedCandidateRejected):
            self.candidate(source_sha256="z" * 64).assert_admissible_as_frozen()

    def test_historical_composite_is_rejected(self) -> None:
        with self.assertRaises(HistoricalCompositeRejected):
            self.candidate(historical_composite=True).assert_admissible_as_frozen()

    def test_conflicting_candidates_block_bundle_completion(self) -> None:
        first = self.candidate()
        second = self.candidate(source_path="release/other.json", source_sha256="b" * 64)
        result = assess_frozen_bundle(("lambda0",), (first, second))
        self.assertFalse(result.complete)
        self.assertEqual(result.conflicting_object_ids, ("lambda0",))

    def test_incomplete_authentic_bundle_remains_blocked(self) -> None:
        result = assess_frozen_bundle(("lambda0", "lambdaA"), (self.candidate(),))
        self.assertEqual(result.status, "AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE")
        self.assertEqual(result.missing_object_ids, ("lambdaA",))

    def test_complete_structural_fixture_validates_shape_only(self) -> None:
        path = ROOT / "tests/fixtures/NON_PHYSICAL_FROZEN_BUNDLE_FIXTURE.json"
        result = validate_non_physical_structural_fixture(json.loads(path.read_text(encoding="utf-8")))
        self.assertTrue(result["structural_shape_valid"])
        self.assertFalse(result["physics_values_present"])
        self.assertFalse(result["prediction_authorized"])


class AcquisitionGateTests(unittest.TestCase):
    def test_incomplete_external_mapping_cannot_unlock_veto(self) -> None:
        with self.assertRaises(ExternalVetoBlockedMappingMissing):
            ExternalMappingEvidence("KATRIN").assert_authorized()

    def test_complete_mapping_contract_is_structurally_authorized(self) -> None:
        mapping = ExternalMappingEvidence(
            "TEST_ONLY",
            ("x = f(theta)",),
            ("eV2",),
            ("0 <= x <= 1",),
            "native likelihood semantics retained",
            ("NON_PHYSICAL_TEST_SOURCE",),
            ("not an LSC mapping",),
        )
        mapping.assert_authorized()

    def test_missing_authoritative_covariance_cannot_unlock_scenario(self) -> None:
        with self.assertRaises(CollaborationCovarianceUnavailable):
            assert_collaboration_covariance_authorized(
                matrix_acquired=False,
                authenticated_source=False,
                source_sha256=None,
            )
        with self.assertRaises(CollaborationCovarianceUnavailable):
            assert_collaboration_covariance_authorized(
                matrix_acquired=True,
                authenticated_source=True,
                source_sha256="z" * 64,
            )

    def test_one_missing_t12_prerequisite_keeps_t12_blocked(self) -> None:
        prerequisites = T12Prerequisites(True, True, True, True, True, True, True, False)
        with self.assertRaises(T12PrerequisiteMissing):
            prerequisites.assert_authorized()
        self.assertEqual(prerequisites.missing, ("required_units",))

    def test_step05_blocks_prediction_even_if_bundle_were_complete(self) -> None:
        with self.assertRaises(StepBoundaryPredictionBlocked):
            assert_step05_prediction_authorized(bundle_complete=True)


class Step05GoldenTests(unittest.TestCase):
    def test_required_step05_publication_artifacts_exist(self) -> None:
        required = {
            "docs/acquisition/STEP_05_BLOCKER_ACQUISITION_REPORT.md",
            "docs/acquisition/FROZEN_NUMERICAL_BUNDLE_SEARCH.md",
            "docs/acquisition/FROZEN_PARAMETER_ADJUDICATION.csv",
            "docs/acquisition/LSC_TO_KATRIN_MAPPING_ASSESSMENT.md",
            "docs/acquisition/LSC_TO_ICECUBE_MAPPING_ASSESSMENT.md",
            "docs/acquisition/M3_GEOMETRY_ASSESSMENT.md",
            "docs/acquisition/M4_HIERARCHICAL_ADJUDICATION.md",
            "docs/acquisition/T12_DATA_ASSESSMENT.md",
            "docs/acquisition/VALIDATION_UNLOCK_MATRIX.md",
            "docs/acquisition/NEGATIVE_FINDINGS.md",
            "docs/acquisition/ACQUISITION_SEARCH_LOG.csv",
            "blocker_registry.json",
            "STEP_05_EVIDENCE_FREEZE.json",
        }
        self.assertFalse([relative for relative in sorted(required) if not (ROOT / relative).is_file()])

    def test_parameter_adjudication_has_required_contract_and_objects(self) -> None:
        path = ROOT / "docs/acquisition/FROZEN_PARAMETER_ADJUDICATION.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        required_fields = {
            "parameter_id", "canonical_name", "required_by_equation", "candidate_value",
            "units", "frame", "source_path", "source_commit", "source_date", "source_hash",
            "evidence_class", "exposure_class", "conflict_status", "adjudication", "reason",
        }
        self.assertEqual(set(rows[0]), required_fields)
        names = {row["canonical_name"] for row in rows}
        self.assertTrue(
            {
                "theta", "parameter_ordering", "lambda0", "lambdaA", "f0_a", "fA_a",
                "active_tensor_components", "tensor_orientation", "complete_reference_frame",
                "complete_units", "numerical_configuration", "parameter_bounds",
                "numerical_defaults", "frozen_prediction_table",
            }
            <= names
        )
        self.assertTrue(all(row["adjudication"] in {"STILL_MISSING", "UNVERIFIED_CANDIDATE"} for row in rows))

    def test_step05_publication_paths_are_repo_relative(self) -> None:
        candidates = [
            path
            for path in (ROOT / "docs/acquisition").rglob("*")
            if path.is_file()
        ]
        candidates.extend((ROOT / name) for name in ("blocker_registry.json", "STEP_05_EVIDENCE_FREEZE.json"))
        self.assertEqual(scan_publication_paths(candidates, root=ROOT), ())

    def test_golden_state_is_derived_from_machine_readable_artifacts(self) -> None:
        status = json.loads((ROOT / "frozen_core/manifests/kernel_status.json").read_text(encoding="utf-8"))
        blockers = json.loads((ROOT / "blocker_registry.json").read_text(encoding="utf-8"))
        self.assertTrue(status["symbolic_model_ready"])
        self.assertTrue(status["likelihood_engine_ready"])
        self.assertTrue(status["baseline_engine_ready"])
        self.assertEqual(status["frozen_bundle_recovery_status"], "AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE")
        self.assertFalse(status["frozen_bundle_complete"])
        self.assertFalse(status["minimum_validation_unlock_set_complete"])
        self.assertFalse(status["prediction_authorized"])
        self.assertFalse(status["numerical_validation_authorized"])
        self.assertEqual(
            status["acquisition_verdict"],
            "BLOCKER_ADJUDICATION_COMPLETE_FROZEN_BUNDLE_STILL_MISSING",
        )
        self.assertEqual(status["T12_data_status"], "BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT")
        self.assertFalse(blockers["minimum_validation_unlock_set"]["complete"])

    def test_registry_has_every_priority_and_no_authorization(self) -> None:
        value = blocker_registry()
        self.assertEqual({row["priority"] for row in value["records"]}, {"P0", "P1", "P2", "P3", "P4", "P5"})
        self.assertFalse(value["prediction_authorized"])
        self.assertFalse(value["numerical_validation_authorized"])

    def test_evidence_freeze_verifies(self) -> None:
        value = json.loads((ROOT / "STEP_05_EVIDENCE_FREEZE.json").read_text(encoding="utf-8"))
        self.assertTrue(verify_evidence_freeze(ROOT, value))


if __name__ == "__main__":
    unittest.main()
