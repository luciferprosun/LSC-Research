"""Source-bounded frame vocabulary and validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from lsc_kernel.errors import FrozenFrameUnknown


MISSING_FROZEN_FRAME = "MISSING_FROZEN_FRAME"


@dataclass(frozen=True, slots=True)
class FrameDefinition:
    name: str
    source_status: str
    complete: bool
    description: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


FRAME_DEFINITIONS = (
    FrameDefinition(
        "MODEL_INTERNAL",
        "NOT_SOURCE_DEFINED",
        False,
        "A separate model-internal frame is not defined by the frozen sources.",
    ),
    FrameDefinition(
        "DETECTOR_FRAME",
        "SYMBOLIC_NAME_ONLY",
        False,
        "Detector and lab orientation are required, but no surveyed detector transform is frozen.",
    ),
    FrameDefinition(
        "EARTH_FIXED",
        "UNVERIFIED_INTERMEDIATE",
        False,
        "Latitude and longitude appear in E11; no Earth-fixed intermediate transform is specified.",
    ),
    FrameDefinition(
        "LAB_FRAME",
        "AUTHENTIC_SYMBOLIC_ROLE",
        False,
        "E3 and E11 name lab-frame directions; origin, axes, handedness, and orientation are incomplete.",
    ),
    FrameDefinition(
        "ICRS",
        "AUTHENTIC_SYMBOLIC_ROLE",
        False,
        "E11 names ICRS, but the frozen celestial direction and complete transform metadata are absent.",
    ),
)


@dataclass(frozen=True, slots=True)
class FrameRequirement:
    field: str
    expected_frame: str
    status: str

    def validate(self, supplied_frame: str | None) -> None:
        if self.status == MISSING_FROZEN_FRAME:
            raise FrozenFrameUnknown(
                f"No complete authentic frozen frame is available for {self.field!r}.",
                details={"field": self.field, "status": self.status},
            )
        if self.status == "NOT_APPLICABLE":
            if supplied_frame not in (None, "NOT_APPLICABLE"):
                raise FrozenFrameUnknown(
                    f"Field {self.field!r} does not accept a frame.",
                    details={"field": self.field, "supplied_frame": supplied_frame},
                )
            return
        if supplied_frame != self.expected_frame:
            raise FrozenFrameUnknown(
                f"Frame mismatch for {self.field!r}.",
                details={"field": self.field, "expected": self.expected_frame, "actual": supplied_frame},
            )
