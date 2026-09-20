#!/usr/bin/env python3
"""Generate deterministic Step 03 methodology and preregistration artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator  # noqa: E402
from lsc_kernel.io.hashes import sha256_file  # noqa: E402
from lsc_kernel.io.manifests import write_json  # noqa: E402
from lsc_kernel.validation.best2 import BEST2FuturePredictionContract  # noqa: E402
from lsc_kernel.validation.datasets import canonical_dataset_registry  # noqa: E402
from lsc_kernel.validation.external import canonical_external_mappings  # noqa: E402
from lsc_kernel.validation.policies import NoRefitPolicy  # noqa: E402
from lsc_kernel.validation.registries import (  # noqa: E402
    GalliumCrossSectionModelRegistry,
    baseline_model_registry,
    covariance_scenario_registry,
    falsification_registry,
    metric_registry,
    multiple_testing_policy,
    nuisance_parameter_registry,
    split_registry,
    validation_test_registry,
)
from lsc_kernel.validation.results import VALIDATION_RESULT_JSON_SCHEMA  # noqa: E402


DATASET_CONTRACT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ValidationDatasetRegistry",
    "type": "object",
    "required": ["schema_version", "source_of_truth", "datasets"],
    "properties": {
        "schema_version": {"const": "1.0.0"},
        "source_of_truth": {"const": "ValidationDatasetRegistry"},
        "datasets": {
            "type": "array",
            "minItems": 13,
            "items": {
                "type": "object",
                "properties": {
                    "dataset_id": {"type": "string"},
                    "experiment": {"type": "string"},
                    "source_dois": {"type": "array", "items": {"type": "string"}},
                    "source_reference": {"type": "string"},
                    "local_path": {"type": "string", "pattern": "^(?!/)(?!.*\\.\\.).+$"},
                    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    "version": {"type": "string"},
                    "quality_grade": {"enum": ["A", "B", "C", "D", "E"]},
                    "raw_or_derived": {"type": "string"},
                    "number_of_objects": {"type": "integer", "minimum": 0},
                    "count_semantics": {"type": "string"},
                    "available_observables": {"type": "array", "items": {"type": "string"}},
                    "uncertainties": {"type": "array", "items": {"type": "string"}},
                    "covariance_availability": {"type": "string"},
                    "timing_resolution": {"type": "string"},
                    "geometry_availability": {"type": "string"},
                    "orientation_availability": {"type": "string"},
                    "validation_role": {"type": "string"},
                    "allowed_tests": {"type": "array", "items": {"type": "string"}},
                    "prohibited_tests": {"type": "array", "items": {"type": "string"}},
                    "known_limitations": {"type": "array", "items": {"type": "string"}},
                    "provenance_status": {"type": "string"},
                    "exposure_classification": {"enum": ["MODEL_PREEXISTING", "MODEL_EXPOSED", "POST_DATA_MODEL_CHANGE", "UNKNOWN_EXPOSURE"]},
                    "blindness_level": {"enum": ["BLIND_STRICT", "BLIND_PARTIAL", "NON_BLIND_HISTORICAL", "FUTURE_BLIND"]},
                    "contract": {"type": "object"},
                },
                "required": [
                    "dataset_id", "experiment", "source_dois", "source_reference", "local_path", "sha256",
                    "version", "quality_grade", "raw_or_derived", "number_of_objects", "count_semantics", "available_observables",
                    "uncertainties", "covariance_availability", "timing_resolution", "geometry_availability",
                    "orientation_availability", "validation_role", "allowed_tests", "prohibited_tests",
                    "known_limitations", "provenance_status", "exposure_classification", "blindness_level", "contract",
                ],
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


EXECUTION_MANIFEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ValidationExecutionManifest",
    "type": "object",
    "required": [
        "manifest_schema_version", "test_id", "model_identity", "model_hash", "dataset_hashes",
        "transformation_version", "split_id", "baseline_versions", "covariance_scenario", "nuisance_policy",
        "metric", "code_commit", "environment_hash", "timestamp", "authorization_state",
        "prediction_authorized", "numerical_validation_authorized", "execution_manifest_hash",
    ],
    "properties": {
        "prediction_authorized": {"const": False},
        "numerical_validation_authorized": {"const": False},
    },
}


def generate(root: Path = ROOT) -> tuple[Path, ...]:
    outputs: list[Path] = []

    def output(relative: str, value: object) -> Path:
        path = root / relative
        write_json(path, value)
        outputs.append(path)
        return path

    datasets_path = output("preregistration/validation_datasets.json", canonical_dataset_registry().as_dict())
    output(
        "preregistration/datasets.json",
        {
            "schema_version": "1.0.0",
            "$ref": "validation_datasets.json",
            "sha256": sha256_file(datasets_path),
            "note": "Checksum-bound alias; validation_datasets.json is the sole machine-readable dataset source of truth.",
        },
    )
    output(
        "preregistration/tests.json",
        {"schema_version": "1.0.0", "tests": [test.as_dict() for test in validation_test_registry()]},
    )
    output("preregistration/splits.json", split_registry())
    output("preregistration/covariance_scenarios.json", covariance_scenario_registry())
    output("preregistration/baseline_models.json", baseline_model_registry())
    output("preregistration/nuisance_registry.json", nuisance_parameter_registry())
    output("preregistration/falsification_rules.json", falsification_registry())
    output("preregistration/metric_registry.json", metric_registry())
    output("preregistration/multiple_testing_policy.json", multiple_testing_policy())
    output("preregistration/no_refit_policy.json", NoRefitPolicy().as_dict())
    output(
        "preregistration/external_constraints.json",
        {
            "schema_version": "1.0.0",
            "automatic_likelihood_multiplication": False,
            "mappings": [mapping.as_dict() for mapping in canonical_external_mappings()],
        },
    )
    output("preregistration/best2_future_contract.json", BEST2FuturePredictionContract().as_dict())
    output(
        "preregistration/gallium_cross_section_models.json",
        GalliumCrossSectionModelRegistry.from_repository(root).as_dict(),
    )
    output("preregistration/dataset_contract.schema.json", DATASET_CONTRACT_SCHEMA)
    output("preregistration/validation_execution_manifest.schema.json", EXECUTION_MANIFEST_SCHEMA)
    output("preregistration/validation_result.schema.json", VALIDATION_RESULT_JSON_SCHEMA)

    evaluator = FrozenLSCEvaluator.from_repository(root)
    output("frozen_core/manifests/kernel_status.json", evaluator.status.as_dict())
    output(
        "frozen_core/manifests/validation_interfaces.json",
        {"schema_version": "1.0.0", "tests": [test.as_dict() for test in validation_test_registry()]},
    )
    return tuple(outputs)


if __name__ == "__main__":
    for generated in generate():
        print(generated.relative_to(ROOT))
