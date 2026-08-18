"""Independent stdlib reference implementation for exact LSC 6.5.0."""

from __future__ import annotations

import bisect
import csv
import math
from pathlib import Path
from typing import Iterable, Mapping

from lsc_kernel.lsc650.errors import InvalidBaselineMeasure, UnsupportedDomainError


class NaturalSplineReference650:
    """Independent natural-spline solver; shares no production ratio/integration routine."""

    def __init__(self, x: Iterable[float], y: Iterable[float]) -> None:
        self.x = tuple(float(item) for item in x)
        self.y = tuple(float(item) for item in y)
        if len(self.x) < 3 or len(self.x) != len(self.y):
            raise ValueError("Reference spline requires matching x/y arrays.")
        self.second = self._solve_second_derivatives()

    @classmethod
    def from_csv(cls, path: Path | str) -> "NaturalSplineReference650":
        x: list[float] = []
        y: list[float] = []
        with Path(path).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                x.append(float(row["energy_mev"]))
                y.append(float(row["cross_section_1e_minus_46_cm2"]))
        return cls(x, y)

    def _solve_second_derivatives(self) -> tuple[float, ...]:
        n = len(self.x)
        size = n - 2
        lower = [0.0] * size
        diagonal = [0.0] * size
        upper = [0.0] * size
        rhs = [0.0] * size
        for j in range(size):
            i = j + 1
            h0 = self.x[i] - self.x[i - 1]
            h1 = self.x[i + 1] - self.x[i]
            if h0 <= 0.0 or h1 <= 0.0:
                raise ValueError("Reference x grid must be strictly increasing.")
            lower[j] = h0 if j else 0.0
            diagonal[j] = 2.0 * (h0 + h1)
            upper[j] = h1 if j < size - 1 else 0.0
            rhs[j] = 6.0 * ((self.y[i + 1] - self.y[i]) / h1 - (self.y[i] - self.y[i - 1]) / h0)
        for j in range(1, size):
            factor = lower[j] / diagonal[j - 1]
            diagonal[j] -= factor * upper[j - 1]
            rhs[j] -= factor * rhs[j - 1]
        interior = [0.0] * size
        interior[-1] = rhs[-1] / diagonal[-1]
        for j in range(size - 2, -1, -1):
            interior[j] = (rhs[j] - upper[j] * interior[j + 1]) / diagonal[j]
        return tuple([0.0, *interior, 0.0])

    def _interval(self, value: float) -> int:
        if not math.isfinite(value) or value < self.x[0] or value > self.x[-1]:
            raise UnsupportedDomainError("Reference evaluation is outside frozen support.")
        return min(bisect.bisect_right(self.x, value) - 1, len(self.x) - 2)

    def evaluate(self, value: float) -> float:
        i = self._interval(value)
        x0, x1 = self.x[i], self.x[i + 1]
        y0, y1 = self.y[i], self.y[i + 1]
        m0, m1 = self.second[i], self.second[i + 1]
        h = x1 - x0
        left = x1 - value
        right = value - x0
        result = (
            m0 * left**3 / (6.0 * h) + m1 * right**3 / (6.0 * h)
            + (y0 - m0 * h * h / 6.0) * left / h
            + (y1 - m1 * h * h / 6.0) * right / h
        )
        if not math.isfinite(result) or result <= 0.0:
            raise UnsupportedDomainError("Reference spline is not finite and positive.")
        return result

    def derivative(self, value: float) -> float:
        i = self._interval(value)
        x0, x1 = self.x[i], self.x[i + 1]
        y0, y1 = self.y[i], self.y[i + 1]
        m0, m1 = self.second[i], self.second[i + 1]
        h = x1 - x0
        left = x1 - value
        right = value - x0
        return (
            -m0 * left**2 / (2.0 * h) + m1 * right**2 / (2.0 * h)
            - (y0 - m0 * h * h / 6.0) / h + (y1 - m1 * h * h / 6.0) / h
        )

    def exact_ratio(self, energy_mev: float, alpha_0: float) -> tuple[float, float]:
        transformed = float(energy_mev) * math.exp(float(alpha_0))
        low, high = self.x[0], self.x[-1]
        if transformed > high and transformed <= high + 4.0 * math.ulp(high):
            transformed = high
        elif transformed < low and transformed >= low - 4.0 * math.ulp(low):
            transformed = low
        return self.evaluate(transformed) / self.evaluate(float(energy_mev)), transformed


def reference_exact_prediction(
    spline: NaturalSplineReference650,
    lines: Iterable[Mapping[str, float | str]],
    alpha_0: float,
) -> dict[str, object]:
    denominator_terms: list[float] = []
    numerator_terms: list[float] = []
    per_line: list[dict[str, float | str]] = []
    for line in lines:
        energy = float(line["energy_mev"])
        transformed = energy * math.exp(float(alpha_0))
        if transformed > spline.x[-1] and transformed <= spline.x[-1] + 4.0 * math.ulp(spline.x[-1]):
            transformed = spline.x[-1]
        if transformed < spline.x[0] and transformed >= spline.x[0] - 4.0 * math.ulp(spline.x[0]):
            transformed = spline.x[0]
        prefactor = (
            float(line["branching_fraction"]) * float(line["source_activity_bq"])
            * float(line["exposure_seconds"]) * float(line["conventional_probability"])
            * float(line["geometry_factor"]) * float(line["detector_efficiency"])
        )
        baseline = prefactor * spline.evaluate(energy)
        numerator = prefactor * spline.evaluate(transformed)
        denominator_terms.append(baseline)
        numerator_terms.append(numerator)
        per_line.append({"line_id": str(line["line_id"]), "transformed_energy_mev": transformed, "K_m": numerator / baseline})
    denominator = math.fsum(denominator_terms)
    numerator = math.fsum(numerator_terms)
    if not math.isfinite(denominator) or denominator <= 0.0 or not math.isfinite(numerator) or numerator <= 0.0:
        raise InvalidBaselineMeasure("Independent reference measure is invalid.")
    return {"baseline_denominator": denominator, "exact_numerator": numerator, "R_pred": numerator / denominator, "per_line": per_line}
