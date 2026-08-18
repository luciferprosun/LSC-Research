"""Independent baseline models; frozen LSC models are never dispatched here."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from lsc_kernel.validation.policies import FROZEN_LSC_MODEL_IDS, NoRefitPolicy
from lsc_kernel.validation.registries import GalliumCrossSectionModelRegistry, baseline_model_registry

from .covariance import CovarianceMatrix
from .errors import BaselineSpecificationIncomplete, LSCStatisticalExecutionForbidden, StatisticalInputError
from .optimization import OptimizationResult, optimize_baseline
from .result_schema import StatisticEvaluation


ALIASES = {
    "M_NULL": "M0",
    "M_CONSTANT_DEFICIT": "M1",
    "M_CROSS_SECTION_VARIANT": "M2",
    "M_STERILE_3P1": "M3",
    "M_DETECTOR_SYSTEMATIC": "M4_DETECTOR_SYSTEMATIC",
    "M_EXPERIMENT_NORMALIZATION": "M4_EXPERIMENT_NORMALIZATION",
    "M_HIERARCHICAL_EXPERIMENT": "M4_HIERARCHICAL_EXPERIMENT",
}


@dataclass(frozen=True, slots=True)
class BaselineFit:
    model_id: str
    prediction: tuple[float, ...]
    evaluation: StatisticEvaluation
    fitted_parameters: tuple[tuple[str, float], ...]
    optimization: OptimizationResult | None
    assumptions: tuple[str, ...]


def _arrays(observed: ArrayLike, expected: ArrayLike, covariance: CovarianceMatrix) -> tuple[np.ndarray, np.ndarray]:
    observations = np.asarray(observed, dtype=np.float64)
    conventional = np.asarray(expected, dtype=np.float64)
    if observations.ndim != 1 or observations.shape != conventional.shape or observations.size == 0:
        raise StatisticalInputError("Observed and conventional expectation vectors must match.")
    if not np.isfinite(observations).all() or not np.isfinite(conventional).all():
        raise StatisticalInputError("Baseline inputs must be finite.")
    covariance.require_dimension(int(observations.size))
    return observations, conventional


def _evaluate(
    observed: np.ndarray,
    prediction: np.ndarray,
    covariance: CovarianceMatrix,
    *,
    n_fitted: int,
    raw_statistic: float | None = None,
    convergence: bool = True,
    warnings: tuple[str, ...] = (),
) -> StatisticEvaluation:
    statistic, covariance_warnings = covariance.quadratic_form(observed - prediction)
    return StatisticEvaluation(
        raw_statistic=statistic if raw_statistic is None else raw_statistic,
        profiled_statistic=statistic,
        statistic_type="BASELINE_FULL_COVARIANCE_CHI_SQUARE",
        n_observations=int(observed.size),
        n_fitted_parameters=n_fitted,
        dof_if_valid=(int(observed.size - n_fitted) if n_fitted < observed.size else None),
        convergence=convergence,
        assumptions=("DECLARED_BASELINE_MODEL", "DECLARED_COVARIANCE"),
        covariance_diagnostics=covariance.diagnostics.as_dict(),
        warnings=tuple(sorted(set(warnings + covariance_warnings))),
    )


def null_baseline(observed: ArrayLike, expected: ArrayLike, covariance: CovarianceMatrix) -> BaselineFit:
    observations, conventional = _arrays(observed, expected, covariance)
    evaluation = _evaluate(observations, conventional, covariance, n_fitted=0)
    return BaselineFit("M0", tuple(conventional), evaluation, (), None, ("PUBLISHED_NO_TRANSITION_EXPECTATION",))


def constant_deficit_baseline(
    observed: ArrayLike,
    expected: ArrayLike,
    covariance: CovarianceMatrix,
    *,
    bounds: tuple[float | None, float | None] = (0.0, 2.0),
) -> BaselineFit:
    observations, conventional = _arrays(observed, expected, covariance)
    raw_statistic, _ = covariance.quadratic_form(observations - conventional)

    def objective(values: np.ndarray) -> float:
        return covariance.quadratic_form(observations - values[0] * conventional)[0]

    optimization = optimize_baseline(
        objective,
        model_id="M1",
        initial_values=(1.0,),
        bounds=(bounds,),
    )
    normalization = optimization.final_parameters[0]
    prediction = normalization * conventional
    evaluation = _evaluate(
        observations,
        prediction,
        covariance,
        n_fitted=1,
        raw_statistic=raw_statistic,
        convergence=optimization.convergence,
    )
    return BaselineFit(
        "M1",
        tuple(float(item) for item in prediction),
        evaluation,
        (("normalization", normalization),),
        optimization,
        ("ONE_SHARED_NORMALIZATION",),
    )


def experiment_normalization_baseline(
    observed: ArrayLike,
    expected: ArrayLike,
    covariance: CovarianceMatrix,
    experiment_ids: Sequence[str],
) -> BaselineFit:
    observations, conventional = _arrays(observed, expected, covariance)
    groups = tuple(str(item) for item in experiment_ids)
    if len(groups) != observations.size:
        raise StatisticalInputError("One experiment ID is required per observation.")
    unique = tuple(dict.fromkeys(groups))
    if len(unique) >= observations.size:
        raise StatisticalInputError("Experiment-normalization baseline requires residual degrees of freedom.")
    raw_statistic, _ = covariance.quadratic_form(observations - conventional)

    def prediction(values: np.ndarray) -> np.ndarray:
        by_group = dict(zip(unique, values, strict=True))
        return np.asarray([by_group[group] * conventional[index] for index, group in enumerate(groups)])

    optimization = optimize_baseline(
        lambda values: covariance.quadratic_form(observations - prediction(values))[0],
        model_id="M4",
        initial_values=np.ones(len(unique)),
        bounds=tuple((0.0, 2.0) for _ in unique),
    )
    fitted_prediction = prediction(np.asarray(optimization.final_parameters))
    evaluation = _evaluate(
        observations,
        fitted_prediction,
        covariance,
        n_fitted=len(unique),
        raw_statistic=raw_statistic,
        convergence=optimization.convergence,
    )
    return BaselineFit(
        "M4_EXPERIMENT_NORMALIZATION",
        tuple(float(item) for item in fitted_prediction),
        evaluation,
        tuple((f"normalization[{group}]", value) for group, value in zip(unique, optimization.final_parameters, strict=True)),
        optimization,
        ("ONE_NORMALIZATION_PER_DECLARED_EXPERIMENT", "COMPLEXITY_COUNT_REPORTED"),
    )


def cross_section_variant_baseline(
    observed: ArrayLike,
    expectation_by_model: Mapping[str, ArrayLike],
    covariance: CovarianceMatrix,
    *,
    model_choice: str,
    profile_source_normalization: bool = False,
    model_registry: GalliumCrossSectionModelRegistry | None = None,
) -> BaselineFit:
    if model_registry is not None and model_choice not in {model.model_id for model in model_registry.models}:
        raise StatisticalInputError("Cross-section model choice is not present in GalliumCrossSectionModelRegistry.")
    if model_choice not in expectation_by_model:
        raise StatisticalInputError("Cross-section model choice must be an explicit registered key.")
    expected = np.asarray(expectation_by_model[model_choice], dtype=np.float64)
    observed_array, expected = _arrays(observed, expected, covariance)
    if profile_source_normalization:
        raw_statistic, _ = covariance.quadratic_form(observed_array - expected)
        optimization = optimize_baseline(
            lambda values: covariance.quadratic_form(observed_array - values[0] * expected)[0],
            model_id="M2",
            initial_values=(1.0,),
            bounds=((0.0, 2.0),),
        )
        normalization = optimization.final_parameters[0]
        prediction = normalization * expected
        evaluation = _evaluate(
            observed_array,
            prediction,
            covariance,
            n_fitted=1,
            raw_statistic=raw_statistic,
            convergence=optimization.convergence,
        )
        return BaselineFit(
            "M2",
            tuple(float(item) for item in prediction),
            evaluation,
            (("source_normalization", normalization),),
            optimization,
            (f"CROSS_SECTION_MODEL={model_choice}", "SOURCE_NORMALIZATION_PROFILED", "NO_MODEL_DECLARED_CORRECT"),
        )
    evaluation = _evaluate(observed_array, expected, covariance, n_fitted=0)
    return BaselineFit(
        "M2",
        tuple(float(item) for item in expected),
        evaluation,
        (),
        None,
        (f"CROSS_SECTION_MODEL={model_choice}", "NO_MODEL_DECLARED_CORRECT"),
    )


def cross_section_registry_baselines(
    observed: ArrayLike,
    expectation_by_model: Mapping[str, ArrayLike],
    covariance: CovarianceMatrix,
    *,
    model_registry: GalliumCrossSectionModelRegistry,
    isotope: str,
    profile_source_normalization: bool = False,
) -> tuple[BaselineFit, ...]:
    """Evaluate every registered model for one isotope without result-adaptive selection."""
    isotope_key = isotope.strip().casefold()
    eligible = tuple(
        model for model in model_registry.models
        if model.isotope.strip().casefold() == isotope_key
    )
    if not eligible:
        raise StatisticalInputError(f"No registered cross-section models exist for isotope {isotope!r}.")
    missing = tuple(model.model_id for model in eligible if model.model_id not in expectation_by_model)
    if missing:
        raise StatisticalInputError(
            "A complete preregistered cross-section scan requires expectations for every eligible model: "
            + ", ".join(missing)
        )
    return tuple(
        cross_section_variant_baseline(
            observed,
            expectation_by_model,
            covariance,
            model_choice=model.model_id,
            profile_source_normalization=profile_source_normalization,
            model_registry=model_registry,
        )
        for model in eligible
    )


def detector_systematic_baseline(
    observed: ArrayLike,
    expected: ArrayLike,
    covariance: CovarianceMatrix,
    detector_response: ArrayLike,
) -> BaselineFit:
    observations, conventional = _arrays(observed, expected, covariance)
    response = np.asarray(detector_response, dtype=np.float64)
    if response.shape != conventional.shape or not np.isfinite(response).all() or np.any(response <= 0):
        raise StatisticalInputError("Detector response must be a finite positive vector matching observations.")
    prediction = conventional * response
    evaluation = _evaluate(observations, prediction, covariance, n_fitted=0)
    return BaselineFit(
        "M4_DETECTOR_SYSTEMATIC",
        tuple(float(item) for item in prediction),
        evaluation,
        (),
        None,
        ("EXPLICIT_DECLARED_DETECTOR_RESPONSE",),
    )


def sterile_survival_probability(
    baselines_m: ArrayLike,
    energies_mev: ArrayLike,
    *,
    sin2_2theta_ee: float,
    delta_m2_ev2: float,
) -> NDArray[np.float64]:
    baselines = np.asarray(baselines_m, dtype=np.float64)
    energies = np.asarray(energies_mev, dtype=np.float64)
    if baselines.shape != energies.shape or baselines.ndim != 1 or baselines.size == 0:
        raise StatisticalInputError("Sterile baseline and energy vectors must be non-empty and equal length.")
    if np.any(baselines < 0) or np.any(energies <= 0) or not np.isfinite(baselines).all() or not np.isfinite(energies).all():
        raise StatisticalInputError("Sterile baselines/energies must be finite with L>=0 and E>0.")
    if not 0 <= sin2_2theta_ee <= 1 or delta_m2_ev2 < 0:
        raise StatisticalInputError("Sterile parameters require 0<=sin^2(2theta)<=1 and Delta m^2>=0.")
    phase = 1.267 * delta_m2_ev2 * baselines / energies
    return 1.0 - sin2_2theta_ee * np.sin(phase) ** 2


def sterile_3p1_baseline(
    observed: ArrayLike,
    expected: ArrayLike,
    covariance: CovarianceMatrix,
    baselines_m: ArrayLike,
    energies_mev: ArrayLike,
    *,
    initial: tuple[float, float] = (0.1, 1.0),
    bounds: tuple[tuple[float, float], tuple[float, float]] = ((0.0, 1.0), (0.0, 100.0)),
) -> BaselineFit:
    observations, conventional = _arrays(observed, expected, covariance)
    baselines = np.asarray(baselines_m, dtype=np.float64)
    energies = np.asarray(energies_mev, dtype=np.float64)
    if baselines.shape != observations.shape or energies.shape != observations.shape:
        raise BaselineSpecificationIncomplete(
            "M3 requires explicit per-observation baseline and energy integration inputs; no geometry fallback is allowed."
        )

    def prediction(values: np.ndarray) -> np.ndarray:
        return conventional * sterile_survival_probability(
            baselines,
            energies,
            sin2_2theta_ee=float(values[0]),
            delta_m2_ev2=float(values[1]),
        )

    raw_statistic, _ = covariance.quadratic_form(observations - conventional)
    optimization = optimize_baseline(
        lambda values: covariance.quadratic_form(observations - prediction(values))[0],
        model_id="M3",
        initial_values=initial,
        bounds=bounds,
    )
    fitted_prediction = prediction(np.asarray(optimization.final_parameters))
    evaluation = _evaluate(
        observations,
        fitted_prediction,
        covariance,
        n_fitted=2,
        raw_statistic=raw_statistic,
        convergence=optimization.convergence,
    )
    return BaselineFit(
        "M3",
        tuple(float(item) for item in fitted_prediction),
        evaluation,
        (
            ("sin2_2theta_ee", optimization.final_parameters[0]),
            ("delta_m2_ev2", optimization.final_parameters[1]),
        ),
        optimization,
        ("STANDARD_3P1_SURVIVAL", "EXPLICIT_PER_OBSERVATION_L_OVER_E", "NO_LSC_PARAMETERS"),
    )


def hierarchical_experiment_baseline(*_: object, **__: object) -> BaselineFit:
    raise BaselineSpecificationIncomplete(
        "M_HIERARCHICAL_EXPERIMENT remains SPECIFICATION_INCOMPLETE: no canonical hierarchy/prior was frozen in Step 03."
    )


def assert_baseline_execution_authorized(model_id: str) -> str:
    canonical = ALIASES.get(model_id.upper(), model_id.upper())
    if canonical in FROZEN_LSC_MODEL_IDS or canonical in {"M5", "M6", "LSC", "LSC_6_3_0"}:
        NoRefitPolicy().authorize(operation="FIT", target_model=canonical, parameter_scope="FROZEN_LSC_PARAMETERS")
        raise LSCStatisticalExecutionForbidden("Frozen LSC may not enter the independent baseline engine.")
    registry = baseline_model_registry()
    known = {item["model_id"] for item in registry["historical_models"]}
    if canonical.split("_")[0] not in known:
        raise StatisticalInputError(f"Unknown baseline model ID {model_id!r}.")
    return canonical
