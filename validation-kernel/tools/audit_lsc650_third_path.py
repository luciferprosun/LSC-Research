#!/usr/bin/env python3
"""Independent STEP 08 numerical audit for the frozen LSC 6.5.0 model.

This implementation intentionally imports neither the production evaluator nor
the existing reference evaluator.  It solves the natural-spline system as a
dense Decimal linear system and evaluates the finite-dilation observable from
the frozen payloads directly.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any, Iterable


getcontext().prec = 60

DEFAULT_ABSOLUTE_TOLERANCE = 5e-11
BOUNDARY_ABSOLUTE_TOLERANCE = 5e-9
DOMAIN_ABSOLUTE_TOLERANCE = 5e-15
FIRST_ORDER_ABSOLUTE_TOLERANCE = 5e-7
ROOT_ABSOLUTE_TOLERANCE = 5e-10
UNSUPPORTED_DOMAIN_CODE = "FAIL_CLOSED_UNSUPPORTED_DOMAIN"


class ThirdPathDomainError(ValueError):
    """Raised when a third-path request leaves the frozen support."""

    code = UNSUPPORTED_DOMAIN_CODE


def _d(value: object) -> Decimal:
    return Decimal(str(value))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class DenseDecimalNaturalSpline:
    """Natural cubic spline solved by dense Decimal Gaussian elimination."""

    def __init__(self, x: Iterable[Decimal], y: Iterable[Decimal]) -> None:
        self.x = tuple(x)
        self.y = tuple(y)
        if len(self.x) < 3 or len(self.x) != len(self.y):
            raise ValueError("spline inputs must be matching arrays of length >= 3")
        if any(right <= left for left, right in zip(self.x, self.x[1:])):
            raise ValueError("spline grid must be strictly increasing")
        self.second = self._solve_second_derivatives()

    def _solve_second_derivatives(self) -> tuple[Decimal, ...]:
        n = len(self.x)
        matrix = [[Decimal(0) for _ in range(n)] for _ in range(n)]
        rhs = [Decimal(0) for _ in range(n)]
        matrix[0][0] = Decimal(1)
        matrix[-1][-1] = Decimal(1)
        for i in range(1, n - 1):
            h0 = self.x[i] - self.x[i - 1]
            h1 = self.x[i + 1] - self.x[i]
            matrix[i][i - 1] = h0
            matrix[i][i] = Decimal(2) * (h0 + h1)
            matrix[i][i + 1] = h1
            rhs[i] = Decimal(6) * (
                (self.y[i + 1] - self.y[i]) / h1
                - (self.y[i] - self.y[i - 1]) / h0
            )

        for column in range(n):
            pivot = max(range(column, n), key=lambda row: abs(matrix[row][column]))
            if matrix[pivot][column] == 0:
                raise ArithmeticError("singular natural-spline system")
            if pivot != column:
                matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
                rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
            pivot_value = matrix[column][column]
            for row in range(column + 1, n):
                if matrix[row][column] == 0:
                    continue
                factor = matrix[row][column] / pivot_value
                matrix[row][column] = Decimal(0)
                for j in range(column + 1, n):
                    matrix[row][j] -= factor * matrix[column][j]
                rhs[row] -= factor * rhs[column]

        result = [Decimal(0) for _ in range(n)]
        for row in range(n - 1, -1, -1):
            residual = rhs[row] - sum(
                matrix[row][j] * result[j] for j in range(row + 1, n)
            )
            result[row] = residual / matrix[row][row]
        return tuple(result)

    def _interval(self, value: Decimal) -> int:
        if value < self.x[0] or value > self.x[-1]:
            raise ThirdPathDomainError("energy leaves frozen cross-section support")
        if value == self.x[-1]:
            return len(self.x) - 2
        low = 0
        high = len(self.x) - 1
        while high - low > 1:
            middle = (low + high) // 2
            if value < self.x[middle]:
                high = middle
            else:
                low = middle
        return low

    def evaluate(self, value: Decimal) -> Decimal:
        i = self._interval(value)
        x0, x1 = self.x[i], self.x[i + 1]
        h = x1 - x0
        left = (x1 - value) / h
        right = (value - x0) / h
        return (
            left * self.y[i]
            + right * self.y[i + 1]
            + ((left**3 - left) * self.second[i] + (right**3 - right) * self.second[i + 1])
            * h**2
            / Decimal(6)
        )

    def derivative(self, value: Decimal) -> Decimal:
        i = self._interval(value)
        x0, x1 = self.x[i], self.x[i + 1]
        h = x1 - x0
        left = (x1 - value) / h
        right = (value - x0) / h
        return (
            (self.y[i + 1] - self.y[i]) / h
            + ((-Decimal(3) * left**2 + Decimal(1)) * self.second[i]
               + (Decimal(3) * right**2 - Decimal(1)) * self.second[i + 1])
            * h
            / Decimal(6)
        )


def load_spline(root: Path) -> DenseDecimalNaturalSpline:
    energies: list[Decimal] = []
    values: list[Decimal] = []
    path = root / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            energies.append(Decimal(row["energy_mev"]))
            values.append(Decimal(row["cross_section_1e_minus_46_cm2"]))
    if len(energies) != 58:
        raise AssertionError("frozen cross-section payload must contain 58 knots")
    return DenseDecimalNaturalSpline(energies, values)


def load_source_lines(root: Path) -> dict[str, list[dict[str, object]]]:
    document = json.loads(
        (root / "external_physics/gallium_capture/source_lines_prc108_035502.json")
        .read_text(encoding="utf-8")
    )
    return document["isotopes"]


def alpha_domain(
    spline: DenseDecimalNaturalSpline, lines: Iterable[dict[str, object]]
) -> tuple[Decimal, Decimal]:
    energies = [_d(row["energy_mev"]) for row in lines]
    return (
        max((spline.x[0] / energy).ln() for energy in energies),
        min((spline.x[-1] / energy).ln() for energy in energies),
    )


def exact_ratio(
    spline: DenseDecimalNaturalSpline, energy: Decimal, alpha: Decimal
) -> Decimal:
    transformed = energy * alpha.exp()
    if transformed < spline.x[0] or transformed > spline.x[-1]:
        raise ThirdPathDomainError("transformed energy leaves frozen support")
    return spline.evaluate(transformed) / spline.evaluate(energy)


def prediction(
    spline: DenseDecimalNaturalSpline,
    lines: Iterable[dict[str, object]],
    alpha: Decimal,
) -> dict[str, object]:
    denominator_terms: list[Decimal] = []
    numerator_terms: list[Decimal] = []
    kernels: list[Decimal] = []
    for row in lines:
        energy = _d(row["energy_mev"])
        prefactor = (
            _d(row.get("branching_fraction", 1))
            * _d(row.get("source_activity_bq", 1))
            * _d(row.get("exposure_seconds", 1))
            * _d(row.get("conventional_probability", 1))
            * _d(row.get("geometry_factor", 1))
            * _d(row.get("detector_efficiency", 1))
        )
        baseline_sigma = spline.evaluate(energy)
        transformed_sigma = spline.evaluate(energy * alpha.exp())
        kernel = transformed_sigma / baseline_sigma
        denominator_terms.append(prefactor * baseline_sigma)
        numerator_terms.append(prefactor * transformed_sigma)
        kernels.append(kernel)
    denominator = sum(denominator_terms, Decimal(0))
    numerator = sum(numerator_terms, Decimal(0))
    return {
        "baseline_denominator": denominator,
        "exact_numerator": numerator,
        "R_pred": numerator / denominator,
        "per_line_K_m": kernels,
    }


def _materialize_success_case(
    specification: dict[str, Any],
    case: dict[str, Any],
    source_lines: dict[str, list[dict[str, object]]],
) -> tuple[list[dict[str, object]], Decimal]:
    template = specification["templates"][case["template"]]
    if "authoritative_line_source" in template:
        isotope = template["source_isotope"]
        factors = template["conventional_factors"]
        lines = [{**row, **factors} for row in source_lines[isotope]]
    else:
        lines = [dict(row) for row in template["lines"]]
    return lines, _d(case["overrides"]["alpha_0"])


def _bisect_prediction(
    spline: DenseDecimalNaturalSpline,
    lines: list[dict[str, object]],
    target: Decimal,
    lower: Decimal,
    upper: Decimal,
) -> Decimal:
    low_value = prediction(spline, lines, lower)["R_pred"]
    high_value = prediction(spline, lines, upper)["R_pred"]
    if not (low_value <= target <= high_value):
        raise AssertionError("root target is not bracketed")
    for _ in range(240):
        middle = (lower + upper) / Decimal(2)
        value = prediction(spline, lines, middle)["R_pred"]
        if value < target:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / Decimal(2)


def run_audit(root: Path) -> dict[str, object]:
    root = root.resolve()
    spline = load_spline(root)
    source_lines = load_source_lines(root)
    all_lines = [row for isotope in ("Cr51", "Ar37") for row in source_lines[isotope]]
    domain = alpha_domain(spline, all_lines)
    stored_domain = (
        Decimal("-0.5747389495096434"),
        Decimal("3.607238025076703"),
    )
    domain_error = max(abs(float(actual - expected)) for actual, expected in zip(domain, stored_domain, strict=True))
    if domain_error > DOMAIN_ABSOLUTE_TOLERANCE:
        raise AssertionError("independent domain derivation differs from frozen domain")

    boundary_results: dict[str, object] = {}
    for label, alpha in (
        ("exact_lower", domain[0]),
        ("inside_lower", domain[0] + Decimal("1e-12")),
        ("exact_upper", domain[1]),
        ("inside_upper", domain[1] - Decimal("1e-12")),
    ):
        values = [exact_ratio(spline, _d(row["energy_mev"]), alpha) for row in all_lines]
        boundary_results[label] = {
            "status": "PASS",
            "minimum_K_m": float(min(values)),
            "maximum_K_m": float(max(values)),
        }
    for label, alpha in (
        ("outside_lower", domain[0] - Decimal("1e-12")),
        ("outside_upper", domain[1] + Decimal("1e-12")),
    ):
        try:
            for row in all_lines:
                exact_ratio(spline, _d(row["energy_mev"]), alpha)
        except ThirdPathDomainError as exc:
            boundary_results[label] = {"status": "PASS", "error_code": exc.code}
        else:
            raise AssertionError(f"{label} did not fail closed")

    golden = json.loads(
        (root / "spec/LSC_6_5_0_GOLDEN_VECTORS.json").read_text(encoding="utf-8")
    )
    golden_results: list[dict[str, object]] = []
    maximum_golden_difference = 0.0
    for case in golden["vectors"][:20]:
        lines, alpha = _materialize_success_case(golden, case, source_lines)
        actual = prediction(spline, lines, alpha)
        tolerance = max(DEFAULT_ABSOLUTE_TOLERANCE, float(case["tolerance"]))
        differences: list[float] = []
        for field in ("baseline_denominator", "exact_numerator", "R_pred"):
            differences.append(abs(float(actual[field]) - float(case["expected"][field])))
        differences.extend(
            abs(float(value) - float(expected))
            for value, expected in zip(
                actual["per_line_K_m"], case["expected"]["per_line_K_m"], strict=True
            )
        )
        maximum = max(differences)
        if maximum > tolerance:
            raise AssertionError(f"{case['id']} exceeds declared third-path tolerance")
        maximum_golden_difference = max(maximum_golden_difference, maximum)
        golden_results.append(
            {"id": case["id"], "status": "PASS", "maximum_absolute_difference": maximum}
        )

    linear_goldens = json.loads(
        (root / "spec/LSC_6_4_0_GOLDEN_VECTORS.json").read_text(encoding="utf-8")
    )
    expected_mean_f = {
        "Cr51": _d(linear_goldens["vectors"][0]["expected"]["mean_F_m"]),
        "Ar37": _d(linear_goldens["vectors"][1]["expected"]["mean_F_m"]),
    }
    bridge_results: dict[str, object] = {}
    bridge_maximum_error = 0.0
    h = Decimal("1e-7")
    for isotope in ("Cr51", "Ar37"):
        lines = source_lines[isotope]
        denominator = Decimal(0)
        weighted_generator = Decimal(0)
        for row in lines:
            energy = _d(row["energy_mev"])
            weight = _d(row["branching_fraction"]) * spline.evaluate(energy)
            generator = energy * spline.derivative(energy) / spline.evaluate(energy)
            denominator += weight
            weighted_generator += weight * generator
        mean_generator = weighted_generator / denominator
        central = (
            prediction(spline, lines, h)["R_pred"]
            - prediction(spline, lines, -h)["R_pred"]
        ) / (Decimal(2) * h)
        frozen_difference = abs(float(mean_generator - expected_mean_f[isotope]))
        central_difference = abs(float(central - mean_generator))
        bridge_maximum_error = max(bridge_maximum_error, frozen_difference, central_difference)
        if frozen_difference > DEFAULT_ABSOLUTE_TOLERANCE or central_difference > FIRST_ORDER_ABSOLUTE_TOLERANCE:
            raise AssertionError("first-order bridge to LSC 6.4.0 failed")
        bridge_results[isotope] = {
            "third_path_mean_generator": float(mean_generator),
            "frozen_lsc640_mean_generator": float(expected_mean_f[isotope]),
            "central_exact_derivative": float(central),
            "status": "PASS",
        }

    protocol = json.loads(
        (root / "LSC_6_5_0_ALPHA_DETERMINATION_PROTOCOL.json").read_text(encoding="utf-8")
    )
    frozen_result = json.loads(
        (root / "LSC_6_5_0_ALPHA_DETERMINATION_RESULT.json").read_text(encoding="utf-8")
    )
    cr_lines = source_lines["Cr51"]
    observed = _d(protocol["development_data"]["observed_values"][0])
    uncertainty = _d(protocol["development_data"]["standard_uncertainties"][0])
    estimate = _bisect_prediction(spline, cr_lines, observed, domain[0], Decimal(0))
    interval_lower = _bisect_prediction(spline, cr_lines, observed - uncertainty, domain[0], estimate)
    interval_upper = _bisect_prediction(spline, cr_lines, observed + uncertainty, estimate, Decimal(0))
    frozen_estimate = _d(frozen_result["alpha_0_estimate"])
    frozen_interval = tuple(_d(item) for item in frozen_result["certified_profile_delta_chi_square_1_interval"])
    root_differences = {
        "estimate": abs(float(estimate - frozen_estimate)),
        "interval_lower": abs(float(interval_lower - frozen_interval[0])),
        "interval_upper": abs(float(interval_upper - frozen_interval[1])),
    }
    if max(root_differences.values()) > ROOT_ABSOLUTE_TOLERANCE:
        raise AssertionError("third-path root solution differs from the frozen result")
    stored_prediction = prediction(spline, cr_lines, frozen_estimate)["R_pred"]
    stored_objective = ((observed - stored_prediction) / uncertainty) ** 2

    grid = [
        domain[0] + Decimal("1e-10"),
        Decimal("-0.3"),
        frozen_interval[0],
        frozen_estimate,
        frozen_interval[1],
        Decimal("-0.000001"),
        Decimal(0),
        Decimal("0.000001"),
        Decimal("0.3"),
        domain[1] - Decimal("1e-10"),
    ]
    grid_checks = 0
    for alpha in grid:
        for row in all_lines:
            value = exact_ratio(spline, _d(row["energy_mev"]), alpha)
            if value <= 0:
                raise AssertionError("third-path kernel is non-positive")
            grid_checks += 1

    return {
        "status": "PASS",
        "implementation": "dense Decimal natural-spline solve; no production/reference imports",
        "declared_tolerances": {
            "default_absolute": DEFAULT_ABSOLUTE_TOLERANCE,
            "boundary_absolute": BOUNDARY_ABSOLUTE_TOLERANCE,
            "domain_absolute": DOMAIN_ABSOLUTE_TOLERANCE,
            "first_order_absolute": FIRST_ORDER_ABSOLUTE_TOLERANCE,
            "root_absolute": ROOT_ABSOLUTE_TOLERANCE,
        },
        "input_hashes": {
            "cross_section_payload_sha256": sha256_file(root / "external_physics/gallium_capture/bahcall_1997_best_estimate.csv"),
            "source_line_payload_sha256": sha256_file(root / "external_physics/gallium_capture/source_lines_prc108_035502.json"),
        },
        "domain": {
            "independently_derived": [float(item) for item in domain],
            "stored": [float(item) for item in stored_domain],
            "maximum_absolute_difference": domain_error,
            "boundary_checks": boundary_results,
        },
        "golden_success_vectors": {
            "passed": len(golden_results),
            "failed": 0,
            "maximum_absolute_difference": maximum_golden_difference,
            "results": golden_results,
        },
        "first_order_bridge": {
            "status": "PASS",
            "maximum_absolute_difference": bridge_maximum_error,
            "isotopes": bridge_results,
        },
        "parameter_root_reconstruction": {
            "status": "PASS",
            "analytic_structure": "solve R_pred(alpha_0)=R_observed by monotone bisection",
            "alpha_0": float(estimate),
            "interval": [float(interval_lower), float(interval_upper)],
            "differences_from_frozen": root_differences,
            "objective_at_frozen_alpha": float(stored_objective),
        },
        "all_source_line_grid_checks": grid_checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    print(json.dumps(run_audit(arguments.root), sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
