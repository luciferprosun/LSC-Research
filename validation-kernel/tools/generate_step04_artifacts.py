#!/usr/bin/env python3
"""Generate deterministic Step 04 statistical-control artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator  # noqa: E402
from lsc_kernel.io.manifests import write_json  # noqa: E402
from lsc_kernel.statistics.controls import run_statistical_control_diagnostics  # noqa: E402
from lsc_kernel.statistics.fixtures import run_analytical_fixtures, run_baseline_execution_controls  # noqa: E402
from lsc_kernel.statistics.multiple_testing import (  # noqa: E402
    adjudicated_multiple_testing_policy,
    multiple_testing_dependency_map,
)
from lsc_kernel.statistics.reproduction import reproduce_public_results  # noqa: E402
from lsc_kernel.statistics.result_schema import (  # noqa: E402
    BASELINE_RESULT_JSON_SCHEMA,
    STATISTICAL_EXECUTION_MANIFEST_JSON_SCHEMA,
    StatisticalExecutionManifest,
)
from tools.generate_step03_artifacts import generate as generate_step03  # noqa: E402


def generate(root: Path = ROOT) -> tuple[Path, ...]:
    outputs = list(generate_step03(root))

    def output(relative: str, value: object) -> Path:
        path = root / relative
        write_json(path, value)
        outputs.append(path)
        return path

    fixtures = run_analytical_fixtures()
    baseline_controls = run_baseline_execution_controls(root)
    reproduction = reproduce_public_results(root)
    controls = run_statistical_control_diagnostics(root)
    if not fixtures["passed"] or not baseline_controls["passed"] or not reproduction["passed"] or not controls["passed"]:
        raise RuntimeError("Step 04 control generation failed; refusing to emit a ready status.")

    output("statistics/statistical_fixtures.json", fixtures)
    output("statistics/baseline_execution_controls.json", baseline_controls)
    output("statistics/public_reproduction.json", reproduction)
    output("statistics/statistical_control_diagnostics.json", controls)
    output("statistics/baseline_result.schema.json", BASELINE_RESULT_JSON_SCHEMA)
    output("statistics/statistical_execution_manifest.schema.json", STATISTICAL_EXECUTION_MANIFEST_JSON_SCHEMA)
    output("preregistration/multiple_testing_dependency_map.json", multiple_testing_dependency_map())
    output("preregistration/multiple_testing_policy.json", adjudicated_multiple_testing_policy())
    fixture_manifest = StatisticalExecutionManifest.build(
        repository_root=root,
        dataset_hashes={"NON_PHYSICAL_TEST_FIXTURE": "0" * 64},
        model="M1",
        model_version="STEP04_BASELINE_1.0.0",
        parameters_fitted=("normalization",),
        nuisance_treatment="FIXTURE_NONE",
        covariance_scenario="FIXTURE_DIAGONAL",
        split="FIXTURE_MODEL_SELECTION",
        metric="CHI_SQUARE",
        optimizer="L-BFGS-B",
        classification="NON_PHYSICAL_TEST_FIXTURE",
        timestamp="STEP04_DETERMINISTIC_FIXTURE_NO_WALL_CLOCK",
        code_commit="4553c25205c1c2fcb13c2c97c3a0d1af724a78fe",
    )
    output("statistics/fixture_execution_manifest.json", fixture_manifest.as_dict())
    output(
        "statistics/baseline_benchmark.json",
        {
            "schema_version": "1.0.0",
            "classification": [
                "NON_PHYSICAL_TEST_FIXTURE",
                "PUBLIC_RESULT_REPRODUCTION_ONLY",
                "STATISTICAL_ENGINE_CONTROL",
            ],
            "LSC_used": False,
            "fixtures": {"passed": fixtures["passed"], "count": fixtures["total_count"]},
            "public_reproduction": {"passed": reproduction["passed"], "count": reproduction["total_count"]},
            "baseline_execution_controls": {
                "passed": baseline_controls["passed"],
                "count": baseline_controls["execution_count"],
            },
            "statistical_controls": {
                "passed": controls["passed"],
                "datasets": ["MicroBooNE", "PROSPECT", "STEREO", "IceCube"],
            },
            "six_gallium_interpretation": "SENSITIVITY_ONLY",
            "external_mapping_state": "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING",
            "LSC_prediction_performed": False,
            "LSC_validation_performed": False,
        },
    )
    evaluator = FrozenLSCEvaluator.from_repository(root)
    output("frozen_core/manifests/kernel_status.json", evaluator.status.as_dict())
    return tuple(dict.fromkeys(outputs))


if __name__ == "__main__":
    for generated in generate():
        print(generated.relative_to(ROOT))
