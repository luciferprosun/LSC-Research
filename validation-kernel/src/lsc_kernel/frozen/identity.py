"""Immutable identity for the historical frozen model specification."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from lsc_kernel.errors import FrozenIdentityMismatch


@dataclass(frozen=True, slots=True)
class FrozenModelIdentity:
    """Content-addressed identity of the object recovered in Step 01."""

    model_name: str
    canonical_version: str
    historical_git_commit: str
    freeze_commit: str
    zenodo_version_doi: str
    zenodo_concept_doi: str
    symbolic_equation_set_identity: str
    provenance_registry_checksum: str
    source_manifest_checksum: str
    kernel_schema_version: str

    @classmethod
    def canonical(cls) -> "FrozenModelIdentity":
        return cls(
            model_name="LSC",
            canonical_version="6.3.0-pre-BEST2-freeze-update",
            historical_git_commit="6ffa07bdde533fcc2a550e36c762b8edd9236c47",
            freeze_commit="a6d582694d55fa0260ef7ab07ed83fd06feef607",
            zenodo_version_doi="10.5281/zenodo.20377427",
            zenodo_concept_doi="10.5281/zenodo.19780615",
            symbolic_equation_set_identity=(
                "LSC-E1-E12@sha256:"
                "af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981"
            ),
            provenance_registry_checksum=(
                "f8c595a27f4352424712dab2300c2e01bdafd8cdda4ba5fabef50c1feb77d67c"
            ),
            source_manifest_checksum=(
                "e16b7b5ac775389aa3fdf5b319d0ecb3460eab3bf3126f850d1ef4da84c659ce"
            ),
            kernel_schema_version="1.0.0",
        )

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


IDENTITY_FIELDS = tuple(FrozenModelIdentity.__dataclass_fields__)


def validate_identity(
    actual: FrozenModelIdentity | Mapping[str, Any],
    expected: FrozenModelIdentity | None = None,
) -> FrozenModelIdentity:
    """Return the canonical identity or reject every identity mismatch."""

    expected = expected or FrozenModelIdentity.canonical()
    values: Mapping[str, Any] = actual.as_dict() if isinstance(actual, FrozenModelIdentity) else actual
    missing = [field for field in IDENTITY_FIELDS if field not in values]
    unknown = sorted(set(values) - set(IDENTITY_FIELDS))
    mismatches = {
        field: {"expected": getattr(expected, field), "actual": values.get(field)}
        for field in IDENTITY_FIELDS
        if field in values and values[field] != getattr(expected, field)
    }
    if missing or unknown or mismatches:
        raise FrozenIdentityMismatch(
            "Frozen model identity does not match the Step 01 authenticated object.",
            details={"missing_fields": missing, "unknown_fields": unknown, "mismatches": mismatches},
        )
    return actual if isinstance(actual, FrozenModelIdentity) else expected
