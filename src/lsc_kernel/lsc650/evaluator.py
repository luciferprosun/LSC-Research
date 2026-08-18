"""Deterministic production evaluator for exact LSC 6.5.0 finite dilation."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

from lsc_kernel.lsc650.contracts import PredictionInput
from lsc_kernel.lsc650.cross_section import ExactGalliumCaptureCrossSection, canonical_hash
from lsc_kernel.lsc650.errors import InvalidBaselineMeasure


class LSC650Evaluator:
    """One-parameter exact scalar evaluator with no fitting or hidden defaults."""

    def __init__(self, cross_section: ExactGalliumCaptureCrossSection) -> None:
        self.cross_section = cross_section

    @classmethod
    def from_repository(cls, repository_root: Path | str) -> "LSC650Evaluator":
        return cls(ExactGalliumCaptureCrossSection.from_repository(repository_root))

    def predict(self, payload: Mapping[str, Any]) -> dict[str, object]:
        request = PredictionInput.parse(payload, cross_section=self.cross_section)
        denominator_terms: list[float] = []
        numerator_terms: list[float] = []
        numerator_direct_terms: list[float] = []
        line_results: list[dict[str, object]] = []
        for line in request.lines:
            sigma_baseline = self.cross_section.sigma(line.energy_mev)
            ratio, transformed, boundary_normalized = self.cross_section.exact_ratio(line.energy_mev, request.alpha_0)
            prefactor = (
                line.branching_fraction * line.source_activity_bq * line.exposure_seconds
                * line.conventional_probability * line.geometry_factor * line.detector_efficiency
            )
            baseline_weight = prefactor * sigma_baseline
            numerator_term = baseline_weight * ratio
            direct_term = prefactor * self.cross_section.sigma(transformed)
            if not all(math.isfinite(value) and value > 0.0 for value in (prefactor, baseline_weight, numerator_term, direct_term)):
                raise InvalidBaselineMeasure("A source line produced a non-positive baseline or transformed weight.")
            denominator_terms.append(baseline_weight)
            numerator_terms.append(numerator_term)
            numerator_direct_terms.append(direct_term)
            line_results.append({
                "line_id": line.line_id,
                "authoritative_energy_mev": line.energy_mev,
                "transformed_cross_section_argument_mev": transformed,
                "support_endpoint_roundoff_normalized": boundary_normalized,
                "sigma_baseline_1e_minus_46_cm2": sigma_baseline,
                "K_m": ratio,
                "S_m": ratio - 1.0,
                "conventional_prefactor": prefactor,
                "baseline_measure_weight": baseline_weight,
                "transformed_numerator_weight": numerator_term,
            })
        denominator = math.fsum(denominator_terms)
        numerator = math.fsum(numerator_terms)
        direct_numerator = math.fsum(numerator_direct_terms)
        if not math.isfinite(denominator) or denominator <= 0.0 or not math.isfinite(numerator) or numerator <= 0.0:
            raise InvalidBaselineMeasure("The normalized exact observable is not finite and positive.")
        if not math.isclose(numerator, direct_numerator, rel_tol=5e-15, abs_tol=0.0):
            raise InvalidBaselineMeasure("Cross-section accounting invariant failed.")
        prediction = numerator / denominator
        if not math.isfinite(prediction) or prediction <= 0.0:
            raise InvalidBaselineMeasure("R_pred is not finite and positive.")
        parameter_hash = str(request.parameter_source.get("bundle_sha256") or canonical_hash({"kind": request.parameter_source["kind"], "alpha_0": request.alpha_0}))
        warnings = [
            "LSC 6.5.0 exact finite dilation is a NEW_POST_6_4_PHYSICAL_SUCCESSOR.",
            "Only the frozen capture-cross-section argument is dilated; source energies are unchanged.",
        ]
        if request.input_classification == "NON_PHYSICAL_TEST_FIXTURE":
            warnings.append("NON_PHYSICAL_TEST_FIXTURE: this is not an experimental result.")
        return {
            "schema_version": "1.0.0",
            "model_version": "6.5.0",
            "model_profile": "EXACT_FINITE_A2/C/A",
            "model_sha256": self.cross_section.identity.model_sha256,
            "model_state": self.cross_section.identity.model_state,
            "scientific_specification_sha256": self.cross_section.identity.scientific_specification_sha256,
            "scientific_freeze_sha256": self.cross_section.identity.scientific_freeze_sha256,
            "parameter_sha256": parameter_hash,
            "cross_section_payload_sha256": self.cross_section.identity.payload_sha256,
            "source_line_payload_sha256": self.cross_section.identity.source_line_payload_sha256,
            "input_sha256": canonical_hash(payload),
            "input_classification": request.input_classification,
            "experiment_id": request.experiment_id,
            "observation_id": request.observation_id,
            "source_isotope": request.source_isotope,
            "alpha_0": request.alpha_0,
            "alpha_domain_closed_for_input": list(self.cross_section.alpha_domain(line.energy_mev for line in request.lines)),
            "per_line": line_results,
            "baseline_denominator": denominator,
            "exact_numerator": numerator,
            "R_pred": prediction,
            "applicable_domain_status": "PASS",
            "anisotropic_sector": "DISABLED",
            "warnings": warnings,
            "blockers": [],
            "provenance_references": [
                "LSC_6_5_0_SCIENTIFIC_FREEZE.json",
                "spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml",
                "external_physics/gallium_capture/PROVENANCE_MANIFEST.json",
            ],
            "analysis_context": request.analysis_context,
        }

    def predict_json(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(self.predict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
