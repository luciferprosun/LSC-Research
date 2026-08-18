"""Fail-closed errors for the executable LSC 6.4.0 profile."""

from __future__ import annotations


class LSC640Error(RuntimeError):
    """Base error carrying a stable machine-readable code."""

    code = "LSC_6_4_0_ERROR"

    def __init__(self, message: str, *, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class CrossSectionProvenanceError(LSC640Error):
    code = "A2_CROSS_SECTION_PROVENANCE_ERROR"


class UnsupportedDomainError(LSC640Error):
    code = "FAIL_CLOSED_UNSUPPORTED_DOMAIN"


class InvalidBaselineMeasure(LSC640Error):
    code = "FAIL_CLOSED_INVALID_BASELINE_MEASURE"


class PredictionInputError(LSC640Error):
    code = "FAIL_CLOSED_INVALID_PREDICTION_INPUT"


class UnsupportedModelProfileError(LSC640Error):
    code = "FAIL_CLOSED_UNSUPPORTED_MODEL_PROFILE"


class PreFitGateError(LSC640Error):
    code = "PRE_FIT_GATE_FAILED"


class NoRefitViolation(LSC640Error):
    code = "NO_REFIT_POLICY_VIOLATION"
