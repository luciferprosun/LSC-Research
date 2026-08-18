"""Hash-bound exact finite-dilation cross-section layer for LSC 6.5.0."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.interpolate import CubicSpline

from lsc_kernel.lsc650.errors import CrossSectionProvenanceError, UnsupportedDomainError


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
class LSC650CrossSectionIdentity:
    scenario_id: str
    payload_sha256: str
    source_line_payload_sha256: str
    scientific_specification_sha256: str
    scientific_freeze_sha256: str
    model_sha256: str
    model_state: str


class ExactGalliumCaptureCrossSection:
    """Frozen natural spline used by the exact finite-dilation kernel."""

    SCENARIO_ID = "BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE"
    PAYLOAD_SHA256 = "55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5"
    SOURCE_LINES_SHA256 = "ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e"
    SPEC_SHA256 = "114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948"

    def __init__(
        self,
        *,
        repository_root: Path,
        energies: np.ndarray,
        values: np.ndarray,
        source_lines: dict[str, Any],
        identity: LSC650CrossSectionIdentity,
    ) -> None:
        self.repository_root = repository_root
        self.energies = np.asarray(energies, dtype=np.float64)
        self.values = np.asarray(values, dtype=np.float64)
        self.source_lines = source_lines
        self.identity = identity
        self._spline = CubicSpline(self.energies, self.values, bc_type="natural", extrapolate=False)
        self._audit_representation()

    @classmethod
    def from_repository(cls, repository_root: Path | str) -> "ExactGalliumCaptureCrossSection":
        root = Path(repository_root).resolve()
        manifest_path = root / "external_physics/gallium_capture/PROVENANCE_MANIFEST.json"
        payload_path = root / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"
        lines_path = root / "external_physics/gallium_capture/source_lines_prc108_035502.json"
        spec_path = root / "spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml"
        freeze_path = root / "LSC_6_5_0_SCIENTIFIC_FREEZE.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            source_lines = json.loads(lines_path.read_text(encoding="utf-8"))
            freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CrossSectionProvenanceError("LSC 6.5.0 cross-section provenance is unavailable.") from exc
        if manifest.get("production_scenario_id") != cls.SCENARIO_ID:
            raise CrossSectionProvenanceError("Unrecognized cross-section scenario.")
        expected = {
            payload_path: cls.PAYLOAD_SHA256,
            lines_path: cls.SOURCE_LINES_SHA256,
            spec_path: cls.SPEC_SHA256,
        }
        for path, digest in expected.items():
            if not path.is_file() or sha256_file(path) != digest:
                raise CrossSectionProvenanceError("A frozen LSC 6.5.0 source binding failed.", details={"path": str(path.relative_to(root))})
        if freeze.get("cross_section", {}).get("payload_sha256") != cls.PAYLOAD_SHA256:
            raise CrossSectionProvenanceError("Scientific freeze selects a different cross-section payload.")
        if freeze.get("cross_section", {}).get("source_lines_sha256") != cls.SOURCE_LINES_SHA256:
            raise CrossSectionProvenanceError("Scientific freeze selects different source lines.")
        energies: list[float] = []
        values: list[float] = []
        with payload_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != ["energy_mev", "cross_section_1e_minus_46_cm2"]:
                raise CrossSectionProvenanceError("Unexpected cross-section table schema.")
            for row in reader:
                energies.append(float(row["energy_mev"]))
                values.append(float(row["cross_section_1e_minus_46_cm2"]))
        freeze_hash = sha256_file(freeze_path)
        model_state = "PREFIT_SCIENTIFIC_FREEZE"
        model_hash = canonical_hash(
            {
                "model_version": "6.5.0",
                "scientific_specification_sha256": cls.SPEC_SHA256,
                "scientific_freeze_sha256": freeze_hash,
                "cross_section_payload_sha256": cls.PAYLOAD_SHA256,
                "source_line_payload_sha256": cls.SOURCE_LINES_SHA256,
            }
        )
        identity_path = root / "LSC_6_5_0_MODEL_IDENTITY.json"
        if identity_path.is_file():
            identity_doc = json.loads(identity_path.read_text(encoding="utf-8"))
            components = identity_doc.get("components", {})
            if components.get("scientific_freeze_sha256") != freeze_hash or components.get("cross_section_payload_sha256") != cls.PAYLOAD_SHA256:
                raise CrossSectionProvenanceError("Final model identity does not bind the active scientific sources.")
            model_hash = str(identity_doc["model_sha256"])
            model_state = "FROZEN_PARAMETER_BUNDLE"
        return cls(
            repository_root=root,
            energies=np.asarray(energies),
            values=np.asarray(values),
            source_lines=source_lines,
            identity=LSC650CrossSectionIdentity(
                scenario_id=cls.SCENARIO_ID,
                payload_sha256=cls.PAYLOAD_SHA256,
                source_line_payload_sha256=cls.SOURCE_LINES_SHA256,
                scientific_specification_sha256=cls.SPEC_SHA256,
                scientific_freeze_sha256=freeze_hash,
                model_sha256=model_hash,
                model_state=model_state,
            ),
        )

    @property
    def support(self) -> tuple[float, float]:
        return float(self.energies[0]), float(self.energies[-1])

    def _audit_representation(self) -> None:
        if self.energies.shape != (58,) or self.values.shape != (58,):
            raise CrossSectionProvenanceError("The frozen payload must have exactly 58 rows.")
        if not np.all(np.isfinite(self.energies)) or not np.all(np.isfinite(self.values)):
            raise CrossSectionProvenanceError("The frozen payload contains non-finite values.")
        if not np.all(np.diff(self.energies) > 0.0) or not np.all(self.values > 0.0):
            raise CrossSectionProvenanceError("The frozen payload is not ordered and strictly positive.")
        grid = np.linspace(self.energies[0], self.energies[-1], 32769, dtype=np.float64)
        values = self._spline(grid)
        if not np.all(np.isfinite(values)) or not np.all(values > 0.0):
            raise CrossSectionProvenanceError("The frozen spline is not finite and positive over support.")

    def _checked_energy(self, energy_mev: float) -> float:
        energy = float(energy_mev)
        low, high = self.support
        if not math.isfinite(energy) or energy < low or energy > high:
            raise UnsupportedDomainError("Energy is outside frozen cross-section support.", details={"energy_mev": energy, "support_mev": [low, high]})
        return energy

    def sigma(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        value = float(self._spline(energy))
        if not math.isfinite(value) or value <= 0.0:
            raise UnsupportedDomainError("Interpolated cross section is not finite and positive.")
        return value

    def derivative(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        value = float(self._spline(energy, 1))
        if not math.isfinite(value):
            raise UnsupportedDomainError("Spline derivative is not finite.")
        return value

    def linear_generator(self, energy_mev: float) -> float:
        energy = self._checked_energy(energy_mev)
        return energy * self.derivative(energy) / self.sigma(energy)

    def authoritative_lines(self, isotope: str) -> tuple[dict[str, object], ...]:
        rows = self.source_lines.get("isotopes", {}).get(isotope)
        if not isinstance(rows, list):
            raise UnsupportedDomainError("Unsupported source isotope.", details={"source_isotope": isotope})
        return tuple(dict(row) for row in rows)

    def alpha_domain(self, energies_mev: Iterable[float]) -> tuple[float, float]:
        energies = tuple(float(value) for value in energies_mev)
        if not energies:
            raise UnsupportedDomainError("At least one source energy is required.")
        low, high = self.support
        for energy in energies:
            self._checked_energy(energy)
        lower = max(math.log(low / energy) for energy in energies)
        upper = min(math.log(high / energy) for energy in energies)
        return lower, upper

    def validate_alpha(self, alpha_0: float, energies_mev: Iterable[float]) -> float:
        alpha = float(alpha_0)
        lower, upper = self.alpha_domain(energies_mev)
        if not math.isfinite(alpha) or alpha < lower or alpha > upper:
            raise UnsupportedDomainError("alpha_0 violates the source-support-derived domain.", details={"alpha_0": alpha, "domain_closed": [lower, upper]})
        return alpha

    def transformed_energy(self, energy_mev: float, alpha_0: float) -> tuple[float, bool]:
        energy = self._checked_energy(energy_mev)
        alpha = self.validate_alpha(alpha_0, (energy,))
        transformed = energy * math.exp(alpha)
        low, high = self.support
        normalized = False
        # Closed-support endpoint roundoff is explicit and limited to four ULPs.
        if transformed < low and transformed >= low - 4.0 * math.ulp(low):
            transformed = low
            normalized = True
        elif transformed > high and transformed <= high + 4.0 * math.ulp(high):
            transformed = high
            normalized = True
        self._checked_energy(transformed)
        return transformed, normalized

    def exact_ratio(self, energy_mev: float, alpha_0: float) -> tuple[float, float, bool]:
        transformed, normalized = self.transformed_energy(energy_mev, alpha_0)
        ratio = self.sigma(transformed) / self.sigma(energy_mev)
        if not math.isfinite(ratio) or ratio <= 0.0:
            raise UnsupportedDomainError("Exact finite-dilation kernel is not finite and positive.")
        return ratio, transformed, normalized
