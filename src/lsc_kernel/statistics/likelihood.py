"""Core likelihood interface used only by fixtures and authorized baselines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy.typing import ArrayLike

from lsc_kernel.validation.policies import FROZEN_LSC_MODEL_IDS

from .chi_square import diagonal_gaussian_chi_square, full_covariance_gaussian_chi_square
from .covariance import CovarianceMatrix
from .errors import LSCStatisticalExecutionForbidden, StatisticalInputError
from .result_schema import StatisticEvaluation


class LikelihoodModel(ABC):
    """Deterministic statistic contract; it is not an LSC execution entry point."""

    @abstractmethod
    def evaluate(self) -> StatisticEvaluation:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class GaussianLikelihood(LikelihoodModel):
    model_id: str
    execution_classification: str
    observations: ArrayLike
    predictions: ArrayLike
    uncertainties: ArrayLike | None = None
    covariance: CovarianceMatrix | None = None
    mask: ArrayLike | None = None
    n_fitted_parameters: int = 0

    def evaluate(self) -> StatisticEvaluation:
        if self.model_id.upper() in FROZEN_LSC_MODEL_IDS:
            raise LSCStatisticalExecutionForbidden(
                "Frozen LSC predictions may enter the likelihood layer only through a future authorized evaluator path."
            )
        if not self.execution_classification:
            raise StatisticalInputError("Likelihood execution classification is required.")
        if (self.uncertainties is None) == (self.covariance is None):
            raise StatisticalInputError("Exactly one of uncertainties or covariance must be provided.")
        if self.covariance is not None:
            return full_covariance_gaussian_chi_square(
                self.observations,
                self.predictions,
                self.covariance,
                mask=self.mask,
                n_fitted_parameters=self.n_fitted_parameters,
            )
        return diagonal_gaussian_chi_square(
            self.observations,
            self.predictions,
            self.uncertainties,
            mask=self.mask,
            n_fitted_parameters=self.n_fitted_parameters,
        )

    def negative_log_likelihood(self, *, include_normalization: bool = False) -> float:
        evaluation = self.evaluate()
        if include_normalization:
            raise StatisticalInputError(
                "Normalized Gaussian log-likelihood requires an explicitly declared determinant contract."
            )
        return 0.5 * evaluation.profiled_statistic
