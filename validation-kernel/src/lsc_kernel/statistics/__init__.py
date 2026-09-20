"""Independent statistical instrumentation; no frozen-LSC numerical path."""

from .chi_square import diagonal_gaussian_chi_square, full_covariance_gaussian_chi_square
from .covariance import CovarianceMatrix, SingularPolicy
from .likelihood import GaussianLikelihood, LikelihoodModel
from .execution import BaselineExecutionEngine, ManifestedBaselineExecution
from .result_schema import BaselineResult, StatisticalExecutionManifest, StatisticEvaluation

__all__ = [
    "BaselineResult",
    "BaselineExecutionEngine",
    "CovarianceMatrix",
    "GaussianLikelihood",
    "LikelihoodModel",
    "ManifestedBaselineExecution",
    "SingularPolicy",
    "StatisticalExecutionManifest",
    "StatisticEvaluation",
    "diagonal_gaussian_chi_square",
    "full_covariance_gaussian_chi_square",
]
