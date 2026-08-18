"""Deterministic result and execution-manifest contracts."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import scipy


def canonical_json_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class StatisticEvaluation:
    raw_statistic: float
    profiled_statistic: float
    statistic_type: str
    n_observations: int
    n_fitted_parameters: int
    dof_if_valid: int | None
    convergence: bool
    assumptions: tuple[str, ...]
    covariance_diagnostics: Mapping[str, Any] | None = None
    nuisance_values: tuple[tuple[str, float], ...] = ()
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["nuisance_values"] = dict(self.nuisance_values)
        return result


@dataclass(frozen=True, slots=True)
class StatisticalExecutionManifest:
    manifest_schema_version: str
    dataset_hashes: tuple[tuple[str, str], ...]
    model: str
    model_version: str
    parameters_fitted: tuple[str, ...]
    nuisance_treatment: str
    covariance_scenario: str
    split: str
    metric: str
    optimizer: str
    code_commit: str
    code_tree_hash: str
    code_commit_relationship: str
    environment_hash: str
    classification: str
    timestamp: str
    LSC_used: bool = False

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["dataset_hashes"] = dict(self.dataset_hashes)
        result["execution_manifest_hash"] = canonical_json_hash(result)
        return result

    @classmethod
    def build(
        cls,
        *,
        repository_root: Path,
        dataset_hashes: Mapping[str, str],
        model: str,
        model_version: str,
        parameters_fitted: tuple[str, ...],
        nuisance_treatment: str,
        covariance_scenario: str,
        split: str,
        metric: str,
        optimizer: str,
        classification: str,
        timestamp: str,
        code_commit: str | None = None,
    ) -> "StatisticalExecutionManifest":
        commit = code_commit or subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True, capture_output=True, text=True
        ).stdout.strip()
        if len(commit) != 40 or any(character not in "0123456789abcdef" for character in commit.lower()):
            raise ValueError("code_commit must be a full 40-character Git SHA.")
        for dataset_id, digest in dataset_hashes.items():
            if not dataset_id or len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest.lower()):
                raise ValueError("Every dataset identity requires a full SHA-256 digest.")
        source_files = sorted((repository_root / "src").rglob("*.py")) + [repository_root / "pyproject.toml"]
        source_digest = hashlib.sha256()
        for path in source_files:
            relative = path.relative_to(repository_root).as_posix().encode("utf-8")
            source_digest.update(len(relative).to_bytes(8, "big"))
            source_digest.update(relative)
            payload = path.read_bytes()
            source_digest.update(len(payload).to_bytes(8, "big"))
            source_digest.update(payload)
        environment = {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "package": "lsc-validation-kernel",
        }
        return cls(
            manifest_schema_version="1.0.0",
            dataset_hashes=tuple(sorted(dataset_hashes.items())),
            model=model,
            model_version=model_version,
            parameters_fitted=parameters_fitted,
            nuisance_treatment=nuisance_treatment,
            covariance_scenario=covariance_scenario,
            split=split,
            metric=metric,
            optimizer=optimizer,
            code_commit=commit,
            code_tree_hash=source_digest.hexdigest(),
            code_commit_relationship="HASHED_SOURCE_TREE_DESCENDS_FROM_CODE_COMMIT",
            environment_hash=canonical_json_hash(environment),
            classification=classification,
            timestamp=timestamp,
            LSC_used=False,
        )


@dataclass(frozen=True, slots=True)
class BaselineResult:
    execution_manifest_hash: str
    model_id: str
    dataset_id: str
    split_id: str
    statistic: float
    statistic_type: str
    fitted_parameters: tuple[tuple[str, float], ...]
    nuisance_parameters: tuple[tuple[str, float], ...]
    n_observations: int
    n_parameters: int
    dof_if_valid: int | None
    AIC_if_valid: float | None
    BIC_if_valid: float | None
    predictive_score_if_valid: float | None
    covariance_scenario: str
    sensitivity_only: bool
    convergence: bool
    warnings: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["fitted_parameters"] = dict(self.fitted_parameters)
        result["nuisance_parameters"] = dict(self.nuisance_parameters)
        return result


BASELINE_RESULT_JSON_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "BaselineResult",
    "type": "object",
    "properties": {
        "execution_manifest_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "model_id": {"type": "string"},
        "dataset_id": {"type": "string"},
        "split_id": {"type": "string"},
        "statistic": {"type": "number"},
        "statistic_type": {"type": "string"},
        "fitted_parameters": {"type": "object", "additionalProperties": {"type": "number"}},
        "nuisance_parameters": {"type": "object", "additionalProperties": {"type": "number"}},
        "n_observations": {"type": "integer", "minimum": 1},
        "n_parameters": {"type": "integer", "minimum": 0},
        "dof_if_valid": {"type": ["integer", "null"]},
        "AIC_if_valid": {"type": ["number", "null"]},
        "BIC_if_valid": {"type": ["number", "null"]},
        "predictive_score_if_valid": {"type": ["number", "null"]},
        "covariance_scenario": {"type": "string"},
        "sensitivity_only": {"type": "boolean"},
        "convergence": {"type": "boolean"},
        "warnings": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "execution_manifest_hash", "model_id", "dataset_id", "split_id", "statistic", "statistic_type",
        "fitted_parameters", "nuisance_parameters", "n_observations", "n_parameters", "dof_if_valid",
        "AIC_if_valid", "BIC_if_valid", "predictive_score_if_valid", "covariance_scenario",
        "sensitivity_only", "convergence", "warnings",
    ],
    "additionalProperties": False,
}


STATISTICAL_EXECUTION_MANIFEST_JSON_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "StatisticalExecutionManifest",
    "type": "object",
    "properties": {
        "manifest_schema_version": {"const": "1.0.0"},
        "dataset_hashes": {"type": "object", "additionalProperties": {"type": "string", "pattern": "^[0-9a-f]{64}$"}},
        "model": {"type": "string"},
        "model_version": {"type": "string"},
        "parameters_fitted": {"type": "array", "items": {"type": "string"}},
        "nuisance_treatment": {"type": "string"},
        "covariance_scenario": {"type": "string"},
        "split": {"type": "string"},
        "metric": {"type": "string"},
        "optimizer": {"type": "string"},
        "code_commit": {"type": "string"},
        "code_tree_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "code_commit_relationship": {"const": "HASHED_SOURCE_TREE_DESCENDS_FROM_CODE_COMMIT"},
        "environment_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "classification": {"type": "string"},
        "timestamp": {"type": "string"},
        "LSC_used": {"const": False},
        "execution_manifest_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    },
    "required": [
        "manifest_schema_version", "dataset_hashes", "model", "model_version", "parameters_fitted",
        "nuisance_treatment", "covariance_scenario", "split", "metric", "optimizer", "code_commit",
        "code_tree_hash", "code_commit_relationship",
        "environment_hash", "classification", "timestamp", "LSC_used", "execution_manifest_hash",
    ],
    "additionalProperties": False,
}
