"""Hash-bound conventional gallium capture cross section for A2."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import CubicSpline

from lsc_kernel.lsc640.errors import CrossSectionProvenanceError, UnsupportedDomainError


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class CrossSectionIdentity:
    scenario_id: str
    payload_sha256: str
    line_payload_sha256: str
    response_spec_sha256: str
    model_sha256: str


class GalliumCaptureCrossSection:
    """Natural-cubic-spline representation frozen before alpha determination."""

    SCENARIO_ID = "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE"

    def __init__(
        self,
        *,
        repository_root: Path,
        energies: np.ndarray,
        values: np.ndarray,
        source_lines: dict[str, Any],
        response_spec: dict[str, Any],
        identity: CrossSectionIdentity,
    ) -> None:
        self.repository_root = repository_root
        self.energies = np.asarray(energies, dtype=np.float64)
        self.values = np.asarray(values, dtype=np.float64)
        self.source_lines = source_lines
        self.response_spec = response_spec
        self.identity = identity
        self._spline = CubicSpline(
            self.energies,
            self.values,
            bc_type="natural",
            extrapolate=False,
        )
        self._audit_representation()

    @classmethod
    def from_repository(cls, repository_root: Path | str) -> "GalliumCaptureCrossSection":
        root = Path(repository_root).resolve()
        manifest_path = root / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json"
        response_path = root / "spec/LSC_6_4_0_RESPONSE_A2.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            response_spec = json.loads(response_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CrossSectionProvenanceError("Cross-section manifest/specification is unavailable.") from exc

        if manifest.get("production_scenario_id") != cls.SCENARIO_ID:
            raise CrossSectionProvenanceError("Unrecognized production cross-section scenario.")
        if response_spec.get("cross_section", {}).get("scenario_id") != cls.SCENARIO_ID:
            raise CrossSectionProvenanceError("Response specification selects a different scenario.")
        if sha256_file(manifest_path) != response_spec["cross_section"].get("provenance_manifest_sha256"):
            raise CrossSectionProvenanceError("Cross-section provenance manifest hash mismatch.")

        declared = {
            row["path"]: row["sha256"]
            for row in manifest.get("original_files", []) + manifest.get("production_payloads", [])
        }
        for relative, expected in declared.items():
            path = root / relative
            if not path.is_file() or sha256_file(path) != expected:
                raise CrossSectionProvenanceError(
                    "Cross-section provenance binding failed.",
                    details={"path": relative},
                )

        cross_rel = response_spec["cross_section"]["payload"]
        line_rel = response_spec["supported_sources"]["payload"]
        cross_path = root / cross_rel
        line_path = root / line_rel
        if sha256_file(cross_path) != response_spec["cross_section"]["payload_sha256"]:
            raise CrossSectionProvenanceError("Cross-section payload does not match response specification.")
        if sha256_file(line_path) != response_spec["supported_sources"]["payload_sha256"]:
            raise CrossSectionProvenanceError("Source-line payload does not match response specification.")

        energies: list[float] = []
        values: list[float] = []
        with cross_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["energy_mev", "cross_section_1e_minus_46_cm2"]:
                raise CrossSectionProvenanceError("Unexpected cross-section table schema.")
            for row in reader:
                energies.append(float(row["energy_mev"]))
                values.append(float(row["cross_section_1e_minus_46_cm2"]))
        source_lines = json.loads(line_path.read_text(encoding="utf-8"))
        response_hash = sha256_file(response_path)
        model_hash = canonical_hash(
            {
                "model_version": "6.4.0",
                "configuration": "A2/C/A",
                "response_spec_sha256": response_hash,
                "cross_section_payload_sha256": sha256_file(cross_path),
                "source_line_payload_sha256": sha256_file(line_path),
            }
        )
        identity = CrossSectionIdentity(
            scenario_id=cls.SCENARIO_ID,
            payload_sha256=sha256_file(cross_path),
            line_payload_sha256=sha256_file(line_path),
            response_spec_sha256=response_hash,
            model_sha256=model_hash,
        )
        return cls(
            repository_root=root,
            energies=np.asarray(energies),
            values=np.asarray(values),
            source_lines=source_lines,
            response_spec=response_spec,
            identity=identity,
        )

    @property
    def domain(self) -> tuple[float, float]:
        return float(self.energies[0]), float(self.energies[-1])

    @property
    def alpha_analysis_bounds(self) -> tuple[float, float]:
        lower, upper = self.response_spec["alpha_0_bounds"]["preregistered_analysis_bound"]
        return float(lower), float(upper)

    def _audit_representation(self) -> None:
        if self.energies.shape != (58,) or self.values.shape != (58,):
            raise CrossSectionProvenanceError("The frozen cross-section payload must have 58 rows.")
        if not np.all(np.isfinite(self.energies)) or not np.all(np.isfinite(self.values)):
            raise CrossSectionProvenanceError("Cross-section payload contains non-finite values.")
        if not np.all(np.diff(self.energies) > 0.0) or not np.all(self.values > 0.0):
            raise CrossSectionProvenanceError("Cross-section payload is not strictly ordered and positive.")
        grid = np.linspace(self.energies[0], self.energies[-1], 32769, dtype=np.float64)
        interpolated = self._spline(grid)
        derivative = self._spline(grid, 1)
        if not np.all(np.isfinite(interpolated)) or not np.all(interpolated > 0.0):
            raise CrossSectionProvenanceError("Frozen spline is not finite and positive over its domain.")
        if not np.all(np.isfinite(derivative)):
            raise CrossSectionProvenanceError("Frozen spline derivative is not finite over its domain.")

    def _checked_energy(self, energy_mev: float) -> float:
        energy = float(energy_mev)
        low, high = self.domain
        if not math.isfinite(energy) or energy < low or energy > high:
            raise UnsupportedDomainError(
                "Energy is outside the frozen cross-section support.",
                details={"energy_mev": energy, "supported_domain_mev": [low, high]},
            )
        return energy

    def sigma(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        result = float(self._spline(energy))
        if not math.isfinite(result) or result <= 0.0:
            raise UnsupportedDomainError("Interpolated cross section is not finite and positive.")
        return result

    def derivative(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        result = float(self._spline(energy, 1))
        if not math.isfinite(result):
            raise UnsupportedDomainError("Cross-section derivative is not finite.")
        return result

    def response(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        sigma = self.sigma(energy)
        value = energy * self.derivative(energy) / sigma
        if not math.isfinite(value):
            raise UnsupportedDomainError("Logarithmic cross-section derivative is not finite.")
        return value

    def finite_dilation_ratio(self, energy_mev: float, alpha_0: float) -> float:
        energy = self._checked_energy(energy_mev)
        alpha = float(alpha_0)
        if not math.isfinite(alpha):
            raise UnsupportedDomainError("alpha_0 must be finite.")
        shifted = energy * math.exp(alpha)
        return self.sigma(shifted) / self.sigma(energy)

    def validate_alpha(self, alpha_0: float) -> float:
        alpha = float(alpha_0)
        lower, upper = self.alpha_analysis_bounds
        if not math.isfinite(alpha) or alpha < lower or alpha > upper:
            raise UnsupportedDomainError(
                "alpha_0 is outside the frozen linear-response analysis domain.",
                details={"alpha_0": alpha, "analysis_bound": [lower, upper]},
            )
        return alpha

    def authoritative_lines(self, isotope: str) -> tuple[dict[str, object], ...]:
        rows = self.source_lines.get("isotopes", {}).get(isotope)
        if not isinstance(rows, list):
            raise UnsupportedDomainError(
                "Unknown or unsupported source isotope.",
                details={"source_isotope": isotope},
            )
        return tuple(dict(row) for row in rows)
