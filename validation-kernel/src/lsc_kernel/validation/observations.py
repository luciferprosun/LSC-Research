"""Value-neutral observation contracts for future validation layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ObservationSet:
    observation_set_id: str
    values: Mapping[str, Any]
    units: Mapping[str, str]
    frames: Mapping[str, str]
    source_references: tuple[str, ...] = field(default_factory=tuple)
    timing_basis: str | None = None
