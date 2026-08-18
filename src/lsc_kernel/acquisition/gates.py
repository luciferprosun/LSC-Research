"""Independent Step 05 authorization gates."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from lsc_kernel.errors import (
    CollaborationCovarianceUnavailable,
    ExternalVetoBlockedMappingMissing,
    StepBoundaryPredictionBlocked,
    T12PrerequisiteMissing,
)


@dataclass(frozen=True, slots=True)
class ExternalMappingEvidence:
    constraint_id: str
    explicit_equations: tuple[str, ...] = ()
    units: tuple[str, ...] = ()
    parameter_domain: tuple[str, ...] = ()
    statistical_interpretation: str = ""
    provenance: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    @property
    def authorized(self) -> bool:
        return all(
            (
                self.explicit_equations,
                self.units,
                self.parameter_domain,
                self.statistical_interpretation,
                self.provenance,
                self.limitations,
            )
        )

    def assert_authorized(self) -> None:
        if not self.authorized:
            raise ExternalVetoBlockedMappingMissing(
                "External veto mapping is incomplete.",
                details={"constraint_id": self.constraint_id},
            )

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["authorized"] = self.authorized
        return result


def assert_collaboration_covariance_authorized(
    *,
    matrix_acquired: bool,
    authenticated_source: bool,
    source_sha256: str | None,
) -> None:
    digest = str(source_sha256 or "").lower()
    valid_hash = len(digest) == 64 and all(character in "0123456789abcdef" for character in digest)
    if not (matrix_acquired and authenticated_source and valid_hash):
        raise CollaborationCovarianceUnavailable(
            "COV_COLLABORATION requires an authenticated matrix and verified source hash."
        )


@dataclass(frozen=True, slots=True)
class T12Prerequisites:
    precise_timing: bool
    sufficient_time_resolution: bool
    surveyed_detector_orientation: bool
    surveyed_source_orientation: bool
    earth_fixed_geometry: bool
    complete_active_tensor: bool
    frame_transforms: bool
    required_units: bool

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(name for name, available in asdict(self).items() if not available)

    @property
    def authorized(self) -> bool:
        return not self.missing

    def assert_authorized(self) -> None:
        if self.missing:
            raise T12PrerequisiteMissing(
                "BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT",
                details={"missing": list(self.missing)},
            )


def assert_step05_prediction_authorized(*, bundle_complete: bool) -> None:
    """Step 05 never authorizes execution, even if acquisition succeeds."""

    raise StepBoundaryPredictionBlocked(
        "LSC prediction is blocked by the Step 05 acquisition/evaluation boundary.",
        details={"bundle_complete": bundle_complete, "step": "STEP_05"},
    )
