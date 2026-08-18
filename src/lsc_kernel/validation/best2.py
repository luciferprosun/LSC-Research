"""Future-only BEST-2 prediction contract; contains no prediction values."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class BEST2FuturePredictionContract:
    schema_version: str = "1.0.0"
    status: str = "FUTURE_ONLY"
    blindness_level: str = "FUTURE_BLIND"
    isotope: str = "58Co proposal; final isotope must be collaboration-confirmed"
    source_concept: str = "400 kCi proposal; final assay and covariance required"
    geometry_version: str = "2025 three-zone proposal; as-built survey required"
    proposed_exposures: str = "10 exposures of 16 days in proposal; actual schedule required"
    source_reference: str = "arXiv:2501.08127; DOI:10.31857/S0044451025030058"
    planned_observable: str = "zone-resolved 71Ge production rate"
    prediction_schema: str = "zone, exposure, prediction, units, frozen identity, provenance"
    freeze_requirements: tuple[str, ...] = (
        "complete authentic frozen numerical LSC bundle",
        "collaboration-approved as-built geometry and source insertion coordinates",
        "final isotope/branching/source assay and covariance",
        "actual exposure/extraction/counting protocol",
        "predeclared cross-section/covariance/nuisance policy",
    )
    timestamp_of_prediction_freeze: str | None = None
    hash_requirements: tuple[str, ...] = (
        "model identity/hash",
        "parameter bundle hash",
        "geometry hash",
        "source certificate hash",
        "prediction table hash",
        "preregistration hash",
    )
    prediction_values: tuple[()] = ()

    def as_dict(self) -> dict[str, object]:
        return asdict(self)
