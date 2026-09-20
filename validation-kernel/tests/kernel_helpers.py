from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lsc_kernel.frozen.identity import FrozenModelIdentity  # noqa: E402
from lsc_kernel.frozen.parameter_bundle import compute_bundle_hash  # noqa: E402
from lsc_kernel.frozen.parameter_schema import (  # noqa: E402
    FrozenParameterDefinition,
    FrozenParameterSchema,
)
from lsc_kernel.frozen.provenance import ProvenancePolicy, ProvenanceRecord  # noqa: E402
from lsc_kernel.status import ProvenanceClassification  # noqa: E402


FIXTURE_SHA256 = "a" * 64


def repository_policy() -> ProvenancePolicy:
    return ProvenancePolicy.from_csv(ROOT / "docs" / "provenance" / "FROZEN_PROVENANCE_REGISTRY.csv")


def authentic_parameter_record(artifact_id: str = "NON_PHYSICAL_TEST_FIXTURE") -> ProvenanceRecord:
    return ProvenanceRecord(
        artifact_id=artifact_id,
        artifact_type="parameter",
        parameter_or_role="software validation fixture",
        value_or_summary="NON_PHYSICAL_TEST_FIXTURE",
        units="DIMENSIONLESS",
        source_path="tests/fixtures/NON_PHYSICAL_TEST_FIXTURE.json",
        git_commit="TEST_ONLY",
        git_tag="NOT_TAGGED",
        timestamp_if_known="TEST_ONLY",
        sha256=FIXTURE_SHA256,
        data_exposure_status="TEST_ONLY",
        classification=ProvenanceClassification.AUTHENTIC_FROZEN,
        confidence="TEST_ONLY",
        notes="Software contract fixture; never a scientific LSC value.",
    )


def fixture_policy(artifact_id: str = "NON_PHYSICAL_TEST_FIXTURE") -> ProvenancePolicy:
    return ProvenancePolicy([authentic_parameter_record(artifact_id)])


def single_parameter_schema(
    *,
    name: str = "lambda0",
    value_type: str = "scalar",
    dimensions: str = "SCALAR",
    unit_status: str = "AUTHENTIC_FROZEN_UNIT",
    units: str = "DIMENSIONLESS",
    frame_status: str = "NOT_APPLICABLE",
    frame: str = "NOT_APPLICABLE",
) -> FrozenParameterSchema:
    original = FrozenParameterSchema.canonical().by_name["lambda0"]
    definition: FrozenParameterDefinition = replace(
        original,
        canonical_name=name,
        value_type=value_type,
        dimensions=dimensions,
        unit_status=unit_status,
        units=units,
        frame_status=frame_status,
        frame=frame,
        frozen_status="AUTHENTIC_FROZEN",
        provenance_source="NON_PHYSICAL_TEST_FIXTURE",
        missing_reason="",
    )
    return FrozenParameterSchema("1.0.0", (definition,))


def bundle_mapping(
    parameters: dict[str, dict[str, Any]],
    *,
    identity: dict[str, Any] | None = None,
    schema_version: str = "1.0.0",
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "bundle_schema_version": schema_version,
        "model_identity": identity or FrozenModelIdentity.canonical().as_dict(),
        "parameters": parameters,
        "unit_definitions": {},
        "frame_definitions": {},
        "tensor_definitions": {},
        "source_references": ["NON_PHYSICAL_TEST_FIXTURE"],
        "provenance_state": "AUTHENTIC_FROZEN",
        "bundle_sha256": "",
    }
    value["bundle_sha256"] = compute_bundle_hash(value)
    return value


def parameter_entry(
    *,
    value: Any = 1.0,
    dimensions: list[int] | None = None,
    artifact_id: str = "NON_PHYSICAL_TEST_FIXTURE",
    classification: str = "AUTHENTIC_FROZEN",
    sha256: str = FIXTURE_SHA256,
    units: str | None = "DIMENSIONLESS",
    frame: str | None = "NOT_APPLICABLE",
) -> dict[str, Any]:
    return {
        "value": value,
        "units": units,
        "frame": frame,
        "dimensions": [] if dimensions is None else dimensions,
        "provenance": {
            "artifact_id": artifact_id,
            "classification": classification,
            "sha256": sha256,
        },
    }
