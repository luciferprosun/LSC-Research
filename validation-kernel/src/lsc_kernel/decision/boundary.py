"""Fail-closed Step 06 decision policy.

This module preserves the historical 6.3.0 identity and defines the boundary
for a future executable successor.  It contains no physical parameter values,
fit, prediction, validation result, or BEST-2 prediction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Mapping

from lsc_kernel.errors import (
    BlindnessLabelRejected,
    HistoricalIdentityReassignmentRejected,
    PublicationBoundaryViolation,
    PublicClaimNotAuthorized,
    SuccessorClassificationError,
)


HISTORICAL_VERSION = "6.3.0-pre-BEST2-freeze-update"
HISTORICAL_COMMIT = "6ffa07bdde533fcc2a550e36c762b8edd9236c47"
HISTORICAL_FREEZE_COMMIT = "a6d582694d55fa0260ef7ab07ed83fd06feef607"
HISTORICAL_VERSION_DOI = "10.5281/zenodo.20377427"
HISTORICAL_CONCEPT_DOI = "10.5281/zenodo.19780615"
SYMBOLIC_EQUATION_SHA256 = "af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981"
STEP06_VERDICT = "LSC_6_3_0_NUMERICALLY_UNRECOVERABLE_SUCCESSOR_BOUNDARY_DEFINED"


class RecoverabilityVerdict(StrEnum):
    FULLY_RECOVERABLE = "FULLY_RECOVERABLE"
    PARTIALLY_RECOVERABLE = "PARTIALLY_RECOVERABLE"
    NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE = (
        "NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE"
    )


class SuccessorContentClass(StrEnum):
    UNCHANGED_FROM_6_3_0_AUTHENTIC = "UNCHANGED_FROM_6_3_0_AUTHENTIC"
    FORMALIZED_FROM_6_3_0 = "FORMALIZED_FROM_6_3_0"
    NEW_NUMERICAL_SPECIFICATION_6_3_1 = "NEW_NUMERICAL_SPECIFICATION_6_3_1"
    NEW_METHOD_6_3_1 = "NEW_METHOD_6_3_1"
    HISTORICAL_REFERENCE_ONLY = "HISTORICAL_REFERENCE_ONLY"
    UNRESOLVED = "UNRESOLVED"


class PublicationReadinessLevel(StrEnum):
    P0_HISTORICAL_PRESERVATION_READY = "P0_HISTORICAL_PRESERVATION_READY"
    P1_SPECIFICATION_BOUNDARY_READY = "P1_SPECIFICATION_BOUNDARY_READY"
    P2_EXECUTABLE_SUCCESSOR_READY = "P2_EXECUTABLE_SUCCESSOR_READY"
    P3_RELEASE_PACKAGE_READY = "P3_RELEASE_PACKAGE_READY"
    P4_RETROSPECTIVE_VALIDATION_READY = "P4_RETROSPECTIVE_VALIDATION_READY"
    P5_PROSPECTIVE_PREDICTION_READY = "P5_PROSPECTIVE_PREDICTION_READY"


@dataclass(frozen=True, slots=True)
class PublicClaimRecord:
    claim_id: str
    claim: str
    status: str
    reason: str
    evidence: str
    allowed_in_publication: bool

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def recoverability_decision() -> dict[str, object]:
    """Return the evidence-derived Step 06 recoverability decision."""

    return {
        "schema_version": "1.0.0",
        "decision_date": "2026-08-16",
        "identity_recoverability": RecoverabilityVerdict.FULLY_RECOVERABLE.value,
        "symbolic_recoverability": RecoverabilityVerdict.FULLY_RECOVERABLE.value,
        "numerical_recoverability": (
            RecoverabilityVerdict.NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE.value
        ),
        "overall_recoverability": (
            RecoverabilityVerdict.NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE.value
        ),
        "historical_identity": {
            "version": HISTORICAL_VERSION,
            "commit": HISTORICAL_COMMIT,
            "freeze_commit": HISTORICAL_FREEZE_COMMIT,
            "version_doi": HISTORICAL_VERSION_DOI,
            "concept_doi": HISTORICAL_CONCEPT_DOI,
        },
        "symbolic_equation_set": {
            "identity": f"LSC-E1-E12@sha256:{SYMBOLIC_EQUATION_SHA256}",
            "status": "RECOVERED_SYMBOLIC_ONLY",
        },
        "questions": {
            "Q1_historical_identity_recovered": True,
            "Q2_symbolic_E1_E12_recovered": True,
            "Q3_complete_numerical_state_recovered": False,
            "Q4_numerically_executable_without_new_decisions": False,
            "Q5_exact_frozen_validation_possible": False,
            "Q6_honest_completion_without_new_version": False,
        },
        "scientific_state": {
            "MODEL_FALSIFIED": False,
            "MODEL_NOT_NUMERICALLY_RECOVERABLE": True,
            "TEST_BLOCKED": True,
            "interpretation": (
                "Missing executable provenance is a reproducibility failure, not evidence "
                "that the physical model is falsified."
            ),
        },
        "decision_verdict": STEP06_VERDICT,
    }


def allowed_claim_records() -> tuple[PublicClaimRecord, ...]:
    """Canonical public-claim boundary for historical 6.3.0."""

    return (
        PublicClaimRecord(
            "model_identity_recovered",
            "The historical LSC 6.3.0 model identity was recovered.",
            "SUPPORTED",
            "Version, commit, freeze boundary, version DOI, and concept DOI agree.",
            "Steps 01, 02, and frozen_model_identity.json",
            True,
        ),
        PublicClaimRecord(
            "equations_recovered",
            "The symbolic E1-E12 equation set was recovered.",
            "SUPPORTED_SYMBOLIC_ONLY",
            "The canonical equation source and SHA-256 are fixed; this does not supply numerical values.",
            "Steps 01-02 and canonical equation hash",
            True,
        ),
        PublicClaimRecord(
            "provenance_recovered",
            "Release and symbolic provenance were recovered.",
            "SUPPORTED_WITH_SCOPE",
            "The available lineage is auditable, while the missing numerical object has no recoverable provenance.",
            "Steps 01 and 05 provenance registries",
            True,
        ),
        PublicClaimRecord(
            "numerical_predictions_reproducible",
            "Numerical predictions of historical 6.3.0 are reproducible.",
            "MODEL_NOT_NUMERICALLY_RECOVERABLE",
            "The complete parameter vector, functions, units, frames, tensor state, initialization, and prediction table are absent.",
            "Step 05 parameter adjudication",
            False,
        ),
        PublicClaimRecord(
            "historical_predictions_recoverable",
            "Historical 6.3.0 prediction tables are recoverable.",
            "TEST_BLOCKED",
            "No authentic frozen prediction table was located.",
            "Steps 01 and 05 release-artifact search",
            False,
        ),
        PublicClaimRecord(
            "best_validation_possible",
            "An exact frozen 6.3.0 BEST validation can be performed.",
            "TEST_BLOCKED",
            "The numerical model is incomplete and full collaboration likelihood/covariance is unavailable.",
            "Steps 03-05 unlock matrix",
            False,
        ),
        PublicClaimRecord(
            "sage_validation_possible",
            "An exact frozen 6.3.0 SAGE validation can be performed.",
            "TEST_BLOCKED",
            "The numerical model and authoritative run covariance are unavailable.",
            "Steps 03-05 unlock matrix",
            False,
        ),
        PublicClaimRecord(
            "gallex_validation_possible",
            "An exact frozen 6.3.0 GALLEX/GNO validation can be performed.",
            "TEST_BLOCKED",
            "The numerical model and authoritative source-run covariance/likelihood are unavailable.",
            "Steps 03-05 unlock matrix",
            False,
        ),
        PublicClaimRecord(
            "katrin_veto_possible",
            "KATRIN can currently exclude or confirm LSC.",
            "TEST_BLOCKED_MAPPING_MISSING",
            "The native KATRIN grid is valid, but no justified LSC mapping exists.",
            "Step 05 KATRIN mapping assessment",
            False,
        ),
        PublicClaimRecord(
            "icecube_veto_possible",
            "IceCube can currently exclude or confirm LSC.",
            "TEST_BLOCKED_MAPPING_MISSING",
            "The native IceCube release is valid, but no justified LSC mapping exists.",
            "Step 05 IceCube mapping assessment",
            False,
        ),
        PublicClaimRecord(
            "directional_test_possible",
            "The historical directional/sidereal test can currently be executed.",
            "TEST_BLOCKED",
            "Timing, orientation, geometry, active tensor, frames, units, and statistic prerequisites are incomplete.",
            "Steps 02-05 T12 gates",
            False,
        ),
        PublicClaimRecord(
            "best2_prediction_possible",
            "A BEST-2 prediction is currently available or authorized.",
            "FUTURE_ONLY_BLOCKED",
            "The executable successor and authoritative as-built inputs do not yet exist.",
            "BEST2FuturePredictionContract and Step 05 blocker registry",
            False,
        ),
    )


def assert_public_claim_allowed(claim_id: str) -> None:
    by_id = {record.claim_id: record for record in allowed_claim_records()}
    record = by_id.get(claim_id)
    if record is None or not record.allowed_in_publication:
        raise PublicClaimNotAuthorized(
            "The requested public claim is not authorized by the Step 06 evidence boundary.",
            details={"claim_id": claim_id, "status": record.status if record else "UNKNOWN_CLAIM"},
        )


def assert_successor_identity(
    *,
    version: str,
    source_commit: str | None = None,
    version_doi: str | None = None,
) -> None:
    """Reject reassignment of immutable 6.3.0 identifiers to a successor."""

    conflicts: list[str] = []
    if version in {"6.3.0", HISTORICAL_VERSION}:
        conflicts.append("historical_version")
    if source_commit == HISTORICAL_COMMIT:
        conflicts.append("historical_commit")
    if version_doi == HISTORICAL_VERSION_DOI:
        conflicts.append("historical_version_doi")
    if conflicts:
        raise HistoricalIdentityReassignmentRejected(
            "A successor cannot reuse the immutable identity of historical LSC 6.3.0.",
            details={"conflicts": conflicts, "successor_version": version},
        )


def assert_successor_content_classification(*, requested_class: str, newly_specified: bool) -> None:
    valid = {member.value for member in SuccessorContentClass}
    if requested_class not in valid:
        raise SuccessorClassificationError(
            "Unknown 6.3.1 content classification.", details={"requested_class": requested_class}
        )
    if newly_specified and requested_class == SuccessorContentClass.UNCHANGED_FROM_6_3_0_AUTHENTIC.value:
        raise SuccessorClassificationError(
            "A newly specified numerical value cannot be classified as authentic unchanged 6.3.0 content.",
            details={"requested_class": requested_class},
        )


def assert_blindness_label(*, exposure_class: str, blindness_level: str) -> None:
    if exposure_class in {"MODEL_EXPOSED", "POST_DATA_MODEL_CHANGE"} and blindness_level in {
        "BLIND_STRICT",
        "PROSPECTIVE_BLIND",
    }:
        raise BlindnessLabelRejected(
            "A model-exposed historical dataset cannot be labelled strict or prospective blind.",
            details={"exposure_class": exposure_class, "blindness_level": blindness_level},
        )


EXECUTABLE_RELEASE_REQUIRED_FLAGS = (
    "complete_parameter_vector",
    "canonical_ordering",
    "values",
    "units",
    "frame_definitions",
    "tensor_components",
    "tensor_semantics",
    "initialization_rules",
    "bounds_and_default_policy",
    "executable_evaluator",
    "prediction_input_schema",
    "deterministic_output",
    "golden_reference_vectors",
    "parameter_bundle_sha256",
    "commit_identity",
    "environment_lock",
    "provenance_manifest",
    "machine_readable_release_manifest",
)


def assert_publication_ready(requirements: Mapping[str, bool]) -> None:
    missing = tuple(name for name in EXECUTABLE_RELEASE_REQUIRED_FLAGS if requirements.get(name) is not True)
    if missing:
        raise PublicationBoundaryViolation(
            "The executable successor cannot be marked publication-ready.",
            details={"missing_requirements": list(missing)},
        )


def publication_boundary() -> dict[str, object]:
    decision = recoverability_decision()
    claims = allowed_claim_records()
    return {
        "schema_version": "1.0.0",
        "decision_date": "2026-08-16",
        "decision_verdict": STEP06_VERDICT,
        "historical_version": HISTORICAL_VERSION,
        "historical_commit": HISTORICAL_COMMIT,
        "historical_freeze_commit": HISTORICAL_FREEZE_COMMIT,
        "historical_DOI": HISTORICAL_VERSION_DOI,
        "historical_concept_DOI": HISTORICAL_CONCEPT_DOI,
        "identity_recoverability": decision["identity_recoverability"],
        "symbolic_recoverability": decision["symbolic_recoverability"],
        "numerical_recoverability": decision["numerical_recoverability"],
        "successor_version_required": True,
        "successor_version_candidate": "6.3.1",
        "version_bump_rule": {
            "6.3.1": "Allowed only if E1-E12 and the model class remain unchanged; reproducibility, explicit numerical specification, methodology, and provenance changes only.",
            "6.4.0_or_7.0": "Required if Step 07 changes equations, physical semantics, or model class; major bump for incompatible conceptual change.",
        },
        "preserved_components": [
            "historical release identity, commit, version DOI, and concept DOI",
            "canonical symbolic E1-E12 equation set",
            "authentic parameter names and roles",
            "freeze boundary and negative evidence",
            "historical validation protocol and provenance lineage",
        ],
        "newly_specified_components_required": [
            "complete parameter vector and canonical ordering",
            "all numerical values and uncertainties",
            "exact f0_a and fA_a definitions",
            "active tensor components, normalization, orientation, and frame",
            "complete units and transformations",
            "initialization, bounds, defaults, and normalization order",
            "executable evaluator, prediction input schema, and deterministic outputs",
            "golden numerical reference vectors and release manifest",
        ],
        "content_classifications": [member.value for member in SuccessorContentClass],
        "historical_data_blindness": [
            {"dataset_id": "BEST", "exposure": "MODEL_EXPOSED", "blindness": "NON_BLIND_HISTORICAL", "role": "RETROSPECTIVE_NON_BLIND"},
            {"dataset_id": "GALLEX_GNO", "exposure": "MODEL_EXPOSED", "blindness": "NON_BLIND_HISTORICAL", "role": "RETROSPECTIVE_NON_BLIND"},
            {"dataset_id": "SAGE_CR51", "exposure": "MODEL_EXPOSED", "blindness": "NON_BLIND_HISTORICAL", "role": "RETROSPECTIVE_NON_BLIND"},
            {"dataset_id": "SAGE_AR37", "exposure": "MODEL_EXPOSED", "blindness": "NON_BLIND_HISTORICAL", "role": "RETROSPECTIVE_NON_BLIND"},
        ],
        "historical_data_allowed_roles": [
            "model development",
            "compatibility assessment",
            "retrospective benchmark",
            "parameter illustration",
            "baseline comparison",
        ],
        "historical_data_prohibited_role": "strict blind confirmation of 6.3.1",
        "validation_tracks": {
            "TRACK_A": {"name": "Retrospective validation", "label": "RETROSPECTIVE_NON_BLIND", "datasets": ["BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37"]},
            "TRACK_B": {"name": "Prospective validation", "label": "PROSPECTIVE_BLIND", "requirements": ["model frozen before outcomes", "prediction artifact hashed and timestamped", "no observed target data accessed"]},
        },
        "future_blind_targets": [
            {"dataset_id": "BEST2_FUTURE", "status": "FUTURE_ONLY", "blindness": "FUTURE_BLIND"},
            {"dataset_id": "NEW_GALLIUM_SOURCE_EXPERIMENT", "status": "FUTURE_ELIGIBLE", "blindness": "CONDITIONAL_ON_PRE_DATA_FREEZE"},
            {"dataset_id": "NEW_INDEPENDENT_EXPERIMENT", "status": "FUTURE_ELIGIBLE", "blindness": "ASSESS_INDIVIDUALLY_BEFORE_DATA_ACCESS"},
        ],
        "allowed_claims": [record.as_dict() for record in claims if record.allowed_in_publication],
        "prohibited_claims": [record.as_dict() for record in claims if not record.allowed_in_publication],
        "prohibited_publication_language": [
            "6.3.1 reproduces exactly the original frozen 6.3.0 numerical model",
            "6.3.0 passed independent validation",
            "BEST blindly confirms 6.3.1",
            "KATRIN or IceCube exclude or confirm LSC",
            "a blocked test is a model falsification result",
        ],
        "release_requirements": list(EXECUTABLE_RELEASE_REQUIRED_FLAGS),
        "zenodo_strategy": {
            "recommendation": "OPTION_C",
            "model_release": "Create 6.3.1 as a new version in the 6.3 lineage only after freeze, producing a new version DOI while preserving the historical record.",
            "validation_companion": "Publish the Validation Kernel/reproducibility package as a separate linked record with its own DOI.",
            "historical_version_doi_reused": False,
            "publication_performed": False,
        },
        "publication_readiness": {
            "maximum_current_level": PublicationReadinessLevel.P1_SPECIFICATION_BOUNDARY_READY.value,
            "historical_preservation_ready": True,
            "specification_boundary_ready": True,
            "executable_successor_ready": False,
            "release_package_ready": False,
            "retrospective_validation_ready": False,
            "prospective_prediction_ready": False,
        },
        "prediction_authorized": False,
        "numerical_validation_authorized": False,
        "BEST2_prediction_authorized": False,
        "publication_authorized": False,
    }


def step07_input_contract(
    *,
    publication_boundary_sha256: str,
    parameter_bundle_schema_sha256: str,
) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "contract_date": "2026-08-16",
        "source_decision_verdict": STEP06_VERDICT,
        "publication_boundary_sha256": publication_boundary_sha256,
        "release_naming": {
            "project": "LSC",
            "candidate_version": "6.3.1",
            "identity": "explicitly specified executable successor",
            "not_allowed_identity": "recovered numerical copy of 6.3.0",
            "version_escalation": "Use 6.4.0 or 7.0 if E1-E12, physical semantics, or model class changes.",
        },
        "equations_allowed_to_preserve": {
            "equation_ids": [f"E{i}" for i in range(1, 13)],
            "symbolic_equation_set_sha256": SYMBOLIC_EQUATION_SHA256,
            "condition": "Preserve only if explicitly unchanged; any physical change triggers version escalation.",
        },
        "unresolved_objects": [
            "theta",
            "parameter_ordering",
            "lambda0",
            "lambdaA",
            "f0_a",
            "fA_a",
            "active_tensor_components",
            "tensor_orientation",
            "complete_reference_frame",
            "complete_units",
            "eta",
            "covariance",
            "numerical_configuration",
            "parameter_bounds",
            "numerical_defaults",
            "frozen_prediction_table",
            "executable_evaluator_inputs",
        ],
        "parameter_fields_required": [
            "parameter_id",
            "value",
            "units",
            "origin",
            "reason",
            "introduced_version",
            "data_exposure_status",
            "inherited",
            "newly_specified",
            "fit_derived",
            "uncertainty",
            "frozen_status",
        ],
        "classifications_allowed": [member.value for member in SuccessorContentClass],
        "provenance_requirements": [
            "source identity and SHA-256 for every preserved or inherited object",
            "explicit reason and decision record for every newly specified value",
            "no cross-era composite or silent legacy inheritance",
            "fit-derived values identify all training datasets and cannot support blind claims on those datasets",
            "UNRESOLVED content cannot enter an executable release",
        ],
        "data_exposure_labels": {
            "historical_gallium": ["MODEL_EXPOSED", "NON_BLIND_HISTORICAL", "RETROSPECTIVE_NON_BLIND"],
            "BEST2": ["FUTURE_ONLY", "FUTURE_BLIND"],
            "future_prediction": ["PROSPECTIVE_BLIND only after complete pre-outcome freeze"],
        },
        "numerical_bundle_schema": {
            "path": "frozen_core/parameters/frozen_parameter_bundle.schema.json",
            "sha256": parameter_bundle_schema_sha256,
            "note": "Step 07 may version/extend the schema for 6.3.1 but may not weaken provenance or completeness gates.",
        },
        "freeze_requirements": list(EXECUTABLE_RELEASE_REQUIRED_FLAGS),
        "golden_reference_requirement": "Multiple experiment-independent input cases with exact or precision-bounded expected output.",
        "development_sequence": [
            "specification",
            "parameter determination",
            "freeze",
            "retrospective evaluation",
            "prospective prediction",
            "future unblinding",
        ],
        "validation_restrictions": [
            "No 6.3.0 numerical reconstruction claim.",
            "No historical gallium dataset may be labelled strict blind for 6.3.1.",
            "No LSC numerical validation before the new 6.3.1 freeze.",
            "No BEST-2 prediction before authoritative as-built inputs and the 6.3.1 freeze.",
            "No KATRIN/IceCube claim without an explicit authorized mapping.",
        ],
        "prediction_authorized": False,
        "numerical_validation_authorized": False,
        "publication_authorized": False,
    }
