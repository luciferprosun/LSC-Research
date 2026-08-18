"""Future result schema; Step 03 never instantiates scientific results."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ValidationResult:
    test_id: str
    execution_manifest_hash: str
    status: str
    observed_metric: Any
    baseline_metrics: tuple[tuple[str, Any], ...]
    lsc_metric: Any
    nuisance_scenario: str
    covariance_scenario: str
    uncertainty: Any
    sensitivity_only: bool
    preregistered: bool
    blinded: bool
    falsification_state: str
    interpretation_allowed: tuple[str, ...]
    notes: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["LSC_metric"] = result.pop("lsc_metric")
        return result


VALIDATION_RESULT_JSON_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ValidationResult",
    "type": "object",
    "properties": {
        "test_id": {"type": "string", "pattern": "^T(?:[1-9]|1[0-2])$"},
        "execution_manifest_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "status": {"type": "string"},
        "observed_metric": {},
        "baseline_metrics": {"type": "array"},
        "LSC_metric": {},
        "nuisance_scenario": {"type": "string"},
        "covariance_scenario": {"type": "string"},
        "uncertainty": {},
        "sensitivity_only": {"type": "boolean"},
        "preregistered": {"type": "boolean"},
        "blinded": {"type": "boolean"},
        "falsification_state": {"type": "string"},
        "interpretation_allowed": {"type": "array", "items": {"type": "string"}},
        "notes": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "test_id", "execution_manifest_hash", "status", "observed_metric", "baseline_metrics", "LSC_metric",
        "nuisance_scenario", "covariance_scenario", "uncertainty", "sensitivity_only", "preregistered",
        "blinded", "falsification_state", "interpretation_allowed", "notes",
    ],
    "additionalProperties": False,
}
