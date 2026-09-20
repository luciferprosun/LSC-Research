"""Request/result interfaces that carry authorization and provenance state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .observations import ObservationSet


@dataclass(frozen=True, slots=True)
class PredictionRequest:
    request_id: str
    model_identity: Mapping[str, Any]
    observations: ObservationSet
    requested_outputs: tuple[str, ...]
    purpose: str = "FROZEN_LSC_PREDICTION"


@dataclass(frozen=True, slots=True)
class PredictionResult:
    request_id: str
    authorized: bool
    outputs: Mapping[str, Any] = field(default_factory=dict)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    provenance: Mapping[str, Any] = field(default_factory=dict)
