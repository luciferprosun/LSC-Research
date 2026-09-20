"""One-dimensional, preregistered alpha_0 determination and verification."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from scipy.optimize import minimize_scalar

from lsc_kernel.lsc640.errors import NoRefitViolation
from lsc_kernel.lsc640.prefit import run_prefit_audit


RESULT_PATH = "LSC_6_4_0_ALPHA0_DETERMINATION_RESULT.json"


def _calculate(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    audit = run_prefit_audit(root)
    protocol = json.loads((root / "LSC_6_4_0_ALPHA0_DETERMINATION_PROTOCOL.json").read_text(encoding="utf-8"))
    observed = float(protocol["development_data"]["observed_values"][0])
    uncertainty = float(protocol["development_data"]["standard_uncertainties"][0])
    response = float(protocol["model_prediction"]["mean_F_m"])
    lower, upper = (float(item) for item in protocol["bounds"]["fit_bound"])

    def objective(alpha: float) -> float:
        prediction = 1.0 + float(alpha) * response
        return ((observed - prediction) / uncertainty) ** 2

    options = protocol["optimizer"]
    optimized = minimize_scalar(
        objective,
        bounds=(lower, upper),
        method="bounded",
        options={"xatol": float(options["xatol"]), "maxiter": int(options["maxiter"])},
    )
    unconstrained = (observed - 1.0) / response
    curvature_standard_error = uncertainty / abs(response)
    boundary_tolerance = float(protocol["convergence"]["boundary_tolerance"])
    constrained_alpha = float(optimized.x)
    boundary = (
        unconstrained < lower
        or unconstrained > upper
        or abs(constrained_alpha - lower) <= boundary_tolerance
        or abs(constrained_alpha - upper) <= boundary_tolerance
    )
    identifiable = math.isfinite(response) and abs(response) > 1e-12 and curvature_standard_error > 0.0
    success = bool(optimized.success) and identifiable and not boundary
    verdict = (
        "LSC_6_4_0_PARAMETER_DETERMINATION_SUCCEEDED"
        if success
        else "LSC_6_4_0_PARAMETER_DETERMINATION_FAILED"
    )
    return {
        "schema_version": "1.0.0",
        "document_kind": "LSC_6_4_0_ALPHA0_DETERMINATION_RESULT",
        "fit_run_id": protocol["fit_run_id"],
        "execution_classification": "RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION",
        "development_data_labels": ["MODEL_EXPOSED", "RETROSPECTIVE_NON_BLIND", "DEVELOPMENT_DATA"],
        "verdict": verdict,
        "success": success,
        "alpha_0_estimate_constrained": constrained_alpha,
        "alpha_0_estimate_unconstrained_diagnostic": unconstrained,
        "curvature_standard_error_diagnostic": curvature_standard_error,
        "certified_uncertainty_interval": None if not success else "profile_delta_chi_square_1",
        "objective_value": float(optimized.fun),
        "objective_at_null": objective(0.0),
        "objective_at_lower_bound": objective(lower),
        "objective_at_upper_bound": objective(upper),
        "fit_bound": [lower, upper],
        "optimizer": {
            "library": "scipy.optimize.minimize_scalar",
            "method": "bounded",
            "success": bool(optimized.success),
            "message": str(optimized.message),
            "function_evaluations": int(optimized.nfev),
            "iterations": int(optimized.nit),
        },
        "convergence": bool(optimized.success),
        "boundary_status": "BOUNDARY_DOMINATED" if boundary else "INTERIOR",
        "identifiability": "IDENTIFIABLE_ONE_DIMENSIONAL" if identifiable else "NON_IDENTIFIABLE",
        "failure_reasons": (
            [
                "unconstrained optimum lies below the frozen linear-response analysis domain",
                "bounded solution is boundary dominated",
                "the requested alpha_0 would be incompatible with the preregistered first-order validity criterion",
            ]
            if boundary
            else ([] if success else ["optimizer or identifiability failure"])
        ),
        "covariance_scenario": "COV_DIAGONAL",
        "covariance_classification": "ASSUMPTION_BASED_SENSITIVITY_ONLY",
        "profiled_nuisance_parameters": [],
        "pre_fit_audit": audit,
        "parameter_bundle_frozen": success,
        "refit_authorized": False,
        "response_or_bound_repair_after_result_authorized": False,
        "BEST2_observed_data_accessed": False,
        "BEST2_prediction_generated": False,
        "scientific_interpretation": "ADVERSE_PARAMETER_DETERMINATION_RESULT_NOT_VALIDATION" if not success else "RETROSPECTIVE_PARAMETER_DETERMINATION_NOT_VALIDATION",
    }


def execute_once(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    if (root / RESULT_PATH).exists():
        raise NoRefitViolation("The frozen alpha_0 determination result already exists; refit is forbidden.")
    return _calculate(root)


def verify_frozen_result(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    frozen = json.loads((root / RESULT_PATH).read_text(encoding="utf-8"))
    reproduced = _calculate(root)
    if frozen != reproduced:
        raise AssertionError("Frozen alpha_0 determination does not reproduce exactly.")
    return frozen
