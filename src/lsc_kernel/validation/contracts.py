"""Validation test interfaces and the non-negotiable T12 hard gate."""

from __future__ import annotations

from typing import Any, Mapping

from lsc_kernel.errors import ValidationNotAuthorized

from .datasets import DatasetContract, ValidationDatasetRecord, ValidationDatasetRegistry
from .registries import ValidationTestDefinition, validation_test_registry


def validation_test_definitions() -> tuple[ValidationTestDefinition, ...]:
    """Compatibility entry point returning the canonical Step 03 registry."""

    return validation_test_registry()


T12_REQUIRED_FLAGS = (
    "precise_timing",
    "surveyed_orientation",
    "sufficient_geometry",
    "complete_active_tensor",
    "required_reference_frames",
    "required_units",
)


class T12Gate:
    """Hard gate for every directional or sidereal execution path."""

    @staticmethod
    def blockers(context: Mapping[str, Any]) -> tuple[str, ...]:
        blockers = [flag for flag in T12_REQUIRED_FLAGS if context.get(flag) is not True]
        if context.get("timing_basis") == "exposure_midpoint":
            blockers.append("EXPOSURE_MIDPOINT_IS_NOT_EVENT_TIME")
        return tuple(blockers)

    @classmethod
    def assert_authorized(cls, context: Mapping[str, Any]) -> None:
        blockers = cls.blockers(context)
        if blockers:
            raise ValidationNotAuthorized(
                "T12 is BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT.",
                details={"test_id": "T12", "blockers": list(blockers)},
            )


__all__ = [
    "DatasetContract",
    "T12Gate",
    "ValidationDatasetRecord",
    "ValidationDatasetRegistry",
    "ValidationTestDefinition",
    "validation_test_definitions",
]
