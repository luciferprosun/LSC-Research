"""Canonical, value-free schema for the recovered LSC parameter structures."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class FrozenParameterDefinition:
    canonical_name: str
    symbol: str
    description: str
    value_type: str
    dimensions: str
    units: str
    unit_status: str
    frame: str
    frame_status: str
    required: bool
    frozen_status: str
    structure_provenance_status: str
    provenance_source: str
    confidence: str
    missing_reason: str
    required_for_executable_evaluation: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _definition(
    name: str,
    symbol: str,
    description: str,
    value_type: str,
    dimensions: str,
    source: str,
    missing_reason: str,
    *,
    units: str = "UNKNOWN",
    unit_status: str = "MISSING_FROZEN_UNIT",
    frame: str = "NOT_APPLICABLE",
    frame_status: str = "NOT_APPLICABLE",
    required: bool = True,
    evaluation: bool = True,
) -> FrozenParameterDefinition:
    return FrozenParameterDefinition(
        canonical_name=name,
        symbol=symbol,
        description=description,
        value_type=value_type,
        dimensions=dimensions,
        units=units,
        unit_status=unit_status,
        frame=frame,
        frame_status=frame_status,
        required=required,
        frozen_status="MISSING",
        structure_provenance_status="AUTHENTIC_FROZEN",
        provenance_source=source,
        confidence="HIGH",
        missing_reason=missing_reason,
        required_for_executable_evaluation=evaluation,
    )


@dataclass(frozen=True, slots=True)
class FrozenParameterSchema:
    schema_version: str
    definitions: tuple[FrozenParameterDefinition, ...]

    @classmethod
    def canonical(cls) -> "FrozenParameterSchema":
        canonical = "canonical-parameter-structures"
        return cls(
            schema_version="1.0.0",
            definitions=(
                _definition(
                    "theta",
                    "theta",
                    "Complete ordered LSC and nuisance-parameter vector.",
                    "vector",
                    "UNKNOWN_LENGTH",
                    "missing-full-theta",
                    "No complete numerical vector or authoritative serialization was recovered.",
                ),
                _definition(
                    "parameter_ordering",
                    "order(theta)",
                    "Canonical serialization order for theta.",
                    "ordered_names",
                    "UNKNOWN_LENGTH",
                    "missing-parameter-ordering",
                    "No authoritative ordered vector or checkpoint layout was recovered.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                    evaluation=True,
                ),
                _definition(
                    "lambda0",
                    "lambda0",
                    "Scalar trace-response amplitude in E2 and E7.",
                    "scalar",
                    "SCALAR",
                    "missing-lambda0",
                    "The symbol is frozen, but its numerical value and unit normalization are not.",
                ),
                _definition(
                    "lambdaA",
                    "lambdaA",
                    "Anisotropic response amplitude in E2 and E7.",
                    "scalar",
                    "SCALAR",
                    "missing-lambdaA",
                    "The symbol is frozen, but its numerical value and unit normalization are not.",
                ),
                _definition(
                    "f0_a",
                    "f0_a(E,t)",
                    "Scalar response template for analysis bin or zone a.",
                    "function",
                    "INPUTS(E,t)_OUTPUT_UNKNOWN",
                    "missing-f0-a",
                    "The freeze boundary explicitly says the exact functional form is not frozen.",
                ),
                _definition(
                    "fA_a",
                    "fA_a(E,t)",
                    "Anisotropic response template for analysis bin or zone a.",
                    "function",
                    "INPUTS(E,t)_OUTPUT_UNKNOWN",
                    "missing-fA-a",
                    "The freeze boundary explicitly says the exact functional form is not frozen.",
                ),
                _definition(
                    "active_anisotropy_tensor",
                    "A_a^{ij}",
                    "Symmetric traceless anisotropy tensor for bin or detector zone a.",
                    "rank_2_tensor",
                    "SQUARE_UNKNOWN_SIZE",
                    "missing-active-tensor-components",
                    "No version-safe active components were recovered.",
                    frame="COMPATIBLE_WITH_n_lab",
                    frame_status="MISSING_FROZEN_FRAME",
                ),
                _definition(
                    "tensor_orientation",
                    "orientation(A_a^{ij})",
                    "Frozen physical orientation of the active tensor.",
                    "orientation",
                    "UNKNOWN_REPRESENTATION",
                    "missing-tensor-orientation",
                    "No direction, Euler angles, rotation, or equivalent frozen object was recovered.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                    frame="UNKNOWN",
                    frame_status="MISSING_FROZEN_FRAME",
                ),
                _definition(
                    "complete_reference_frame",
                    "frame",
                    "Complete frame definitions and transformations required by E3, E11, and E12.",
                    "frame_contract",
                    "NOT_APPLICABLE",
                    "missing-coordinate-frame",
                    "ICRS and lab names are symbolic; the complete transform metadata are absent.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                    frame="UNKNOWN",
                    frame_status="MISSING_FROZEN_FRAME",
                ),
                _definition(
                    "eta",
                    "eta",
                    "Nuisance parameters for source, cross-section, geometry, extraction, and normalization.",
                    "structured_vector",
                    "UNKNOWN_LENGTH",
                    canonical,
                    "Roles are frozen, but an ordered numerical nuisance contract and bounds are absent.",
                ),
                _definition(
                    "covariance",
                    "C",
                    "Statistical and systematic covariance matrix used by E10.",
                    "square_matrix",
                    "SQUARE_UNKNOWN_SIZE",
                    canonical,
                    "The full covariance object and its unit convention are not frozen.",
                ),
                _definition(
                    "numerical_configuration",
                    "config",
                    "Configuration binding equations, values, conventions, and normalization order.",
                    "object",
                    "NOT_APPLICABLE",
                    "missing-frozen-numeric-config",
                    "No complete frozen numerical configuration was recovered.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                ),
                _definition(
                    "parameter_bounds",
                    "bounds(theta,eta)",
                    "Final frozen parameter priors or bounds.",
                    "object",
                    "NOT_APPLICABLE",
                    "missing-final-bounds",
                    "The freeze boundary explicitly classifies final bounds as not frozen.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                ),
                _definition(
                    "numerical_defaults",
                    "numerical_defaults",
                    "Integration, boundary, quadrature, and normalization defaults and order.",
                    "object",
                    "NOT_APPLICABLE",
                    "missing-numerical-defaults",
                    "The symbolic integrals have no complete executable numerical contract.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                ),
                _definition(
                    "frozen_prediction_table",
                    "R_pred",
                    "Authentic precomputed prediction table usable without fitting.",
                    "table",
                    "UNKNOWN",
                    "missing-frozen-prediction-table",
                    "Existing tables are post-data, fitted, or unrelated.",
                ),
                _definition(
                    "executable_evaluator_inputs",
                    "inputs(E1-E12)",
                    "Complete observations, geometry, exposure, and transformation inputs.",
                    "object",
                    "NOT_APPLICABLE",
                    "missing-e1-e12-evaluator",
                    "No machine-executable E1-E12 input contract was frozen.",
                    units="NOT_APPLICABLE",
                    unit_status="NOT_APPLICABLE",
                ),
            ),
        )

    @property
    def by_name(self) -> dict[str, FrozenParameterDefinition]:
        return {definition.canonical_name: definition for definition in self.definitions}

    @property
    def required_names(self) -> tuple[str, ...]:
        return tuple(definition.canonical_name for definition in self.definitions if definition.required)

    @property
    def numerical_blockers(self) -> tuple[FrozenParameterDefinition, ...]:
        return tuple(
            definition
            for definition in self.definitions
            if definition.required_for_executable_evaluation and definition.frozen_status != "AUTHENTIC_FROZEN"
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "definitions": [definition.as_dict() for definition in self.definitions],
        }
