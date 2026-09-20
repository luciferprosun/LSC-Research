"""Statistical metrics with prerequisite checks and interpretation limits."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .errors import MetricPrerequisiteError


@dataclass(frozen=True, slots=True)
class InformationCriteria:
    aic: float
    bic: float
    n_observations: int
    n_parameters: int
    contract: str


@dataclass(frozen=True, slots=True)
class CrossValidationScore:
    total_predictive_log_likelihood: float
    mean_predictive_log_likelihood: float
    n_folds: int
    all_preregistered_folds_included: bool


def information_criteria(
    *,
    minus_two_log_likelihood: float,
    n_parameters: int,
    n_observations: int,
    likelihood_normalization_comparable: bool,
) -> InformationCriteria:
    if not likelihood_normalization_comparable:
        raise MetricPrerequisiteError("AIC/BIC require comparable likelihood normalization.")
    if n_observations <= 0 or n_parameters < 0 or n_parameters >= n_observations:
        raise MetricPrerequisiteError("AIC/BIC require 0 <= k < n with a declared observation count.")
    if not math.isfinite(minus_two_log_likelihood):
        raise MetricPrerequisiteError("Likelihood statistic must be finite.")
    return InformationCriteria(
        aic=float(minus_two_log_likelihood + 2 * n_parameters),
        bic=float(minus_two_log_likelihood + n_parameters * math.log(n_observations)),
        n_observations=n_observations,
        n_parameters=n_parameters,
        contract="COMPARABLE_MINUS_TWO_LOG_LIKELIHOOD",
    )


def delta_chi_square(
    candidate: float,
    reference: float,
    *,
    comparable_data_and_covariance: bool,
) -> float:
    if not comparable_data_and_covariance:
        raise MetricPrerequisiteError("Delta chi-square requires identical data and covariance contracts.")
    if not math.isfinite(candidate) or not math.isfinite(reference):
        raise MetricPrerequisiteError("Delta chi-square inputs must be finite.")
    return float(candidate - reference)


def likelihood_ratio_statistic(
    candidate_minus_two_log_likelihood: float,
    reference_minus_two_log_likelihood: float,
    *,
    likelihoods_comparable: bool,
) -> float:
    if not likelihoods_comparable:
        raise MetricPrerequisiteError("Likelihood-ratio statistic requires comparable likelihoods.")
    return delta_chi_square(
        candidate_minus_two_log_likelihood,
        reference_minus_two_log_likelihood,
        comparable_data_and_covariance=True,
    )


def predictive_log_likelihood(
    chi_square_value: float,
    *,
    normalized_likelihood_available: bool,
    log_normalization: float | None = None,
) -> float:
    if not normalized_likelihood_available or log_normalization is None:
        raise MetricPrerequisiteError(
            "Predictive log-likelihood requires the held-out likelihood normalization, not chi-square alone."
        )
    if not math.isfinite(chi_square_value) or not math.isfinite(log_normalization):
        raise MetricPrerequisiteError("Predictive likelihood inputs must be finite.")
    return float(log_normalization - 0.5 * chi_square_value)


def cross_validation_score(
    fold_predictive_log_likelihoods: Sequence[float],
    *,
    expected_fold_count: int,
) -> CrossValidationScore:
    values = tuple(float(item) for item in fold_predictive_log_likelihoods)
    if expected_fold_count <= 0 or len(values) != expected_fold_count:
        raise MetricPrerequisiteError("Cross-validation score requires every preregistered fold exactly once.")
    if not all(math.isfinite(item) for item in values):
        raise MetricPrerequisiteError("Cross-validation fold scores must be finite.")
    total = float(sum(values))
    return CrossValidationScore(total, total / len(values), len(values), True)
