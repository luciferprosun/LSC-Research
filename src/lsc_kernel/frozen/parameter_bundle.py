"""Frozen parameter bundle serialization, hashing, and fail-closed validation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from numbers import Real
from pathlib import Path
from typing import Any, Mapping, Sequence

from lsc_kernel.errors import FrozenParameterMissing, FrozenTensorIncomplete, MalformedBundle
from lsc_kernel.frozen.frames import FrameRequirement
from lsc_kernel.frozen.identity import FrozenModelIdentity, validate_identity
from lsc_kernel.frozen.parameter_schema import FrozenParameterDefinition, FrozenParameterSchema
from lsc_kernel.frozen.provenance import ProvenancePolicy
from lsc_kernel.frozen.tensor import TensorContract
from lsc_kernel.frozen.units import UnitRequirement


TOP_LEVEL_FIELDS = frozenset(
    {
        "bundle_schema_version",
        "model_identity",
        "parameters",
        "unit_definitions",
        "frame_definitions",
        "tensor_definitions",
        "source_references",
        "provenance_state",
        "bundle_sha256",
    }
)
PARAMETER_FIELDS = frozenset({"value", "units", "frame", "dimensions", "provenance"})
PROVENANCE_FIELDS = frozenset({"artifact_id", "classification", "sha256"})


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def compute_bundle_hash(bundle: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in bundle.items() if key != "bundle_sha256"}
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


@dataclass(frozen=True, slots=True)
class FrozenParameterBundle:
    bundle_schema_version: str
    model_identity: Mapping[str, Any]
    parameters: Mapping[str, Mapping[str, Any]]
    unit_definitions: Mapping[str, Any]
    frame_definitions: Mapping[str, Any]
    tensor_definitions: Mapping[str, Any]
    source_references: tuple[str, ...]
    provenance_state: str
    bundle_sha256: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrozenParameterBundle":
        unknown = sorted(set(value) - TOP_LEVEL_FIELDS)
        missing = sorted(TOP_LEVEL_FIELDS - set(value))
        if unknown or missing:
            raise MalformedBundle(
                "Frozen parameter bundle has an invalid top-level contract.",
                details={"unknown_fields": unknown, "missing_fields": missing},
            )
        if not isinstance(value.get("model_identity"), Mapping):
            raise MalformedBundle("model_identity must be a JSON object.")
        if not isinstance(value.get("parameters"), Mapping):
            raise MalformedBundle("parameters must be a JSON object.")
        for field in ("unit_definitions", "frame_definitions", "tensor_definitions"):
            if not isinstance(value.get(field), Mapping):
                raise MalformedBundle(f"{field} must be a JSON object.")
        if not isinstance(value.get("source_references"), list) or not all(
            isinstance(item, str) for item in value.get("source_references", [])
        ):
            raise MalformedBundle("source_references must be an array of strings.")
        try:
            return cls(
                bundle_schema_version=str(value["bundle_schema_version"]),
                model_identity=value["model_identity"],
                parameters=value["parameters"],
                unit_definitions=value["unit_definitions"],
                frame_definitions=value["frame_definitions"],
                tensor_definitions=value["tensor_definitions"],
                source_references=tuple(value["source_references"]),
                provenance_state=str(value["provenance_state"]),
                bundle_sha256=str(value["bundle_sha256"]),
            )
        except (KeyError, TypeError) as exc:
            raise MalformedBundle("Frozen parameter bundle contains malformed field types.") from exc

    @classmethod
    def load(cls, path: Path | str) -> "FrozenParameterBundle":
        try:
            value = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MalformedBundle("Parameter bundle is not readable JSON.") from exc
        if not isinstance(value, Mapping):
            raise MalformedBundle("Parameter bundle root must be a JSON object.")
        return cls.from_mapping(value)

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["source_references"] = list(self.source_references)
        return result


def _dimensions(value: object) -> list[int]:
    if isinstance(value, bool):
        return []
    if isinstance(value, Real):
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        rows = list(value)
        if rows and all(isinstance(row, Sequence) and not isinstance(row, (str, bytes)) for row in rows):
            widths = {len(row) for row in rows}
            if len(widths) != 1:
                raise FrozenTensorIncomplete("Nested parameter arrays must be rectangular.")
            return [len(rows), widths.pop()]
        return [len(rows)]
    return []


def _validate_dimensions(definition: FrozenParameterDefinition, entry: Mapping[str, Any]) -> None:
    declared = entry.get("dimensions")
    actual = _dimensions(entry.get("value"))
    if declared != actual:
        raise FrozenTensorIncomplete(
            f"Declared dimensions do not match the value for {definition.canonical_name!r}.",
            details={"declared": declared, "actual": actual},
        )
    if definition.value_type == "scalar" and actual != []:
        raise FrozenTensorIncomplete(f"{definition.canonical_name!r} must be scalar.")
    if definition.value_type == "rank_2_tensor":
        TensorContract().validate_structure(entry.get("value"))
    if definition.value_type == "square_matrix":
        value = entry.get("value")
        if len(actual) != 2 or actual[0] != actual[1]:
            raise FrozenTensorIncomplete(f"{definition.canonical_name!r} must be a square matrix.")


def validate_parameter_bundle(
    bundle: FrozenParameterBundle | Mapping[str, Any],
    *,
    provenance: ProvenancePolicy,
    schema: FrozenParameterSchema | None = None,
    identity: FrozenModelIdentity | None = None,
) -> FrozenParameterBundle:
    """Validate the complete bundle and reject every unresolved frozen contract."""

    schema = schema or FrozenParameterSchema.canonical()
    identity = identity or FrozenModelIdentity.canonical()
    resolved = bundle if isinstance(bundle, FrozenParameterBundle) else FrozenParameterBundle.from_mapping(bundle)
    if resolved.bundle_schema_version != schema.schema_version:
        raise MalformedBundle(
            "Parameter bundle schema version mismatch.",
            details={"expected": schema.schema_version, "actual": resolved.bundle_schema_version},
        )
    validate_identity(resolved.model_identity, identity)
    if resolved.provenance_state != "AUTHENTIC_FROZEN":
        raise MalformedBundle(
            "A frozen parameter bundle must declare AUTHENTIC_FROZEN provenance state.",
            details={"actual": resolved.provenance_state},
        )
    actual_hash = compute_bundle_hash(resolved.as_dict())
    if resolved.bundle_sha256 != actual_hash:
        raise MalformedBundle(
            "Parameter bundle SHA-256 mismatch.",
            details={"expected": actual_hash, "actual": resolved.bundle_sha256},
        )
    unknown_parameters = sorted(set(resolved.parameters) - set(schema.by_name))
    missing_parameters = sorted(set(schema.required_names) - set(resolved.parameters))
    if unknown_parameters:
        raise MalformedBundle(
            "Bundle contains unknown critical parameter fields.",
            details={"unknown_parameters": unknown_parameters},
        )
    if missing_parameters:
        raise FrozenParameterMissing(
            "Required authentic frozen parameters are missing.",
            details={"missing_parameters": missing_parameters},
        )
    for name in schema.required_names:
        definition = schema.by_name[name]
        entry = resolved.parameters[name]
        unknown_fields = sorted(set(entry) - PARAMETER_FIELDS)
        missing_fields = sorted(PARAMETER_FIELDS - set(entry))
        if unknown_fields or missing_fields:
            raise MalformedBundle(
                f"Invalid parameter entry contract for {name!r}.",
                details={"unknown_fields": unknown_fields, "missing_fields": missing_fields},
            )
        provenance_claim = entry["provenance"]
        if not isinstance(provenance_claim, Mapping):
            raise MalformedBundle(f"Provenance for {name!r} must be an object.")
        if set(provenance_claim) != PROVENANCE_FIELDS:
            raise MalformedBundle(
                f"Provenance contract for {name!r} is malformed.",
                details={"required_fields": sorted(PROVENANCE_FIELDS)},
            )
        provenance.admit_numerical(
            str(provenance_claim["artifact_id"]),
            claimed_classification=str(provenance_claim["classification"]),
            claimed_sha256=str(provenance_claim["sha256"]),
        )
        if str(provenance_claim["artifact_id"]) not in resolved.source_references:
            raise MalformedBundle(
                f"Parameter source for {name!r} is absent from source_references.",
                details={"artifact_id": provenance_claim["artifact_id"]},
            )
        _validate_dimensions(definition, entry)
        UnitRequirement(name, definition.units, definition.unit_status).validate(entry.get("units"))
        FrameRequirement(name, definition.frame, definition.frame_status).validate(entry.get("frame"))
        if name == "active_anisotropy_tensor":
            TensorContract().require_orientation(resolved.parameters["tensor_orientation"].get("value"))
    return resolved


def parameter_bundle_json_schema(schema: FrozenParameterSchema | None = None) -> dict[str, Any]:
    schema = schema or FrozenParameterSchema.canonical()
    identity = FrozenModelIdentity.canonical().as_dict()
    parameter_names = list(schema.required_names)
    parameter_entry = {
        "type": "object",
        "additionalProperties": False,
        "required": sorted(PARAMETER_FIELDS),
        "properties": {
            "value": {},
            "units": {"type": ["string", "null"]},
            "frame": {"type": ["string", "null"]},
            "dimensions": {"type": "array", "items": {"type": "integer", "minimum": 0}},
            "provenance": {
                "type": "object",
                "additionalProperties": False,
                "required": sorted(PROVENANCE_FIELDS),
                "properties": {
                    "artifact_id": {"type": "string"},
                    "classification": {"const": "AUTHENTIC_FROZEN"},
                    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                },
            },
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:lsc-validation-kernel:frozen-parameter-bundle:1.0.0",
        "title": "FrozenParameterBundle",
        "$defs": {"parameterEntry": parameter_entry},
        "type": "object",
        "additionalProperties": False,
        "required": sorted(TOP_LEVEL_FIELDS),
        "properties": {
            "bundle_schema_version": {"const": schema.schema_version},
            "model_identity": {
                "type": "object",
                "additionalProperties": False,
                "required": sorted(identity),
                "properties": {name: {"const": value} for name, value in identity.items()},
            },
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "required": parameter_names,
                "properties": {
                    name: {"$ref": "#/$defs/parameterEntry"} for name in parameter_names
                },
            },
            "unit_definitions": {"type": "object"},
            "frame_definitions": {"type": "object"},
            "tensor_definitions": {"type": "object"},
            "source_references": {"type": "array", "items": {"type": "string"}},
            "provenance_state": {"const": "AUTHENTIC_FROZEN"},
            "bundle_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }
