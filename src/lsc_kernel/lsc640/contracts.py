"""Strict prediction contracts for LSC 6.4.0 A2/C/A."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Mapping

from lsc_kernel.lsc640.cross_section import GalliumCaptureCrossSection
from lsc_kernel.lsc640.errors import PredictionInputError, UnsupportedModelProfileError


_TOP_LEVEL_KEYS = {
    "schema_version",
    "model_version",
    "model_profile",
    "input_classification",
    "experiment_id",
    "observation_id",
    "source_isotope",
    "alpha_0",
    "lines",
    "analysis_context",
}
_LINE_KEYS = {
    "line_id",
    "energy_mev",
    "branching_fraction",
    "source_activity_bq",
    "exposure_seconds",
    "conventional_probability",
    "geometry_factor",
    "detector_efficiency",
}
_ANISOTROPIC_KEYS = {"tensor", "tensor_components", "preferred_axis", "anisotropic_amplitude", "directional"}


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
            raise PredictionInputError("Each line must be an object.")
        unknown = set(value) - _LINE_KEYS
        missing = _LINE_KEYS - set(value)
        if unknown or missing:
            raise PredictionInputError(
                "Line schema mismatch.",
                details={"unknown": sorted(unknown), "missing": sorted(missing)},
            )
        line_id = value["line_id"]
        if not isinstance(line_id, str) or not line_id:
            raise PredictionInputError("line_id must be a non-empty string.")
        branching = _finite_number(value["branching_fraction"], "branching_fraction", positive=True)
        probability = _finite_number(value["conventional_probability"], "conventional_probability", positive=True)
        efficiency = _finite_number(value["detector_efficiency"], "detector_efficiency", positive=True)
        if branching > 1.0 or probability > 1.0 or efficiency > 1.0:
            raise PredictionInputError("Fraction/probability/efficiency values cannot exceed one.")
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
    schema_version: str
    model_version: str
    model_profile: str
    input_classification: str
    experiment_id: str
    observation_id: str
    source_isotope: str
    alpha_0: float
    lines: tuple[LineInput, ...]
    analysis_context: dict[str, object]

    @classmethod
    def parse(
        cls,
        value: Mapping[str, Any],
        *,
        cross_section: GalliumCaptureCrossSection,
    ) -> "PredictionInput":
        if not isinstance(value, Mapping):
            raise PredictionInputError("Prediction input must be an object.")
        if _ANISOTROPIC_KEYS.intersection(value):
            raise UnsupportedModelProfileError("The A2/C/A profile has no anisotropic execution path.")
        unknown = set(value) - _TOP_LEVEL_KEYS
        missing = _TOP_LEVEL_KEYS - set(value)
        if unknown or missing:
            raise PredictionInputError(
                "Prediction input schema mismatch.",
                details={"unknown": sorted(unknown), "missing": sorted(missing)},
            )
        if value["schema_version"] != "1.0.0" or value["model_version"] != "6.4.0":
            raise PredictionInputError("Prediction schema/model version mismatch.")
        if value["model_profile"] != "A2/C/A":
            raise UnsupportedModelProfileError("Only the owner-authorized A2/C/A profile is supported.")
        classification = value["input_classification"]
        if classification not in {"AUTHORIZED_SOURCE_INPUT", "NON_PHYSICAL_TEST_FIXTURE"}:
            raise PredictionInputError("Unknown input classification.")
        for field in ("experiment_id", "observation_id", "source_isotope"):
            if not isinstance(value[field], str) or not value[field]:
                raise PredictionInputError(f"{field} must be a non-empty string.")
        context = value["analysis_context"]
        if not isinstance(context, Mapping):
            raise PredictionInputError("analysis_context must be an object.")
        required_context = {
            "role",
            "covariance_scenario_id",
            "nuisance_policy_id",
            "observed_outcomes_included",
            "BEST2_observed_data_accessed",
        }
        if set(context) != required_context:
            raise PredictionInputError("analysis_context schema mismatch.")
        if context["observed_outcomes_included"] is not False or context["BEST2_observed_data_accessed"] is not False:
            raise PredictionInputError("Prediction input may not contain observed outcomes or BEST-2 observations.")
        raw_lines = value["lines"]
        if not isinstance(raw_lines, list) or not raw_lines:
            raise PredictionInputError("lines must be a non-empty array.")
        lines = tuple(LineInput.parse(row) for row in raw_lines)
        if classification == "AUTHORIZED_SOURCE_INPUT":
            expected = cross_section.authoritative_lines(str(value["source_isotope"]))
            if len(lines) != len(expected):
                raise PredictionInputError("Authoritative source line count mismatch.")
            for provided, canonical in zip(lines, expected, strict=True):
                if (
                    provided.line_id != canonical["line_id"]
                    or provided.energy_mev != float(canonical["energy_mev"])
                    or provided.branching_fraction != float(canonical["branching_fraction"])
                ):
                    raise PredictionInputError("Authoritative source line identity was altered.")
        elif value["source_isotope"] != "NON_PHYSICAL_TEST_FIXTURE":
            raise PredictionInputError("Synthetic lines require the NON_PHYSICAL_TEST_FIXTURE isotope label.")
        alpha = cross_section.validate_alpha(_finite_number(value["alpha_0"], "alpha_0"))
        return cls(
            schema_version="1.0.0",
            model_version="6.4.0",
            model_profile="A2/C/A",
            input_classification=classification,
            experiment_id=str(value["experiment_id"]),
            observation_id=str(value["observation_id"]),
            source_isotope=str(value["source_isotope"]),
            alpha_0=alpha,
            lines=lines,
            analysis_context=dict(context),
        )
