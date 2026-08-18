"""Policy-gated deterministic wrappers around SciPy optimizers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Sequence

import numpy as np
from scipy.optimize import minimize

from lsc_kernel.validation.policies import NoRefitPolicy
from lsc_kernel.validation.registries import baseline_model_registry

from .errors import StatisticalInputError


_FIT_POLICY_ALIASES = {
    "M_CONSTANT_DEFICIT": "M1",
    "M_CROSS_SECTION_VARIANT": "M2",
    "M_STERILE_3P1": "M3",
    "M_DETECTOR_SYSTEMATIC": "M4",
    "M_EXPERIMENT_NORMALIZATION": "M4",
    "M_HIERARCHICAL_EXPERIMENT": "M4",
    "M4_DETECTOR_SYSTEMATIC": "M4",
    "M4_EXPERIMENT_NORMALIZATION": "M4",
    "M4_HIERARCHICAL_EXPERIMENT": "M4",
}


def _authorize_registry_fit(model_id: str) -> str:
    """Require an exact Step 03 registry entry whose fit flag is true."""
    requested = model_id.upper()
    canonical = _FIT_POLICY_ALIASES.get(requested, requested)
    # This call preserves the project's required FrozenModelRefitForbidden
    # exception before any generic registry error can be raised.
    NoRefitPolicy().authorize(
        operation="FIT",
        target_model=canonical,
        parameter_scope="BASELINE_PARAMETERS",
    )
    definitions = {
        str(row["model_id"]): row
        for row in baseline_model_registry()["historical_models"]
    }
    definition = definitions.get(canonical)
    if definition is None:
        raise StatisticalInputError(f"Model {model_id!r} is not present in the frozen baseline registry.")
    if not bool(definition["fitting_allowed"]):
        raise StatisticalInputError(f"Model {canonical} is not marked fitting_allowed in the frozen registry.")
    return canonical


@dataclass(frozen=True, slots=True)
class OptimizationResult:
    optimizer: str
    initial_values: tuple[float, ...]
    parameter_bounds: tuple[tuple[float | None, float | None], ...]
    tolerance: float
    convergence: bool
    number_of_evaluations: int
    final_parameters: tuple[float, ...]
    final_statistic: float
    message: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def optimize_baseline(
    objective: Callable[[np.ndarray], float],
    *,
    model_id: str,
    initial_values: Sequence[float],
    bounds: Sequence[tuple[float | None, float | None]],
    parameter_scope: str = "BASELINE_PARAMETERS",
    tolerance: float = 1e-10,
    method: str = "L-BFGS-B",
) -> OptimizationResult:
    canonical_model = _authorize_registry_fit(model_id)
    NoRefitPolicy().authorize(
        operation="FIT",
        target_model=canonical_model,
        parameter_scope=parameter_scope,
    )
    initial = np.asarray(initial_values, dtype=np.float64)
    if initial.ndim != 1 or initial.size == 0 or not np.isfinite(initial).all():
        raise StatisticalInputError("Optimizer initial values must be a non-empty finite vector.")
    if not np.isfinite(float(tolerance)) or tolerance <= 0:
        raise StatisticalInputError("Optimizer tolerance must be finite and strictly positive.")
    normalized_bounds = tuple((low, high) for low, high in bounds)
    if len(normalized_bounds) != initial.size:
        raise StatisticalInputError("One explicit bound pair is required per optimization parameter.")
    for index, (low, high) in enumerate(normalized_bounds):
        if low is not None and not np.isfinite(float(low)):
            raise StatisticalInputError("Optimizer lower bounds must be finite when supplied.")
        if high is not None and not np.isfinite(float(high)):
            raise StatisticalInputError("Optimizer upper bounds must be finite when supplied.")
        if low is not None and high is not None and low > high:
            raise StatisticalInputError("Optimizer lower bounds cannot exceed upper bounds.")
        if low is not None and initial[index] < low:
            raise StatisticalInputError("Optimizer initial value is below its lower bound.")
        if high is not None and initial[index] > high:
            raise StatisticalInputError("Optimizer initial value is above its upper bound.")

    def guarded(values: np.ndarray) -> float:
        statistic = float(objective(values))
        if not np.isfinite(statistic):
            raise StatisticalInputError("Objective returned a non-finite statistic.")
        return statistic

    result = minimize(
        guarded,
        initial,
        method=method,
        bounds=normalized_bounds,
        tol=float(tolerance),
        options={"ftol": float(tolerance), "gtol": float(tolerance), "maxiter": 10000, "maxls": 50},
    )
    return OptimizationResult(
        optimizer=method,
        initial_values=tuple(float(item) for item in initial),
        parameter_bounds=normalized_bounds,
        tolerance=float(tolerance),
        convergence=bool(result.success),
        number_of_evaluations=int(result.nfev),
        final_parameters=tuple(float(item) for item in result.x),
        final_statistic=float(result.fun),
        message=str(result.message),
    )
