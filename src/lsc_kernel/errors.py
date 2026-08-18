"""Explicit fail-closed errors used by the Validation Kernel."""

from __future__ import annotations

from typing import Any


class FrozenSpecificationBlocker(RuntimeError):
    """Base class for a frozen-specification execution refusal."""

    error_code = "FROZEN_SPECIFICATION_BLOCKER"

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}

    def as_dict(self) -> dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "error_code": self.error_code,
            "message": str(self),
            "details": self.details,
        }


class FrozenIdentityMismatch(FrozenSpecificationBlocker):
    error_code = "FROZEN_IDENTITY_MISMATCH"


class FrozenParameterMissing(FrozenSpecificationBlocker):
    error_code = "FROZEN_PARAMETER_MISSING"


class FrozenParameterProvenanceError(FrozenSpecificationBlocker):
    error_code = "FROZEN_PARAMETER_PROVENANCE_ERROR"


class FrozenUnitUnknown(FrozenSpecificationBlocker):
    error_code = "FROZEN_UNIT_UNKNOWN"


class FrozenFrameUnknown(FrozenSpecificationBlocker):
    error_code = "FROZEN_FRAME_UNKNOWN"


class FrozenOrientationMissing(FrozenSpecificationBlocker):
    error_code = "FROZEN_ORIENTATION_MISSING"


class FrozenTensorIncomplete(FrozenSpecificationBlocker):
    error_code = "FROZEN_TENSOR_INCOMPLETE"


class FrozenEquationBlocked(FrozenSpecificationBlocker):
    error_code = "FROZEN_EQUATION_BLOCKED"


class PostDataArtifactRejected(FrozenSpecificationBlocker):
    error_code = "POST_DATA_ARTIFACT_REJECTED"


class UnverifiedCandidateRejected(FrozenSpecificationBlocker):
    error_code = "UNVERIFIED_CANDIDATE_REJECTED"


class PredictionNotAuthorized(FrozenSpecificationBlocker):
    error_code = "PREDICTION_NOT_AUTHORIZED"


class ValidationNotAuthorized(FrozenSpecificationBlocker):
    error_code = "VALIDATION_NOT_AUTHORIZED"


class FrozenModelRefitForbidden(FrozenSpecificationBlocker):
    error_code = "FROZEN_MODEL_REFIT_FORBIDDEN"


class DatasetContractError(FrozenSpecificationBlocker):
    error_code = "DATASET_CONTRACT_ERROR"


class ExternalVetoBlockedMappingMissing(FrozenSpecificationBlocker):
    error_code = "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING"


class MalformedBundle(FrozenSpecificationBlocker):
    error_code = "MALFORMED_BUNDLE"


class HistoricalCompositeRejected(FrozenSpecificationBlocker):
    error_code = "HISTORICAL_COMPOSITE_REJECTED"


class ConflictingCandidateRejected(FrozenSpecificationBlocker):
    error_code = "CONFLICTING_CANDIDATE_REJECTED"


class CollaborationCovarianceUnavailable(FrozenSpecificationBlocker):
    error_code = "COLLABORATION_COVARIANCE_UNAVAILABLE"


class T12PrerequisiteMissing(FrozenSpecificationBlocker):
    error_code = "T12_PREREQUISITE_MISSING"


class StepBoundaryPredictionBlocked(FrozenSpecificationBlocker):
    error_code = "STEP_05_PREDICTION_BLOCKED"


class HistoricalIdentityReassignmentRejected(FrozenSpecificationBlocker):
    error_code = "HISTORICAL_IDENTITY_REASSIGNMENT_REJECTED"


class PublicClaimNotAuthorized(FrozenSpecificationBlocker):
    error_code = "PUBLIC_CLAIM_NOT_AUTHORIZED"


class SuccessorClassificationError(FrozenSpecificationBlocker):
    error_code = "SUCCESSOR_CLASSIFICATION_ERROR"


class BlindnessLabelRejected(FrozenSpecificationBlocker):
    error_code = "BLINDNESS_LABEL_REJECTED"


class PublicationBoundaryViolation(FrozenSpecificationBlocker):
    error_code = "PUBLICATION_BOUNDARY_VIOLATION"
