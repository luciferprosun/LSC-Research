"""Deterministic production evaluator for owner-authorized LSC 6.4.0 A2/C/A."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

from lsc_kernel.lsc640.contracts import PredictionInput
from lsc_kernel.lsc640.cross_section import GalliumCaptureCrossSection, canonical_hash
from lsc_kernel.lsc640.errors import InvalidBaselineMeasure


class LSC640Evaluator:
    """One-parameter trace-only evaluator with no fitting or hidden defaults."""

    def __init__(self, cross_section: GalliumCaptureCrossSection) -> None:
        self.cross_section = cross_section

    @classmethod
    def from_repository(cls, repository_root: Path | str) -> "LSC640Evaluator":
        return cls(GalliumCaptureCrossSection.from_repository(repository_root))

    def predict(self, payload: Mapping[str, Any]) -> dict[str, object]:
        request = PredictionInput.parse(payload, cross_section=self.cross_section)
        input_hash = canonical_hash(payload)
        denominator = 0.0
        numerator = 0.0
        line_results: list[dict[str, object]] = []
        for line in request.lines:
            sigma = self.cross_section.sigma(line.energy_mev)
            response = self.cross_section.response(line.energy_mev)
            baseline_weight = (
                line.branching_fraction
                * line.source_activity_bq
                * line.exposure_seconds
                * line.conventional_probability
                * line.geometry_factor
                * line.detector_efficiency
                * sigma
            )
            if not math.isfinite(baseline_weight) or baseline_weight <= 0.0:
                raise InvalidBaselineMeasure("A line produced a non-positive baseline weight.")
            denominator += baseline_weight
            numerator += baseline_weight * response
            line_results.append(
                {
                    "line_id": line.line_id,
                    "energy_mev": line.energy_mev,
                    "sigma_1e_minus_46_cm2": sigma,
                    "F_m": response,
                    "baseline_weight": baseline_weight,
                    "S_a": request.alpha_0 * response,
                }
            )
        if not math.isfinite(denominator) or denominator <= 0.0:
            raise InvalidBaselineMeasure("Normalized baseline denominator is not finite and positive.")
        mean_response = numerator / denominator
        prediction = 1.0 + request.alpha_0 * mean_response
        if not all(math.isfinite(item) for item in (mean_response, prediction)) or prediction <= 0.0:
            raise InvalidBaselineMeasure("The final linear response is not finite and positive.")
        warnings: list[str] = [
            "A2 is a NEW_PHYSICAL_HYPOTHESIS_6_4_0, not recovered LSC 6.3.0 physics.",
            "The logarithmic derivative is representation-defined by the frozen spline.",
        ]
        if request.input_classification == "NON_PHYSICAL_TEST_FIXTURE":
            warnings.append("NON_PHYSICAL_TEST_FIXTURE: output is not an experimental prediction.")
        return {
            "schema_version": "1.0.0",
            "model_version": "6.4.0",
            "model_profile": "A2/C/A",
            "model_sha256": self.cross_section.identity.model_sha256,
            "response_specification_sha256": self.cross_section.identity.response_spec_sha256,
            "cross_section_payload_sha256": self.cross_section.identity.payload_sha256,
            "source_line_payload_sha256": self.cross_section.identity.line_payload_sha256,
            "input_sha256": input_hash,
            "input_classification": request.input_classification,
            "experiment_id": request.experiment_id,
            "observation_id": request.observation_id,
            "source_isotope": request.source_isotope,
            "alpha_0": request.alpha_0,
            "per_line": line_results,
            "baseline_denominator": denominator,
            "mean_F_m": mean_response,
            "R_pred": prediction,
            "applicable_domain_status": "PASS",
            "anisotropic_sector": "DISABLED",
            "warnings": warnings,
            "blockers": [],
            "provenance_references": [
                "external_physics/gallium_capture/PROVENANCE_MANIFEST.json",
                "spec/LSC_6_4_0_RESPONSE_A2.json",
            ],
            "analysis_context": request.analysis_context,
        }

    def predict_json(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(self.predict(payload), sort_keys=True, separators=(",", ":"), allow_nan=False)
