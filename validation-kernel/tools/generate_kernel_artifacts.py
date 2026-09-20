#!/usr/bin/env python3
"""Generate deterministic Step 02 machine-readable artifacts from kernel code."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lsc_kernel.frozen.dependency_graph import graph_as_dict, graph_as_dot, graph_as_markdown  # noqa: E402
from lsc_kernel.frozen.equations import equation_descriptors  # noqa: E402
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator  # noqa: E402
from lsc_kernel.frozen.frames import FRAME_DEFINITIONS  # noqa: E402
from lsc_kernel.frozen.identity import FrozenModelIdentity  # noqa: E402
from lsc_kernel.frozen.parameter_bundle import parameter_bundle_json_schema  # noqa: E402
from lsc_kernel.frozen.tensor import TensorContract  # noqa: E402
from lsc_kernel.io.manifests import write_json  # noqa: E402
from lsc_kernel.validation.contracts import validation_test_definitions  # noqa: E402


def quarantine_manifest(evaluator: FrozenLSCEvaluator) -> dict[str, object]:
    rows = []
    for record in evaluator.provenance.records:
        if record.classification.value not in {"HISTORICAL_POST_DATA", "UNVERIFIED"}:
            continue
        conflict = "UNVERIFIED_CONFLICT" if record.artifact_id.startswith("unverified-") else None
        rows.append(
            {
                "artifact_id": record.artifact_id,
                "artifact_type": record.artifact_type,
                "classification": record.classification.value,
                "conflict_status": conflict,
                "data_exposure_status": record.data_exposure_status,
                "sha256": record.sha256,
                "source_path": record.source_path,
                "forbidden_as": "FROZEN_6_3_0_NUMERICAL_INPUT",
                "notes": record.notes,
            }
        )
    return {
        "schema_version": "1.0.0",
        "policy": "Quarantined artifacts remain evidence and may never be promoted into the frozen 6.3.0 numerical bundle.",
        "artifacts": rows,
    }


def missing_manifest(evaluator: FrozenLSCEvaluator) -> dict[str, object]:
    missing = []
    for definition in evaluator.schema.numerical_blockers:
        missing.append(
            {
                "object": definition.canonical_name,
                "symbol": definition.symbol,
                "status": definition.frozen_status,
                "source": definition.provenance_source,
                "reason": definition.missing_reason,
                "blocks_executable_evaluation": definition.required_for_executable_evaluation,
            }
        )
    return {
        "schema_version": "1.0.0",
        "model_identity": evaluator.identity.as_dict(),
        "provenance_registry_sha256": evaluator.identity.provenance_registry_checksum,
        "count": len(missing),
        "missing": missing,
        "t12_additional_metadata_blockers": [
            "precise_timing",
            "surveyed_orientation",
            "sufficient_geometry",
            "required_reference_frames",
        ],
    }


def generate(root: Path = ROOT) -> tuple[Path, ...]:
    evaluator = FrozenLSCEvaluator.from_repository(root)
    outputs: list[Path] = []

    def output(relative: str, value: object) -> None:
        path = root / relative
        write_json(path, value)
        outputs.append(path)

    output("frozen_core/manifests/frozen_model_identity.json", FrozenModelIdentity.canonical().as_dict())
    output("frozen_core/manifests/kernel_status.json", evaluator.status.as_dict())
    output("frozen_core/manifests/HISTORICAL_ARTIFACT_QUARANTINE.json", quarantine_manifest(evaluator))
    output(
        "frozen_core/manifests/validation_interfaces.json",
        {"tests": [definition.as_dict() for definition in validation_test_definitions()]},
    )
    output(
        "frozen_core/parameters/frozen_parameter_schema.json",
        evaluator.schema.as_dict(),
    )
    output(
        "frozen_core/parameters/frozen_parameter_bundle.schema.json",
        parameter_bundle_json_schema(evaluator.schema),
    )
    output(
        "frozen_core/parameters/frozen_missing_parameters.json",
        missing_manifest(evaluator),
    )
    output(
        "frozen_core/parameters/frame_contract.json",
        {"frames": [frame.as_dict() for frame in FRAME_DEFINITIONS], "complete": False},
    )
    output(
        "frozen_core/parameters/tensor_contract.json",
        {"contract": TensorContract().as_dict(), "active_components_available": False},
    )
    output(
        "frozen_core/parameters/unit_contract.json",
        {
            "complete": False,
            "parameters": [
                {
                    "canonical_name": item.canonical_name,
                    "units": item.units,
                    "unit_status": item.unit_status,
                }
                for item in evaluator.schema.definitions
            ],
        },
    )
    output(
        "frozen_core/equations/equations.json",
        {"schema_version": "1.0.0", "equations": [item.as_dict() for item in equation_descriptors()]},
    )
    output("frozen_core/equations/equation_dependency_graph.json", graph_as_dict())
    markdown = root / "frozen_core/equations/equation_dependency_graph.md"
    markdown.write_text(graph_as_markdown(), encoding="utf-8")
    outputs.append(markdown)
    dot = root / "frozen_core/equations/equation_dependency_graph.dot"
    dot.write_text(graph_as_dot(), encoding="utf-8")
    outputs.append(dot)
    return tuple(outputs)


if __name__ == "__main__":
    for generated in generate():
        print(generated.relative_to(ROOT))
