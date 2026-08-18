"""Auditable model comparison without implicit significance claims."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .errors import MetricPrerequisiteError
from .metrics import delta_chi_square, information_criteria
from .result_schema import BaselineResult


@dataclass(frozen=True, slots=True)
class ModelComparison:
    candidate_model: str
    reference_model: str
    delta_chi_square: float
    delta_aic: float | None
    delta_bic: float | None
    preferred_by_raw_statistic: str
    interpretation: str
    significance_authorized: bool = False

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def compare_baselines(
    candidate: BaselineResult,
    reference: BaselineResult,
    *,
    likelihood_normalization_comparable: bool,
) -> ModelComparison:
    if (
        candidate.dataset_id != reference.dataset_id
        or candidate.split_id != reference.split_id
        or candidate.covariance_scenario != reference.covariance_scenario
        or candidate.n_observations != reference.n_observations
    ):
        raise MetricPrerequisiteError(
            "Model comparison requires identical dataset, split, covariance, and observation-count contracts."
        )
    delta = delta_chi_square(
        candidate.statistic,
        reference.statistic,
        comparable_data_and_covariance=True,
    )
    delta_aic = None
    delta_bic = None
    if likelihood_normalization_comparable:
        candidate_ic = information_criteria(
            minus_two_log_likelihood=candidate.statistic,
            n_parameters=candidate.n_parameters,
            n_observations=candidate.n_observations,
            likelihood_normalization_comparable=True,
        )
        reference_ic = information_criteria(
            minus_two_log_likelihood=reference.statistic,
            n_parameters=reference.n_parameters,
            n_observations=reference.n_observations,
            likelihood_normalization_comparable=True,
        )
        delta_aic = candidate_ic.aic - reference_ic.aic
        delta_bic = candidate_ic.bic - reference_ic.bic
    preferred = candidate.model_id if delta < 0 else reference.model_id if delta > 0 else "TIE"
    sensitivity_only = candidate.sensitivity_only or reference.sensitivity_only
    return ModelComparison(
        candidate_model=candidate.model_id,
        reference_model=reference.model_id,
        delta_chi_square=delta,
        delta_aic=delta_aic,
        delta_bic=delta_bic,
        preferred_by_raw_statistic=preferred,
        interpretation=(
            "SENSITIVITY_ONLY_NO_SIGNIFICANCE"
            if sensitivity_only
            else "MODEL_RANKING_ONLY_NO_AUTOMATIC_COVERAGE_CLAIM"
        ),
        significance_authorized=False,
    )
