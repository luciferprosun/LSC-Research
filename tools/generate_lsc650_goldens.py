#!/usr/bin/env python3
"""Generate LSC 6.5.0 golden values using only the independent reference path."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from lsc_kernel.lsc650.reference import NaturalSplineReference650, reference_exact_prediction


ROOT = Path(__file__).resolve().parents[1]
LINES_PATH = "external_physics/gallium_capture/source_lines_prc108_035502.json"
LINES_HASH = "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e"
SCENARIO = "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE"
LOWER = -0.5747389495096434
UPPER = 3.607238025076703


def context(role: str = "NON_PHYSICAL_TEST") -> dict[str, object]:
    return {
        "role": role,
        "covariance_scenario_id": "NONE_PREDICTION_ONLY",
        "nuisance_policy_id": "NONE_PREDICTION_ONLY",
        "observed_outcomes_included": False,
        "BEST2_observed_data_accessed": False,
    }


def base_template(isotope: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "response_variant": "EXACT_CAPTURE_ARGUMENT_DILATION",
        "cross_section_scenario_id": SCENARIO,
        "source_line_payload_sha256": LINES_HASH,
        "input_classification": "AUTHORIZED_SOURCE_INPUT",
        "experiment_id": "GOLDEN_EXPERIMENT",
        "observation_id": f"GOLDEN_{isotope.upper()}",
        "source_isotope": isotope,
        "alpha_0": 0.0,
        "parameter_source": {"kind": "PREFIT_AUTHORIZED_DEVELOPMENT", "bundle_sha256": None},
        "authoritative_line_source": f"{LINES_PATH}#isotopes/{isotope}",
        "conventional_factors": {
            "source_activity_bq": 1.0,
            "exposure_seconds": 1.0,
            "conventional_probability": 1.0,
            "geometry_factor": 1.0,
            "detector_efficiency": 1.0,
        },
        "analysis_context": context(),
    }


def synthetic_template(weighted: bool) -> dict[str, object]:
    lines = (
        [
            {"line_id": "S-050", "energy_mev": 0.5, "branching_fraction": 0.25, "source_activity_bq": 1.0, "exposure_seconds": 2.0, "conventional_probability": 0.9, "geometry_factor": 0.8, "detector_efficiency": 0.95},
            {"line_id": "S-090", "energy_mev": 0.9, "branching_fraction": 0.75, "source_activity_bq": 1.5, "exposure_seconds": 1.0, "conventional_probability": 0.8, "geometry_factor": 1.2, "detector_efficiency": 0.85},
        ]
        if weighted else
        [{"line_id": "S-060", "energy_mev": 0.6, "branching_fraction": 1.0, "source_activity_bq": 1.0, "exposure_seconds": 1.0, "conventional_probability": 1.0, "geometry_factor": 1.0, "detector_efficiency": 1.0}]
    )
    return {
        "schema_version": "1.0.0",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "response_variant": "EXACT_CAPTURE_ARGUMENT_DILATION",
        "cross_section_scenario_id": SCENARIO,
        "source_line_payload_sha256": LINES_HASH,
        "input_classification": "NON_PHYSICAL_TEST_FIXTURE",
        "experiment_id": "NON_PHYSICAL_TEST_FIXTURE",
        "observation_id": "SYNTHETIC_WEIGHTED" if weighted else "SYNTHETIC_SINGLE",
        "source_isotope": "NON_PHYSICAL_TEST_FIXTURE",
        "alpha_0": 0.0,
        "parameter_source": {"kind": "NON_PHYSICAL_TEST_FIXTURE", "bundle_sha256": None},
        "lines": lines,
        "analysis_context": context(),
    }


def apply_override(payload: dict[str, object], key: str, value: object) -> None:
    target: object = payload
    parts = key.split(".")
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]  # type: ignore[index]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value  # type: ignore[index]


def materialize(templates: dict[str, dict[str, object]], case: dict[str, object]) -> dict[str, object]:
    payload = copy.deepcopy(templates[str(case["template"])])
    source_ref = payload.pop("authoritative_line_source", None)
    factors = payload.pop("conventional_factors", None)
    if source_ref:
        path_text, pointer = str(source_ref).split("#isotopes/", 1)
        document = json.loads((ROOT / path_text).read_text(encoding="utf-8"))
        payload["lines"] = [{**row, **factors} for row in document["isotopes"][pointer]]
    for key, value in case.get("overrides", {}).items():  # type: ignore[union-attr]
        apply_override(payload, key, value)
    return payload


def main() -> int:
    templates = {
        "AUTHORIZED_CR51": base_template("Cr51"),
        "AUTHORIZED_AR37": base_template("Ar37"),
        "SYNTHETIC_SINGLE": synthetic_template(False),
        "SYNTHETIC_WEIGHTED": synthetic_template(True),
    }
    success_rows = [
        ("GV650_01_CR51_NULL", "AUTHORIZED_CR51", {"alpha_0": 0.0}, "analytic null plus independent reference"),
        ("GV650_02_AR37_NULL", "AUTHORIZED_AR37", {"alpha_0": 0.0}, "analytic null plus independent reference"),
        ("GV650_03_CR51_SMALL_POSITIVE", "AUTHORIZED_CR51", {"alpha_0": 1e-6}, "first-order bridge region"),
        ("GV650_04_CR51_SMALL_NEGATIVE", "AUTHORIZED_CR51", {"alpha_0": -1e-6}, "first-order bridge region"),
        ("GV650_05_AR37_POSITIVE", "AUTHORIZED_AR37", {"alpha_0": 0.05}, "independent reference"),
        ("GV650_06_AR37_NEGATIVE", "AUTHORIZED_AR37", {"alpha_0": -0.05}, "independent reference"),
        ("GV650_07_CR51_MODERATE_POSITIVE", "AUTHORIZED_CR51", {"alpha_0": 0.5}, "exact nonlinear region"),
        ("GV650_08_CR51_MODERATE_NEGATIVE", "AUTHORIZED_CR51", {"alpha_0": -0.25}, "exact nonlinear region"),
        ("GV650_09_AR37_POSITIVE", "AUTHORIZED_AR37", {"alpha_0": 1.0}, "exact nonlinear region"),
        ("GV650_10_AR37_NEGATIVE", "AUTHORIZED_AR37", {"alpha_0": -0.4}, "exact nonlinear region"),
        ("GV650_11_LABEL_A", "AUTHORIZED_CR51", {"alpha_0": 0.1, "experiment_id": "LABEL_A"}, "universal-sharing pair"),
        ("GV650_12_LABEL_B", "AUTHORIZED_CR51", {"alpha_0": 0.1, "experiment_id": "LABEL_B"}, "universal-sharing pair"),
        ("GV650_13_SYNTH_SINGLE_POSITIVE", "SYNTHETIC_SINGLE", {"alpha_0": 0.2}, "independent one-line reference"),
        ("GV650_14_SYNTH_SINGLE_NEGATIVE", "SYNTHETIC_SINGLE", {"alpha_0": -0.2}, "independent one-line reference"),
        ("GV650_15_SYNTH_WEIGHTED_POSITIVE", "SYNTHETIC_WEIGHTED", {"alpha_0": 0.3}, "independent weighted reference"),
        ("GV650_16_SYNTH_WEIGHTED_NEGATIVE", "SYNTHETIC_WEIGHTED", {"alpha_0": -0.3}, "independent weighted reference"),
        ("GV650_17_LOWER_DOMAIN_VICINITY", "AUTHORIZED_CR51", {"alpha_0": LOWER + 1e-10}, "closed-support vicinity"),
        ("GV650_18_UPPER_DOMAIN_VICINITY", "AUTHORIZED_AR37", {"alpha_0": UPPER - 1e-10}, "closed-support vicinity"),
        ("GV650_19_CR51_LARGE_POSITIVE", "AUTHORIZED_CR51", {"alpha_0": 0.75}, "exact nonlinear region"),
        ("GV650_20_AR37_LARGE_POSITIVE", "AUTHORIZED_AR37", {"alpha_0": 2.0}, "exact nonlinear region"),
    ]
    error_rows = [
        ("GV650_21_LOWER_DOMAIN_VIOLATION", "AUTHORIZED_CR51", {"alpha_0": LOWER - 1e-12}, "FAIL_CLOSED_UNSUPPORTED_DOMAIN"),
        ("GV650_22_UPPER_DOMAIN_VIOLATION", "AUTHORIZED_AR37", {"alpha_0": UPPER + 1e-12}, "FAIL_CLOSED_UNSUPPORTED_DOMAIN"),
        ("GV650_23_SOURCE_LINE_MUTATION", "AUTHORIZED_CR51", {"lines.0.energy_mev": 0.752401}, "FAIL_CLOSED_INVALID_PREDICTION_INPUT"),
        ("GV650_24_SOURCE_HASH_VIOLATION", "AUTHORIZED_CR51", {"source_line_payload_sha256": "0" * 64}, "FAIL_CLOSED_INVALID_PREDICTION_INPUT"),
        ("GV650_25_TENSOR_REJECTED", "AUTHORIZED_CR51", {"tensor": [[0.0, 0.0, 0.0]] * 3}, "FAIL_CLOSED_UNSUPPORTED_MODEL_PROFILE"),
        ("GV650_26_SECOND_PARAMETER_REJECTED", "AUTHORIZED_CR51", {"beta_0": 0.1}, "FAIL_CLOSED_UNSUPPORTED_MODEL_PROFILE"),
        ("GV650_27_RESPONSE_VARIANT_REJECTED", "AUTHORIZED_CR51", {"response_variant": "LINEAR_A2"}, "FAIL_CLOSED_UNSUPPORTED_MODEL_PROFILE"),
        ("GV650_28_UNVERSIONED_CROSS_SECTION", "AUTHORIZED_CR51", {"cross_section_scenario_id": "UNVERSIONED"}, "FAIL_CLOSED_INVALID_PREDICTION_INPUT"),
        ("GV650_29_EXTRAPOLATED_ENERGY", "SYNTHETIC_SINGLE", {"lines.0.energy_mev": 0.239}, "FAIL_CLOSED_UNSUPPORTED_DOMAIN"),
    ]
    reference = NaturalSplineReference650.from_csv(ROOT / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv")
    vectors: list[dict[str, object]] = []
    for identifier, template, overrides, verification in success_rows:
        case: dict[str, object] = {"id": identifier, "template": template, "overrides": overrides}
        payload = materialize(templates, case)
        result = reference_exact_prediction(reference, payload["lines"], float(payload["alpha_0"]))  # type: ignore[arg-type]
        case.update({
            "expected": {
                "baseline_denominator": result["baseline_denominator"],
                "exact_numerator": result["exact_numerator"],
                "R_pred": result["R_pred"],
                "per_line_K_m": [row["K_m"] for row in result["per_line"]],
            },
            "tolerance": 2e-9 if "DOMAIN_VICINITY" in identifier else 2e-12,
            "verification": verification,
        })
        vectors.append(case)
    for identifier, template, overrides, expected_error in error_rows:
        vectors.append({"id": identifier, "template": template, "overrides": overrides, "expected_error": expected_error})
    document = {
        "schema_version": "1.0.0",
        "document_kind": "LSC_6_5_0_GOLDEN_NUMERICAL_VECTORS",
        "model_version": "6.5.0",
        "model_profile": "EXACT_FINITE_A2/C/A",
        "generation": "Expected values produced only by the independent stdlib natural-spline and direct numerator implementation; production code is separately compared at verification time.",
        "templates": templates,
        "vectors": vectors,
        "success_vector_count": len(success_rows),
        "fail_closed_vector_count": len(error_rows),
        "observed_gallium_deficits_used": False,
        "BEST2_observed_data_used": False,
    }
    target = ROOT / "spec/LSC_6_5_0_GOLDEN_VECTORS.json"
    target.write_text(json.dumps(document, indent=2, sort_keys=False, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
