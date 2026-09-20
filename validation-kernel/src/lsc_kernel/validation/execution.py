"""Dry-run validation planner; it cannot compute an LSC prediction or result."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from lsc_kernel.frozen.identity import FrozenModelIdentity

from .datasets import ValidationDatasetRegistry, canonical_dataset_registry
from .registries import (
    baseline_model_registry,
    covariance_scenario_registry,
    nuisance_parameter_registry,
    split_registry,
    validation_test_registry,
)


def _canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _head_commit(root: Path) -> str:
    head = (root / ".git/HEAD").read_text(encoding="utf-8").strip()
    if not head.startswith("ref: "):
        return head
    ref = root / ".git" / head.removeprefix("ref: ")
    if ref.is_file():
        return ref.read_text(encoding="utf-8").strip()
    return "HEAD_REF_NOT_LOOSE"


@dataclass(frozen=True, slots=True)
class ValidationExecutionManifest:
    manifest_schema_version: str
    test_id: str
    model_identity: dict[str, str]
    model_hash: str
    dataset_hashes: tuple[tuple[str, str], ...]
    transformation_version: str
    split_id: str
    baseline_versions: tuple[tuple[str, str], ...]
    covariance_scenario: str
    nuisance_policy: str
    metric: str
    code_commit: str
    environment_hash: str
    timestamp: str
    authorization_state: str
    prediction_authorized: bool
    numerical_validation_authorized: bool

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["dataset_hashes"] = dict(self.dataset_hashes)
        result["baseline_versions"] = dict(self.baseline_versions)
        result["execution_manifest_hash"] = _canonical_hash(result)
        return result


class DryRunValidationHarness:
    """Builds an auditable execution plan and stops before prediction."""

    def __init__(self, repository_root: Path, datasets: ValidationDatasetRegistry | None = None) -> None:
        self.root = repository_root
        self.datasets = datasets or canonical_dataset_registry()
        self.tests = {test.test_id: test for test in validation_test_registry()}
        self.splits = {item["split_id"]: item for item in split_registry()["splits"]}
        self.covariance = {item["scenario_id"]: item for item in covariance_scenario_registry()["scenarios"]}

    def validate_dataset_sources(self) -> tuple[str, ...]:
        return self.datasets.verify_source_hashes(self.root) + self.datasets.verify_source_structures(self.root)

    @staticmethod
    def _default_split(test_id: str) -> str:
        return {
            "T1": "SPLIT_BEST_INNER_TO_OUTER",
            "T2": "SPLIT_BEST_OUTER_TO_INNER",
            "T3": "SPLIT_BEST_TO_GALLEX",
            "T4": "SPLIT_GALLIUM_LEGACY_TO_BEST",
            "T5": "SPLIT_CR51_TO_AR37",
            "T6": "SPLIT_BEST_LORO",
            "T7": "SPLIT_EXPERIMENT_FAMILY_HOLDOUT",
            "T8": "SPLIT_EXPERIMENT_FAMILY_HOLDOUT",
            "T9": "SPLIT_EXPERIMENT_FAMILY_HOLDOUT",
            "T10": "SPLIT_LOEO_BEST",
            "T11": "SPLIT_LOEO_BEST",
            "T12": "UNAUTHORIZED",
        }[test_id]

    @staticmethod
    def _default_covariance(test_id: str) -> str:
        if test_id in {"T8", "T9"}:
            return "COV_PLAUSIBLE_SCAN"
        return "COV_COLLABORATION"

    def plan(
        self,
        test_id: str,
        *,
        split_id: str | None = None,
        covariance_scenario: str | None = None,
        timestamp: str = "PLANNING_ONLY_NOT_EXECUTED",
    ) -> dict[str, object]:
        if test_id not in self.tests:
            raise KeyError(f"Unknown validation test ID: {test_id}")
        test = self.tests[test_id]
        selected_split = split_id or self._default_split(test_id)
        selected_covariance = covariance_scenario or self._default_covariance(test_id)
        if selected_split != "UNAUTHORIZED" and selected_split not in self.splits:
            raise KeyError(f"Unknown validation split ID: {selected_split}")
        if selected_covariance not in self.covariance:
            raise KeyError(f"Unknown covariance scenario ID: {selected_covariance}")

        source_errors = self.validate_dataset_sources()
        dataset_hashes = tuple(
            (dataset_id, self.datasets.by_id[dataset_id].sha256)
            for dataset_id in test.dataset_inputs
        )
        blockers = list(test.blockers)
        blockers.extend(source_errors)
        if not self.covariance[selected_covariance]["available"]:
            blockers.append(f"{selected_covariance}_UNAVAILABLE")
        blockers.extend(("PREDICTION_AUTHORIZED_FALSE", "NUMERICAL_VALIDATION_AUTHORIZED_FALSE"))
        blockers = sorted(set(blockers))

        identity = FrozenModelIdentity.canonical()
        baselines = tuple((model_id, "STEP03_CONTRACT_1.0.0") for model_id in test.baseline_models)
        environment = {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "kernel_package": "lsc-validation-kernel",
        }
        manifest = ValidationExecutionManifest(
            manifest_schema_version="1.0.0",
            test_id=test_id,
            model_identity=identity.as_dict(),
            model_hash=identity.source_manifest_checksum,
            dataset_hashes=dataset_hashes,
            transformation_version="DATASET_CONTRACT_SCHEMA_1.0.0",
            split_id=selected_split,
            baseline_versions=baselines,
            covariance_scenario=selected_covariance,
            nuisance_policy=_canonical_hash(nuisance_parameter_registry()),
            metric=test.test_statistic[0],
            code_commit=_head_commit(self.root),
            environment_hash=_canonical_hash(environment),
            timestamp=timestamp,
            authorization_state="PLANNING_ONLY_BLOCKED",
            prediction_authorized=False,
            numerical_validation_authorized=False,
        )
        return {
            "test": test.as_dict(),
            "datasets": [self.datasets.by_id[item].as_dict() for item in test.dataset_inputs],
            "split": None if selected_split == "UNAUTHORIZED" else self.splits[selected_split],
            "baseline_registry_hash": _canonical_hash(baseline_model_registry()),
            "covariance_scenario": self.covariance[selected_covariance],
            "blockers": blockers,
            "execution_manifest": manifest.as_dict(),
            "dry_run": True,
            "LSC_prediction_performed": False,
            "validation_result_computed": False,
        }
