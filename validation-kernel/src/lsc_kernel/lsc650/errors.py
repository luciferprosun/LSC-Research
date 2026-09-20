"""Fail-closed errors for the executable LSC 6.5.0 profile."""

from __future__ import annotations


class LSC650Error(RuntimeError):
    """Base error with a stable machine-readable code."""

    code = "LSC_6_5_0_ERROR"

    def __init__(self, message: str, *, details: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class CrossSectionProvenanceError(LSC650Error):
    code = "LSC_6_5_0_EXTERNAL_PAYLOAD_BLOCKED"


class UnsupportedDomainError(LSC650Error):
    code = "FAIL_CLOSED_UNSUPPORTED_DOMAIN"


class InvalidBaselineMeasure(LSC650Error):
    code = "FAIL_CLOSED_INVALID_BASELINE_MEASURE"


class PredictionInputError(LSC650Error):
    code = "FAIL_CLOSED_INVALID_PREDICTION_INPUT"


class UnsupportedModelProfileError(LSC650Error):
    code = "FAIL_CLOSED_UNSUPPORTED_MODEL_PROFILE"


class ParameterBundleError(LSC650Error):
    code = "FAIL_CLOSED_PARAMETER_BUNDLE_ERROR"


class PreFitGateError(LSC650Error):
    code = "PRE_FIT_GATE_FAILED"


class NoRefitViolation(LSC650Error):
    code = "NO_REFIT_POLICY_VIOLATION"
