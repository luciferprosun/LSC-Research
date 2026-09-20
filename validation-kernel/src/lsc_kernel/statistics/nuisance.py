"""Explicit fixed, pull, bounded, shared, and correlated nuisance profiling."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike

from .covariance import CovarianceMatrix
from .errors import StatisticalInputError
from .optimization import OptimizationResult, optimize_baseline
from .result_schema import StatisticEvaluation


class NuisanceKind(StrEnum):
    FIXED = "FIXED"
    GAUSSIAN_PULL = "GAUSSIAN_PULL"
    BOUNDED = "BOUNDED"
    CORRELATED = "CORRELATED"
    SHARED = "SHARED"
    EXPERIMENT_SPECIFIC = "EXPERIMENT_SPECIFIC"


@dataclass(frozen=True, slots=True)
class NuisanceParameter:
    name: str
    kind: NuisanceKind
    initial: float
    lower_bound: float | None
    upper_bound: float | None
    prior_mean: float | None
    prior_sigma: float | None
    effect: tuple[float, ...]
    effect_mode: str = "ADDITIVE"
    fixed_value: float | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.effect:
            raise StatisticalInputError("Nuisance name and effect vector are required.")
        scalar_values = (
            self.initial,
            self.lower_bound,
            self.upper_bound,
            self.prior_mean,
            self.prior_sigma,
            self.fixed_value,
        )
        if any(value is not None and not np.isfinite(float(value)) for value in scalar_values):
            raise StatisticalInputError("Nuisance scalar values must be finite when supplied.")
        if not np.isfinite(np.asarray(self.effect, dtype=np.float64)).all():
            raise StatisticalInputError("Nuisance effect vector must be finite.")
        if self.effect_mode not in {"ADDITIVE", "FRACTIONAL_MULTIPLICATIVE"}:
            raise StatisticalInputError("Unknown nuisance effect mode.")
        if self.kind is NuisanceKind.FIXED and self.fixed_value is None:
            raise StatisticalInputError("Fixed nuisance requires fixed_value.")
        if (self.prior_mean is None) != (self.prior_sigma is None):
            if self.kind is not NuisanceKind.CORRELATED:
                raise StatisticalInputError("An uncorrelated nuisance prior requires both mean and sigma.")
        if self.kind is NuisanceKind.CORRELATED and self.prior_mean is None:
            raise StatisticalInputError("Correlated nuisance requires an explicit prior mean.")
        if self.prior_sigma is not None and self.prior_sigma <= 0:
            raise StatisticalInputError("Nuisance prior sigma must be positive.")
        if (
            self.lower_bound is not None
            and self.upper_bound is not None
            and self.lower_bound > self.upper_bound
        ):
            raise StatisticalInputError("Nuisance lower bound cannot exceed its upper bound.")
        if self.lower_bound is not None and self.initial < self.lower_bound:
            raise StatisticalInputError("Nuisance initial value is below its declared lower bound.")
        if self.upper_bound is not None and self.initial > self.upper_bound:
            raise StatisticalInputError("Nuisance initial value is above its declared upper bound.")
        if self.kind is NuisanceKind.BOUNDED and self.lower_bound is None and self.upper_bound is None:
            raise StatisticalInputError("Bounded nuisance requires at least one explicit bound.")

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["kind"] = self.kind.value
        return result


@dataclass(frozen=True, slots=True)
class NuisanceProfileResult:
    evaluation: StatisticEvaluation
    optimization: OptimizationResult | None
    profiled_prediction: tuple[float, ...]
    values: tuple[tuple[str, float], ...]
    pull_statistic: float


class NuisanceEngine:
    def __init__(
        self,
        parameters: Iterable[NuisanceParameter],
        *,
        correlated_prior_covariance: CovarianceMatrix | None = None,
    ) -> None:
        self.parameters = tuple(parameters)
        if len({item.name for item in self.parameters}) != len(self.parameters):
            raise StatisticalInputError("Nuisance names must be unique.")
        correlated = tuple(item for item in self.parameters if item.kind is NuisanceKind.CORRELATED)
        if correlated and correlated_prior_covariance is None:
            raise StatisticalInputError("Correlated nuisance parameters require an explicit prior covariance.")
        if not correlated and correlated_prior_covariance is not None:
            raise StatisticalInputError(
                "A correlated prior covariance was supplied without correlated nuisance parameters."
            )
        if correlated_prior_covariance is not None:
            correlated_prior_covariance.require_dimension(len(correlated))
        self.correlated_prior_covariance = correlated_prior_covariance

    @staticmethod
    def _prediction(base: np.ndarray, parameters: tuple[NuisanceParameter, ...], values: np.ndarray) -> np.ndarray:
        predicted = base.copy()
        for parameter, value in zip(parameters, values, strict=True):
            effect = np.asarray(parameter.effect, dtype=np.float64)
            if effect.shape != base.shape:
                raise StatisticalInputError(f"Effect shape for nuisance {parameter.name} does not match predictions.")
            if parameter.effect_mode == "ADDITIVE":
                predicted = predicted + value * effect
            else:
                predicted = predicted * (1.0 + value * effect)
        return predicted

    def profile(
        self,
        observations: ArrayLike,
        base_prediction: ArrayLike,
        covariance: CovarianceMatrix,
        *,
        model_id: str,
    ) -> NuisanceProfileResult:
        observed = np.asarray(observations, dtype=np.float64)
        base = np.asarray(base_prediction, dtype=np.float64)
        if observed.ndim != 1 or observed.shape != base.shape or observed.size == 0:
            raise StatisticalInputError("Observed and base prediction vectors must match.")
        covariance.require_dimension(int(observed.size))
        for parameter in self.parameters:
            if len(parameter.effect) != observed.size:
                raise StatisticalInputError(f"Effect dimension mismatch for nuisance {parameter.name}.")
        floating = tuple(parameter for parameter in self.parameters if parameter.kind is not NuisanceKind.FIXED)
        fixed = tuple(parameter for parameter in self.parameters if parameter.kind is NuisanceKind.FIXED)
        fixed_values = np.asarray([float(item.fixed_value) for item in fixed], dtype=np.float64)
        fixed_prediction = self._prediction(base, fixed, fixed_values) if fixed else base

        def pull(values: np.ndarray) -> tuple[float, tuple[str, ...]]:
            correlated_with_prior = [
                (index, item)
                for index, item in enumerate(floating)
                if item.kind is NuisanceKind.CORRELATED
            ]
            independent_with_prior = [
                (index, item)
                for index, item in enumerate(floating)
                if item.kind is not NuisanceKind.CORRELATED
                and item.prior_mean is not None
                and item.prior_sigma is not None
            ]
            correlated_statistic = 0.0
            correlated_warnings: tuple[str, ...] = ()
            if correlated_with_prior:
                deviations = np.asarray(
                    [values[index] - float(item.prior_mean) for index, item in correlated_with_prior]
                )
                correlated_statistic, correlated_warnings = (
                    self.correlated_prior_covariance.quadratic_form(deviations)
                )
            independent_statistic = sum(
                ((values[index] - float(item.prior_mean)) / float(item.prior_sigma)) ** 2
                for index, item in independent_with_prior
            )
            return float(correlated_statistic + independent_statistic), correlated_warnings

        def objective(values: np.ndarray) -> float:
            prediction = self._prediction(fixed_prediction, floating, values)
            data_statistic, _ = covariance.quadratic_form(observed - prediction)
            return data_statistic + pull(values)[0]

        if floating:
            optimization = optimize_baseline(
                objective,
                model_id=model_id,
                initial_values=[item.initial for item in floating],
                bounds=[(item.lower_bound, item.upper_bound) for item in floating],
                parameter_scope="NUISANCE_ONLY",
            )
            values = np.asarray(optimization.final_parameters, dtype=np.float64)
            convergence = optimization.convergence
        else:
            optimization = None
            values = np.asarray([], dtype=np.float64)
            convergence = True
        final_prediction = self._prediction(fixed_prediction, floating, values)
        data_statistic, warnings = covariance.quadratic_form(observed - final_prediction)
        pull_statistic, prior_warnings = pull(values)
        named_values = tuple((item.name, float(value)) for item, value in zip(floating, values, strict=True))
        named_values += tuple((item.name, float(item.fixed_value)) for item in fixed)
        raw_statistic, raw_warnings = covariance.quadratic_form(observed - base)
        evaluation = StatisticEvaluation(
            raw_statistic=raw_statistic,
            profiled_statistic=data_statistic + pull_statistic,
            statistic_type="PROFILED_NUISANCE_CHI_SQUARE",
            n_observations=int(observed.size),
            n_fitted_parameters=len(floating),
            dof_if_valid=(int(observed.size - len(floating)) if len(floating) < observed.size else None),
            convergence=convergence,
            assumptions=("DECLARED_COVARIANCE", "DECLARED_NUISANCE_EFFECTS", "DECLARED_PRIORS"),
            covariance_diagnostics=covariance.diagnostics.as_dict(),
            nuisance_values=named_values,
            warnings=tuple(sorted(set(warnings + raw_warnings + prior_warnings))),
        )
        return NuisanceProfileResult(
            evaluation=evaluation,
            optimization=optimization,
            profiled_prediction=tuple(float(item) for item in final_prediction),
            values=named_values,
            pull_statistic=pull_statistic,
        )
