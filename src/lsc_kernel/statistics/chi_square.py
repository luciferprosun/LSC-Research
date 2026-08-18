"""Gaussian chi-square primitives with explicit covariance policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .covariance import CovarianceMatrix
from .errors import StatisticalInputError
from .result_schema import StatisticEvaluation


def _vectors(
    observations: ArrayLike,
    predictions: ArrayLike,
    *,
    mask: ArrayLike | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.bool_]]:
    observed = np.asarray(observations, dtype=np.float64)
    predicted = np.asarray(predictions, dtype=np.float64)
    if observed.ndim != 1 or predicted.ndim != 1 or observed.shape != predicted.shape or observed.size == 0:
        raise StatisticalInputError("Observations and predictions must be non-empty equal-length vectors.")
    if not np.isfinite(observed).all() or not np.isfinite(predicted).all():
        raise StatisticalInputError("Observations and predictions must be finite.")
    selected = np.ones(observed.size, dtype=np.bool_) if mask is None else np.asarray(mask, dtype=np.bool_)
    if selected.ndim != 1 or selected.shape != observed.shape or not selected.any():
        raise StatisticalInputError("Mask must select at least one element from the observation vector.")
    return observed[selected], predicted[selected], selected


def diagonal_gaussian_chi_square(
    observations: ArrayLike,
    predictions: ArrayLike,
    uncertainties: ArrayLike,
    *,
    mask: ArrayLike | None = None,
    n_fitted_parameters: int = 0,
) -> StatisticEvaluation:
    observed, predicted, selected = _vectors(observations, predictions, mask=mask)
    sigma_all = np.asarray(uncertainties, dtype=np.float64)
    if sigma_all.ndim != 1 or sigma_all.shape != selected.shape:
        raise StatisticalInputError("Uncertainty vector must match the unmasked observations.")
    sigma = sigma_all[selected]
    if not np.isfinite(sigma).all() or np.any(sigma <= 0):
        raise StatisticalInputError("Selected uncertainties must be finite and strictly positive.")
    if not 0 <= n_fitted_parameters < observed.size:
        raise StatisticalInputError("Fitted-parameter count must be non-negative and smaller than selected observations.")
    value = float(np.sum(((observed - predicted) / sigma) ** 2))
    return StatisticEvaluation(
        raw_statistic=value,
        profiled_statistic=value,
        statistic_type="DIAGONAL_GAUSSIAN_CHI_SQUARE",
        n_observations=int(observed.size),
        n_fitted_parameters=int(n_fitted_parameters),
        dof_if_valid=int(observed.size - n_fitted_parameters),
        convergence=True,
        assumptions=("INDEPENDENT_GAUSSIAN_RESIDUALS", "DECLARED_DIAGONAL_UNCERTAINTIES"),
    )


def full_covariance_gaussian_chi_square(
    observations: ArrayLike,
    predictions: ArrayLike,
    covariance: CovarianceMatrix,
    *,
    mask: ArrayLike | None = None,
    n_fitted_parameters: int = 0,
) -> StatisticEvaluation:
    observed, predicted, selected = _vectors(observations, predictions, mask=mask)
    covariance.require_dimension(int(selected.size))
    if not 0 <= n_fitted_parameters < observed.size:
        raise StatisticalInputError("Fitted-parameter count must be non-negative and smaller than selected observations.")
    if selected.all():
        active = covariance
    else:
        indices = np.flatnonzero(selected)
        active = CovarianceMatrix(
            covariance.values[np.ix_(indices, indices)],
            symmetry_tolerance=covariance.diagnostics.symmetry_tolerance,
            psd_tolerance=covariance.diagnostics.psd_tolerance,
            rank_tolerance=covariance.diagnostics.rank_tolerance,
            singular_policy=covariance.singular_policy,
            pseudo_inverse_rcond=covariance.pseudo_inverse_rcond,
        )
    value, warnings = active.quadratic_form(observed - predicted)
    assumptions = ["MULTIVARIATE_GAUSSIAN_RESIDUALS", "DECLARED_COVARIANCE_MATRIX"]
    if active.diagnostics.singular:
        assumptions.append("EXPLICIT_PSEUDOINVERSE_POLICY")
    return StatisticEvaluation(
        raw_statistic=value,
        profiled_statistic=value,
        statistic_type="FULL_COVARIANCE_GAUSSIAN_CHI_SQUARE",
        n_observations=int(observed.size),
        n_fitted_parameters=int(n_fitted_parameters),
        dof_if_valid=int(observed.size - n_fitted_parameters),
        convergence=True,
        assumptions=tuple(assumptions),
        covariance_diagnostics=active.diagnostics.as_dict(),
        warnings=warnings,
    )


def pull_term_chi_square(
    nuisance_values: ArrayLike,
    prior_means: ArrayLike,
    prior_sigmas: ArrayLike,
) -> float:
    values = np.asarray(nuisance_values, dtype=np.float64)
    means = np.asarray(prior_means, dtype=np.float64)
    sigmas = np.asarray(prior_sigmas, dtype=np.float64)
    if values.ndim != 1 or values.shape != means.shape or values.shape != sigmas.shape:
        raise StatisticalInputError("Pull values, means, and sigmas must be equal-length vectors.")
    if not np.isfinite(values).all() or not np.isfinite(means).all() or not np.isfinite(sigmas).all():
        raise StatisticalInputError("Pull-term inputs must be finite.")
    if np.any(sigmas <= 0):
        raise StatisticalInputError("Pull-term sigmas must be strictly positive.")
    return float(np.sum(((values - means) / sigmas) ** 2))


@dataclass(frozen=True, slots=True)
class GridChiSquare:
    """Release-native absolute chi-square lookup with no implicit interpolation."""

    axis_0: tuple[float, ...]
    axis_1: tuple[float, ...]
    values: tuple[tuple[float, ...], ...]
    axis_0_name: str
    axis_1_name: str
    interpolation_authorized: bool = False

    def __post_init__(self) -> None:
        array = np.asarray(self.values, dtype=np.float64)
        if array.shape != (len(self.axis_0), len(self.axis_1)) or array.ndim != 2:
            raise StatisticalInputError("Grid dimensions must match both parameter axes.")
        if array.size == 0 or not np.isfinite(array).all():
            raise StatisticalInputError("Grid values must be non-empty and finite.")
        if not np.isfinite(np.asarray(self.axis_0)).all() or not np.isfinite(np.asarray(self.axis_1)).all():
            raise StatisticalInputError("Grid axes must be finite.")

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.axis_0), len(self.axis_1))

    def minimum(self) -> tuple[float, tuple[int, int], tuple[float, float]]:
        array = np.asarray(self.values, dtype=np.float64)
        flat_index = int(np.argmin(array))
        index = tuple(int(item) for item in np.unravel_index(flat_index, array.shape))
        return float(array[index]), index, (float(self.axis_0[index[0]]), float(self.axis_1[index[1]]))

    def exact(self, axis_0_value: float, axis_1_value: float) -> float:
        try:
            first = self.axis_0.index(float(axis_0_value))
            second = self.axis_1.index(float(axis_1_value))
        except ValueError as error:
            raise StatisticalInputError(
                "Requested grid point is not exact; interpolation is not authorized by this release contract."
            ) from error
        return float(self.values[first][second])

    def nearest(self, axis_0_value: float, axis_1_value: float) -> tuple[float, tuple[float, float]]:
        first = int(np.argmin(np.abs(np.asarray(self.axis_0) - axis_0_value)))
        second = int(np.argmin(np.abs(np.asarray(self.axis_1) - axis_1_value)))
        return float(self.values[first][second]), (float(self.axis_0[first]), float(self.axis_1[second]))


def grid_from_sequences(
    axis_0: Sequence[float],
    axis_1: Sequence[float],
    values: Sequence[Sequence[float]],
    *,
    axis_0_name: str,
    axis_1_name: str,
) -> GridChiSquare:
    return GridChiSquare(
        tuple(float(item) for item in axis_0),
        tuple(float(item) for item in axis_1),
        tuple(tuple(float(cell) for cell in row) for row in values),
        axis_0_name,
        axis_1_name,
    )
