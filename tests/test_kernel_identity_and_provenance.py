from __future__ import annotations

import dataclasses
import unittest

from kernel_helpers import ROOT, authentic_parameter_record, fixture_policy, repository_policy

from lsc_kernel.errors import (
    FrozenIdentityMismatch,
    FrozenParameterProvenanceError,
    PostDataArtifactRejected,
    UnverifiedCandidateRejected,
)
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator
from lsc_kernel.frozen.identity import FrozenModelIdentity, validate_identity


class IdentityTests(unittest.TestCase):
    def test_correct_frozen_identity_is_accepted(self) -> None:
        identity = FrozenModelIdentity.canonical()
        self.assertIs(validate_identity(identity), identity)

    def test_wrong_historical_commit_is_rejected(self) -> None:
        identity = FrozenModelIdentity.canonical().as_dict()
        identity["historical_git_commit"] = "0" * 40
        with self.assertRaises(FrozenIdentityMismatch):
            validate_identity(identity)

    def test_wrong_model_version_is_rejected(self) -> None:
        identity = FrozenModelIdentity.canonical().as_dict()
        identity["canonical_version"] = "6.2.1"
        with self.assertRaises(FrozenIdentityMismatch):
            validate_identity(identity)

    def test_unknown_identity_field_is_rejected(self) -> None:
        identity = FrozenModelIdentity.canonical().as_dict()
        identity["critical_extension"] = "not frozen"
        with self.assertRaises(FrozenIdentityMismatch):
            validate_identity(identity)

    def test_identity_is_immutable(self) -> None:
        identity = FrozenModelIdentity.canonical()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            identity.canonical_version = "changed"  # type: ignore[misc]

    def test_repository_registry_checksum_is_verified(self) -> None:
        evaluator = FrozenLSCEvaluator.from_repository(ROOT)
        self.assertEqual(
            evaluator.identity.provenance_registry_checksum,
            "f8c595a27f4352424712dab2300c2e01bdafd8cdda4ba5fabef50c1feb77d67c",
        )


class ProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = repository_policy()

    def test_authentic_frozen_specification_is_accepted(self) -> None:
        result = self.policy.admit_specification("canonical-equations")
        self.assertEqual(result.classification.value, "AUTHENTIC_FROZEN")

    def test_deterministic_derived_specification_is_accepted_only_as_specification(self) -> None:
        result = self.policy.admit_specification("derived-frozen-model-manifest")
        self.assertEqual(result.classification.value, "DERIVED_FROM_FROZEN")
        with self.assertRaises(FrozenParameterProvenanceError):
            self.policy.admit_numerical(
                result.artifact_id,
                claimed_classification=result.classification.value,
                claimed_sha256=result.sha256,
            )

    def test_historical_post_data_is_rejected(self) -> None:
        with self.assertRaises(PostDataArtifactRejected):
            self.policy.admit_numerical("postdata-lsc621-coefficients")

    def test_unverified_conflict_is_rejected(self) -> None:
        with self.assertRaises(UnverifiedCandidateRejected):
            self.policy.admit_numerical("unverified-c0-c1-to-lambda-mapping")

    def test_authentic_document_cannot_masquerade_as_numeric_parameter(self) -> None:
        record = self.policy.record("canonical-parameter-structures")
        with self.assertRaises(FrozenParameterProvenanceError):
            self.policy.admit_numerical(
                record.artifact_id,
                claimed_classification=record.classification.value,
                claimed_sha256=record.sha256,
            )

    def test_forbidden_claim_labels_are_rejected(self) -> None:
        policy = fixture_policy()
        record = authentic_parameter_record()
        for label in ("UNVERIFIED_CONFLICT", "TOY", "ILLUSTRATIVE", "DEPRECATED"):
            with self.subTest(label=label), self.assertRaises(UnverifiedCandidateRejected):
                policy.admit_numerical(
                    record.artifact_id,
                    claimed_classification=label,
                    claimed_sha256=record.sha256,
                )

    def test_every_quarantined_registry_object_is_rejected_numerically(self) -> None:
        quarantined = [
            record
            for record in self.policy.records
            if record.classification.value in {"HISTORICAL_POST_DATA", "UNVERIFIED"}
        ]
        self.assertEqual(len(quarantined), 11)
        for record in quarantined:
            with self.subTest(artifact=record.artifact_id), self.assertRaises(
                (PostDataArtifactRejected, UnverifiedCandidateRejected)
            ):
                self.policy.admit_numerical(record.artifact_id)

    def test_lsc55_tensor_to_active_tensor_mapping_never_activates(self) -> None:
        with self.assertRaises(UnverifiedCandidateRejected):
            self.policy.admit_numerical("unverified-lsc55-D-to-active-A")


if __name__ == "__main__":
    unittest.main()
