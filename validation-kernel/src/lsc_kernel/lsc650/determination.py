"""Single preregistered exact-dilation alpha_0 determination."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from scipy.optimize import brentq, minimize_scalar

from lsc_kernel.lsc650.evaluator import LSC650Evaluator
from lsc_kernel.lsc650.errors import NoRefitViolation
from lsc_kernel.lsc650.prefit import run_prefit_audit


RESULT_PATH = "LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json"


def _canonical_write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=False, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def _prediction_payload(root: Path, alpha_0: float) -> dict[str, object]:
    lines_doc = json.loads((root / "external_physics/gallium_capture/source_lines_prc108_035502.json").read_text(encoding="utf-8"))
    factors = {
        "source_activity_bq": 1.0,
        "exposure_seconds": 1.0,
        "conventional_probability": 1.0,
        "geometry_factor": 1.0,
        "detector_efficiency": 1.0,
    }
    return {
        "schema_version": "1.0.0",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "response_variant": "EXACT_CAPTURE_ARGUMENT_DILATION",
        "cross_section_scenario_id": "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE",
        "source_line_payload_sha256": "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e",
        "input_classification": "AUTHORIZED_SOURCE_INPUT",
        "experiment_id": "BEST",
        "observation_id": "BEST:zone=inner:published_aggregate_ratio",
        "source_isotope": "Cr51",
        "alpha_0": float(alpha_0),
        "parameter_source": {"kind": "PREFIT_AUTHORIZED_DEVELOPMENT", "bundle_sha256": None},
        "lines": [{**row, **factors} for row in lines_doc["isotopes"]["Cr51"]],
        "analysis_context": {
            "role": "DEVELOPMENT_DATA",
            "covariance_scenario_id": "COV_DIAGONAL",
            "nuisance_policy_id": "PUBLISHED_AGGREGATE_TOTAL_UNCERTAINTY_NO_ADDITIONAL_PROFILED_NUISANCE",
            "observed_outcomes_included": False,
            "BEST2_observed_data_accessed": False,
        },
    }


def calculate_frozen_determination(repository_root: Path | str) -> dict[str, object]:
    """Pure deterministic recalculation; it never writes or authorizes a second fit."""
    root = Path(repository_root).resolve()
    audit = run_prefit_audit(root)
    protocol = json.loads((root / "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json").read_text(encoding="utf-8"))
    evaluator = LSC650Evaluator.from_repository(root)
    observed = float(protocol["development_data"]["observed_values"][0])
    uncertainty = float(protocol["development_data"]["standard_uncertainties"][0])
    lower, upper = (float(item) for item in protocol["bounds"]["fit_bound"])

    def prediction(alpha: float) -> float:
        return float(evaluator.predict(_prediction_payload(root, float(alpha)))["R_pred"])

    def objective(alpha: float) -> float:
        return ((observed - prediction(alpha)) / uncertainty) ** 2

    options = protocol["optimizer"]
    optimized = minimize_scalar(
        objective,
        bounds=(lower, upper),
        method="bounded",
        options={"xatol": float(options["xatol"]), "maxiter": int(options["maxiter"])},
    )
    estimate = float(optimized.x)
    minimum = float(optimized.fun)
    boundary_tolerance = float(protocol["convergence"]["boundary_tolerance"])
    boundary = abs(estimate - lower) <= boundary_tolerance or abs(estimate - upper) <= boundary_tolerance
    step = float(protocol["identifiability"]["finite_difference_step"])
    derivative = (prediction(estimate + step) - prediction(estimate - step)) / (2.0 * step)
    curvature = (objective(estimate + step) - 2.0 * objective(estimate) + objective(estimate - step)) / (step * step)
    identifiable = math.isfinite(derivative) and abs(derivative) > 1e-8 and math.isfinite(curvature) and curvature > 0.0
    target = minimum + 1.0
    left_interval: float | None = None
    right_interval: float | None = None
    if objective(lower) >= target and estimate > lower:
        left_interval = float(brentq(lambda alpha: objective(alpha) - target, lower, estimate, xtol=1e-13, rtol=1e-14, maxiter=1000))
    if objective(upper) >= target and estimate < upper:
        right_interval = float(brentq(lambda alpha: objective(alpha) - target, estimate, upper, xtol=1e-13, rtol=1e-14, maxiter=1000))
    two_sided = left_interval is not None and right_interval is not None
    success = bool(optimized.success) and math.isfinite(estimate) and math.isfinite(minimum) and identifiable and not boundary and two_sided
    failure_reasons: list[str] = []
    if not optimized.success:
        failure_reasons.append("optimizer did not converge")
    if boundary:
        failure_reasons.append("result is boundary dominated")
    if not identifiable:
        failure_reasons.append("alpha_0 is not locally identifiable")
    if not two_sided:
        failure_reasons.append("two-sided DeltaChi2=1 interval is unavailable inside the frozen domain")
    return {
        "schema_version": "1.0.0",
        "document_kind": "LSC_6_5_0_ALPHA_DETERMINATION_RESULT",
        "fit_run_id": protocol["fit_run_id"],
        "fit_execution_count": 1,
        "execution_classification": "RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION",
        "development_data_labels": ["MODEL_EXPOSED", "POST_6_4_DEVELOPMENT", "RETROSPECTIVE_NON_BLIND", "DEVELOPMENT_DATA"],
        "verdict": protocol["success_verdict"] if success else protocol["failure_verdict"],
        "success": success,
        "alpha_0_estimate": estimate,
        "certified_profile_delta_chi_square_1_interval": [left_interval, right_interval] if success else None,
        "objective_value": minimum,
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
        "prediction_derivative_at_estimate": derivative,
        "objective_curvature_at_estimate": curvature,
        "failure_reasons": failure_reasons,
        "unconstrained_diagnostic_predeclared": False,
        "unconstrained_diagnostic_performed": False,
        "covariance_scenario": "COV_DIAGONAL",
        "covariance_classification": "ASSUMPTION_BASED_SENSITIVITY_ONLY",
        "profiled_nuisance_parameters": [],
        "pre_fit_audit": audit,
        "parameter_bundle_frozen": success,
        "refit_authorized": False,
        "BEST2_observed_data_accessed": False,
        "BEST2_prediction_generated": False,
        "scientific_interpretation": "RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION_NOT_VALIDATION" if success else "ADVERSE_PARAMETER_DETERMINATION_RESULT_NOT_VALIDATION",
    }


def execute_once(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    target = root / RESULT_PATH
    if target.exists():
        raise NoRefitViolation("The single frozen LSC 6.5.0 determination result already exists; refit is forbidden.")
    result = calculate_frozen_determination(root)
    _canonical_write(target, result)
    return result


def verify_frozen_result(repository_root: Path | str) -> dict[str, object]:
    root = Path(repository_root).resolve()
    frozen = json.loads((root / RESULT_PATH).read_text(encoding="utf-8"))
    reproduced = calculate_frozen_determination(root)
    if frozen != reproduced:
        raise AssertionError("The frozen LSC 6.5.0 determination does not reproduce exactly.")
    return frozen
