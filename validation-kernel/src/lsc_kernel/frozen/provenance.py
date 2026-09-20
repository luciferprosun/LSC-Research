"""Single admission boundary for frozen specification and numerical inputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from lsc_kernel.errors import (
    FrozenParameterMissing,
    FrozenParameterProvenanceError,
    PostDataArtifactRejected,
    UnverifiedCandidateRejected,
)
from lsc_kernel.status import ProvenanceClassification


SPECIFICATION_CLASSES = frozenset(
    {
        ProvenanceClassification.AUTHENTIC_FROZEN,
        ProvenanceClassification.DERIVED_FROM_FROZEN,
    }
)
NUMERICAL_CLASSES = frozenset({ProvenanceClassification.AUTHENTIC_FROZEN})
NUMERICAL_ARTIFACT_TYPES = frozenset(
    {
        "parameter",
        "parameter_vector",
        "parameter_tensor",
        "configuration",
        "result_table",
    }
)
FORBIDDEN_CLAIMS = frozenset(
    {"UNVERIFIED_CONFLICT", "TOY", "ILLUSTRATIVE", "DEPRECATED"}
)


@dataclass(frozen=True, slots=True)
class ProvenanceRecord:
    artifact_id: str
    artifact_type: str
    parameter_or_role: str
    value_or_summary: str
    units: str
    source_path: str
    git_commit: str
    git_tag: str
    timestamp_if_known: str
    sha256: str
    data_exposure_status: str
    classification: ProvenanceClassification
    confidence: str
    notes: str

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "ProvenanceRecord":
        values: dict[str, Any] = dict(row)
        values["classification"] = ProvenanceClassification(row["classification"])
        return cls(**values)


class ProvenancePolicy:
    """Central answer to: may this object enter the frozen evaluator?"""

    def __init__(self, records: Iterable[ProvenanceRecord]) -> None:
        indexed = {record.artifact_id: record for record in records}
        if not indexed:
            raise ValueError("The provenance registry is empty.")
        self._records = indexed

    @classmethod
    def from_csv(cls, path: Path | str) -> "ProvenancePolicy":
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            return cls(ProvenanceRecord.from_row(row) for row in csv.DictReader(handle))

    @property
    def records(self) -> tuple[ProvenanceRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))

    def record(self, artifact_id: str) -> ProvenanceRecord:
        try:
            return self._records[artifact_id]
        except KeyError as exc:
            raise FrozenParameterProvenanceError(
                f"Artifact {artifact_id!r} is absent from the frozen provenance registry.",
                details={"artifact_id": artifact_id},
            ) from exc

    def _reject_non_admissible(self, record: ProvenanceRecord) -> None:
        if record.classification is ProvenanceClassification.HISTORICAL_POST_DATA:
            raise PostDataArtifactRejected(
                f"Post-data artifact {record.artifact_id!r} cannot enter the frozen evaluator.",
                details={"artifact_id": record.artifact_id, "classification": record.classification},
            )
        if record.classification is ProvenanceClassification.UNVERIFIED:
            raise UnverifiedCandidateRejected(
                f"Unverified artifact {record.artifact_id!r} cannot enter the frozen evaluator.",
                details={"artifact_id": record.artifact_id, "classification": record.classification},
            )
        if record.classification is ProvenanceClassification.MISSING:
            raise FrozenParameterMissing(
                f"Frozen object {record.artifact_id!r} is explicitly missing.",
                details={"artifact_id": record.artifact_id},
            )
        raise FrozenParameterProvenanceError(
            f"Artifact {record.artifact_id!r} is not admissible for this purpose.",
            details={"artifact_id": record.artifact_id, "classification": record.classification},
        )

    def admit_specification(self, artifact_id: str) -> ProvenanceRecord:
        record = self.record(artifact_id)
        if record.classification not in SPECIFICATION_CLASSES:
            self._reject_non_admissible(record)
        return record

    def admit_numerical(
        self,
        artifact_id: str,
        *,
        claimed_classification: str | None = None,
        claimed_sha256: str | None = None,
    ) -> ProvenanceRecord:
        if claimed_classification in FORBIDDEN_CLAIMS:
            raise UnverifiedCandidateRejected(
                f"Claimed provenance {claimed_classification!r} is forbidden for frozen numerical input.",
                details={"artifact_id": artifact_id, "classification": claimed_classification},
            )
        record = self.record(artifact_id)
        if record.classification not in NUMERICAL_CLASSES:
            self._reject_non_admissible(record)
        if claimed_classification and claimed_classification != record.classification.value:
            raise FrozenParameterProvenanceError(
                "Bundle provenance classification disagrees with the registry.",
                details={
                    "artifact_id": artifact_id,
                    "claimed": claimed_classification,
                    "registered": record.classification.value,
                },
            )
        if record.artifact_type not in NUMERICAL_ARTIFACT_TYPES:
            raise FrozenParameterProvenanceError(
                "An authentic specification document is not an authenticated numerical parameter source.",
                details={"artifact_id": artifact_id, "artifact_type": record.artifact_type},
            )
        if record.sha256 == "NOT_APPLICABLE":
            raise FrozenParameterProvenanceError(
                "A numerical input requires a content hash.",
                details={"artifact_id": artifact_id},
            )
        if claimed_sha256 != record.sha256:
            raise FrozenParameterProvenanceError(
                "Bundle artifact hash disagrees with the registry.",
                details={"artifact_id": artifact_id},
            )
        return record
