"""Strict prediction contracts for LSC 6.5.0 exact finite dilation."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Mapping

from lsc_kernel.lsc650.cross_section import ExactGalliumCaptureCrossSection, sha256_file
from lsc_kernel.lsc650.errors import ParameterBundleError, PredictionInputError, UnsupportedModelProfileError


_TOP_LEVEL_KEYS = {
    "schema_version", "model_version", "model_profile", "response_variant",
    "cross_section_scenario_id", "source_line_payload_sha256", "input_classification", "experiment_id",
    "observation_id", "source_isotope", "alpha_0", "parameter_source",
    "lines", "analysis_context",
}
_LINE_KEYS = {
    "line_id", "energy_mev", "branching_fraction", "source_activity_bq",
    "exposure_seconds", "conventional_probability", "geometry_factor", "detector_efficiency",
}
_FORBIDDEN_PROFILE_KEYS = {
    "tensor", "tensor_components", "preferred_axis", "axis", "anisotropic_amplitude",
    "directional", "beta_0", "quadratic_coefficient", "second_lsc_coefficient",
}


def _finite_number(value: object, field: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PredictionInputError(f"{field} must be a finite number.")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0.0):
        raise PredictionInputError(f"{field} is outside its allowed numeric domain.")
    return result


@dataclass(frozen=True)
class LineInput:
    line_id: str
    energy_mev: float
    branching_fraction: float
    source_activity_bq: float
    exposure_seconds: float
    conventional_probability: float
    geometry_factor: float
    detector_efficiency: float

    @classmethod
    def parse(cls, value: object) -> "LineInput":
        if not isinstance(value, Mapping):
            raise PredictionInputError("Each source line must be an object.")
        unknown = set(value) - _LINE_KEYS
        missing = _LINE_KEYS - set(value)
        if unknown or missing:
            raise PredictionInputError("Source-line schema mismatch.", details={"unknown": sorted(unknown), "missing": sorted(missing)})
        line_id = value["line_id"]
        if not isinstance(line_id, str) or not line_id:
            raise PredictionInputError("line_id must be a non-empty string.")
        branching = _finite_number(value["branching_fraction"], "branching_fraction", positive=True)
        probability = _finite_number(value["conventional_probability"], "conventional_probability", positive=True)
        efficiency = _finite_number(value["detector_efficiency"], "detector_efficiency", positive=True)
        if branching > 1.0 or probability > 1.0 or efficiency > 1.0:
            raise PredictionInputError("Fractions, probability, and efficiency cannot exceed one.")
        return cls(
            line_id=line_id,
            energy_mev=_finite_number(value["energy_mev"], "energy_mev", positive=True),
            branching_fraction=branching,
            source_activity_bq=_finite_number(value["source_activity_bq"], "source_activity_bq", positive=True),
            exposure_seconds=_finite_number(value["exposure_seconds"], "exposure_seconds", positive=True),
            conventional_probability=probability,
            geometry_factor=_finite_number(value["geometry_factor"], "geometry_factor", positive=True),
            detector_efficiency=efficiency,
        )


@dataclass(frozen=True)
class PredictionInput:
    input_classification: str
    experiment_id: str
    observation_id: str
    source_isotope: str
    alpha_0: float
    parameter_source: dict[str, object]
    lines: tuple[LineInput, ...]
    analysis_context: dict[str, object]

    @classmethod
    def parse(cls, value: Mapping[str, Any], *, cross_section: ExactGalliumCaptureCrossSection) -> "PredictionInput":
        if not isinstance(value, Mapping):
            raise PredictionInputError("Prediction input must be an object.")
        if _FORBIDDEN_PROFILE_KEYS.intersection(value):
            raise UnsupportedModelProfileError("LSC 6.5.0 has no tensor, axis, anisotropic, or second-parameter path.")
        unknown = set(value) - _TOP_LEVEL_KEYS
        missing = _TOP_LEVEL_KEYS - set(value)
        if unknown or missing:
            raise PredictionInputError("Prediction input schema mismatch.", details={"unknown": sorted(unknown), "missing": sorted(missing)})
        if value["schema_version"] != "1.0.0" or value["model_version"] != "6.5.0":
            raise PredictionInputError("Prediction schema/model version mismatch.")
        if value["model_profile"] != "EXACT_FINITE_A2/C/A" or value["response_variant"] != "EXACT_CAPTURE_ARGUMENT_DILATION":
            raise UnsupportedModelProfileError("Only the owner-authorized exact A2/C/A profile is supported.")
        if value["cross_section_scenario_id"] != cross_section.SCENARIO_ID:
            raise PredictionInputError("The cross-section scenario is unversioned or unsupported.")
        if value["source_line_payload_sha256"] != cross_section.identity.source_line_payload_sha256:
            raise PredictionInputError("The source-line payload hash is absent or mismatched.")
        classification = value["input_classification"]
        if classification not in {"AUTHORIZED_SOURCE_INPUT", "NON_PHYSICAL_TEST_FIXTURE"}:
            raise PredictionInputError("Unknown input classification.")
        for field in ("experiment_id", "observation_id", "source_isotope"):
            if not isinstance(value[field], str) or not value[field]:
                raise PredictionInputError(f"{field} must be a non-empty string.")
        raw_lines = value["lines"]
        if not isinstance(raw_lines, list) or not raw_lines:
            raise PredictionInputError("lines must be a non-empty array.")
        lines = tuple(LineInput.parse(row) for row in raw_lines)
        if classification == "AUTHORIZED_SOURCE_INPUT":
            expected = cross_section.authoritative_lines(str(value["source_isotope"]))
            if len(lines) != len(expected):
                raise PredictionInputError("Authoritative source-line count mismatch.")
            for provided, canonical in zip(lines, expected, strict=True):
                if provided.line_id != canonical["line_id"] or provided.energy_mev != float(canonical["energy_mev"]) or provided.branching_fraction != float(canonical["branching_fraction"]):
                    raise PredictionInputError("Authoritative source-line identity was altered.")
        elif value["source_isotope"] != "NON_PHYSICAL_TEST_FIXTURE":
            raise PredictionInputError("Synthetic lines require the NON_PHYSICAL_TEST_FIXTURE isotope label.")
        parameter_source = value["parameter_source"]
        if not isinstance(parameter_source, Mapping) or set(parameter_source) != {"kind", "bundle_sha256"}:
            raise PredictionInputError("parameter_source schema mismatch.")
        kind = parameter_source["kind"]
        allowed_kinds = {"NON_PHYSICAL_TEST_FIXTURE", "PREFIT_AUTHORIZED_DEVELOPMENT", "FROZEN_PARAMETER_BUNDLE"}
        if kind not in allowed_kinds:
            raise PredictionInputError("Unknown parameter-source kind.")
        if kind == "NON_PHYSICAL_TEST_FIXTURE" and classification != "NON_PHYSICAL_TEST_FIXTURE":
            raise PredictionInputError("Fixture parameter source requires fixture input classification.")
        alpha = cross_section.validate_alpha(_finite_number(value["alpha_0"], "alpha_0"), (line.energy_mev for line in lines))
        if kind == "FROZEN_PARAMETER_BUNDLE":
            bundle_path = cross_section.repository_root / "LSC_6_5_0_PARAMETER_BUNDLE.json"
            if not bundle_path.is_file() or parameter_source["bundle_sha256"] != sha256_file(bundle_path):
                raise ParameterBundleError("Frozen parameter-bundle hash is absent or mismatched.")
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            if float(bundle["parameter"]["value"]) != alpha or bundle.get("no_refit") is not True:
                raise ParameterBundleError("Prediction alpha does not match the frozen no-refit bundle.")
        elif parameter_source["bundle_sha256"] is not None:
            raise PredictionInputError("Non-bundle parameter sources cannot claim a bundle hash.")
        context = value["analysis_context"]
        if not isinstance(context, Mapping):
            raise PredictionInputError("analysis_context must be an object.")
        required_context = {"role", "covariance_scenario_id", "nuisance_policy_id", "observed_outcomes_included", "BEST2_observed_data_accessed"}
        if set(context) != required_context:
            raise PredictionInputError("analysis_context schema mismatch.")
        if context["role"] not in {"PREDICTION_ONLY", "DEVELOPMENT_DATA", "RETROSPECTIVE_SMOKE", "NON_PHYSICAL_TEST"}:
            raise PredictionInputError("Unknown analysis role.")
        if context["observed_outcomes_included"] is not False or context["BEST2_observed_data_accessed"] is not False:
            raise PredictionInputError("The evaluator input may not carry observed outcomes or BEST-2 observations.")
        return cls(
            input_classification=str(classification),
            experiment_id=str(value["experiment_id"]),
            observation_id=str(value["observation_id"]),
            source_isotope=str(value["source_isotope"]),
            alpha_0=alpha,
            parameter_source=dict(parameter_source),
            lines=lines,
            analysis_context=dict(context),
        )
