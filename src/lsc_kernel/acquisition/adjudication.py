"""Fail-closed provenance adjudication for Step 05 evidence.

This module classifies evidence.  It contains no parameter fitting,
digitisation, interpolation, or physics evaluation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import IntEnum, StrEnum
from typing import Iterable, Mapping

from lsc_kernel.errors import (
    ConflictingCandidateRejected,
    HistoricalCompositeRejected,
    PostDataArtifactRejected,
    UnverifiedCandidateRejected,
)


def _valid_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value.lower())


class AcquisitionStatus(StrEnum):
    AUTHENTIC_FROZEN_RECOVERED = "AUTHENTIC_FROZEN_RECOVERED"
    AUTHORITATIVE_EXTERNAL_RECOVERED = "AUTHORITATIVE_EXTERNAL_RECOVERED"
    AUTHORITATIVE_COLLABORATION_RECOVERED = "AUTHORITATIVE_COLLABORATION_RECOVERED"
    DERIVED_WITH_EXACT_PROVENANCE = "DERIVED_WITH_EXACT_PROVENANCE"
    UNVERIFIED_CANDIDATE = "UNVERIFIED_CANDIDATE"
    CONFLICTING_CANDIDATES = "CONFLICTING_CANDIDATES"
    NOT_PUBLIC = "NOT_PUBLIC"
    NOT_LOCATED = "NOT_LOCATED"
    STILL_MISSING = "STILL_MISSING"


class ExposureClass(StrEnum):
    PRE_DATA = "PRE_DATA"
    PRE_TARGET_DATA = "PRE_TARGET_DATA"
    POST_DATA = "POST_DATA"
    UNKNOWN_EXPOSURE = "UNKNOWN_EXPOSURE"


class EvidenceTier(IntEnum):
    EXACT_FROZEN_RELEASE_MACHINE_CONFIG = 1
    EXACT_FROZEN_COMMIT_CONFIG_OR_SOURCE = 2
    EXACT_ARCHIVED_RELEASE_MACHINE_ARTIFACT = 3
    VERSIONED_NUMERICAL_TABLE_TIED_TO_FREEZE = 4
    NUMERICAL_APPENDIX_TIED_TO_RELEASE = 5
    HISTORICAL_CANDIDATE = 6
    INFERENCE_OR_DIGITISATION = 7


@dataclass(frozen=True, slots=True)
class CandidateEvidence:
    object_id: str
    source_path: str
    source_sha256: str
    evidence_tier: EvidenceTier
    exposure_class: ExposureClass
    exact_frozen_lineage: bool
    machine_readable: bool
    conflict: bool = False
    historical_composite: bool = False
    notes: str = ""

    @property
    def authentic_frozen_object(self) -> bool:
        return (
            self.evidence_tier <= EvidenceTier.NUMERICAL_APPENDIX_TIED_TO_RELEASE
            and self.exact_frozen_lineage
            and _valid_sha256(self.source_sha256)
            and not self.conflict
            and not self.historical_composite
        )

    @property
    def admissible_as_clean_frozen_predictor(self) -> bool:
        return self.authentic_frozen_object and self.exposure_class in {
            ExposureClass.PRE_DATA,
            ExposureClass.PRE_TARGET_DATA,
        }

    def assert_admissible_as_frozen(self) -> None:
        if self.historical_composite:
            raise HistoricalCompositeRejected(
                "HISTORICAL_COMPOSITE_INVALID_FOR_FROZEN_VALIDATION",
                details={"object_id": self.object_id},
            )
        if self.conflict:
            raise ConflictingCandidateRejected(
                "Conflicting candidates cannot complete a frozen bundle.",
                details={"object_id": self.object_id},
            )
        if self.exposure_class == ExposureClass.POST_DATA and not self.authentic_frozen_object:
            raise PostDataArtifactRejected(
                "A post-data candidate outside the exact frozen lineage cannot be promoted.",
                details={"object_id": self.object_id},
            )
        if not self.authentic_frozen_object:
            raise UnverifiedCandidateRejected(
                "Candidate lacks the exact provenance required for frozen admission.",
                details={
                    "object_id": self.object_id,
                    "evidence_tier": int(self.evidence_tier),
                    "exposure_class": self.exposure_class.value,
                    "source_sha256_valid": _valid_sha256(self.source_sha256),
                },
            )

    def assert_admissible_as_clean_frozen_predictor(self) -> None:
        self.assert_admissible_as_frozen()
        if not self.admissible_as_clean_frozen_predictor:
            raise UnverifiedCandidateRejected(
                "Authenticity does not establish clean pre-target-data prediction status.",
                details={
                    "object_id": self.object_id,
                    "exposure_class": self.exposure_class.value,
                },
            )

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["evidence_tier"] = int(self.evidence_tier)
        result["evidence_tier_name"] = self.evidence_tier.name
        result["exposure_class"] = self.exposure_class.value
        result["authentic_frozen_object"] = self.authentic_frozen_object
        result["admissible_as_clean_frozen_predictor"] = self.admissible_as_clean_frozen_predictor
        return result


@dataclass(frozen=True, slots=True)
class FrozenBundleAssessment:
    required_object_ids: tuple[str, ...]
    admitted_object_ids: tuple[str, ...]
    missing_object_ids: tuple[str, ...]
    conflicting_object_ids: tuple[str, ...]
    rejected_object_ids: tuple[str, ...]
    status: str
    complete: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def assess_frozen_bundle(
    required_object_ids: Iterable[str],
    candidates: Iterable[CandidateEvidence],
) -> FrozenBundleAssessment:
    """Assess completeness without combining incompatible historical epochs."""

    required = tuple(dict.fromkeys(required_object_ids))
    grouped: dict[str, list[CandidateEvidence]] = {object_id: [] for object_id in required}
    for candidate in candidates:
        if candidate.object_id in grouped:
            grouped[candidate.object_id].append(candidate)

    admitted: list[str] = []
    missing: list[str] = []
    conflicting: list[str] = []
    rejected: list[str] = []
    for object_id in required:
        object_candidates = grouped[object_id]
        if not object_candidates:
            missing.append(object_id)
            continue
        if len({candidate.source_sha256 for candidate in object_candidates}) > 1 or any(
            candidate.conflict for candidate in object_candidates
        ):
            conflicting.append(object_id)
            continue
        if any(candidate.authentic_frozen_object for candidate in object_candidates):
            admitted.append(object_id)
        else:
            rejected.append(object_id)

    complete = not (missing or conflicting or rejected) and len(admitted) == len(required)
    return FrozenBundleAssessment(
        required_object_ids=required,
        admitted_object_ids=tuple(admitted),
        missing_object_ids=tuple(missing),
        conflicting_object_ids=tuple(conflicting),
        rejected_object_ids=tuple(rejected),
        status="AUTHENTIC_FROZEN_BUNDLE_COMPLETE" if complete else "AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE",
        complete=complete,
    )


def validate_non_physical_structural_fixture(value: Mapping[str, object]) -> dict[str, object]:
    """Validate ingestion shape only; never convert a fixture into model input."""

    if value.get("classification") != "NON_PHYSICAL_FROZEN_BUNDLE_FIXTURE":
        raise ValueError("Structural fixture must carry the NON_PHYSICAL marker.")
    if value.get("prediction_authorized") is not False:
        raise ValueError("Structural fixture may never authorize prediction.")
    fields = value.get("parameter_shapes")
    if not isinstance(fields, list) or not fields:
        raise ValueError("Structural fixture must enumerate parameter shapes.")
    required_keys = {"canonical_name", "kind", "shape", "value_marker"}
    for field in fields:
        if not isinstance(field, Mapping) or not required_keys <= set(field):
            raise ValueError("Malformed structural parameter shape.")
        if field["value_marker"] != "NON_PHYSICAL_TEST_VALUE_OMITTED":
            raise ValueError("Structural fixture must not contain physical values.")
    return {
        "classification": "NON_PHYSICAL_FROZEN_BUNDLE_FIXTURE",
        "structural_shape_valid": True,
        "physics_values_present": False,
        "prediction_authorized": False,
    }
