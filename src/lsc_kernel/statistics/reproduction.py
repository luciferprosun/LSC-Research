"""Public-result reproduction controls; these are not LSC validation."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from lsc_kernel.io.hashes import sha256_file

from .chi_square import GridChiSquare, grid_from_sequences


@dataclass(frozen=True, slots=True)
class ReproductionCheck:
    check_id: str
    observed: float | tuple[int, int]
    expected: float | tuple[int, int]
    tolerance: float
    passed: bool
    classification: str
    source: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _archived_gallium_checks(root: Path) -> tuple[tuple[ReproductionCheck, ...], str]:
    """Load the frozen public-reproduction audit instead of duplicating constants in code."""
    relative = "LSC_6_3_0_VALIDATION/18_VALIDATION_READY/PUBLISHED_RESULT_REPRODUCTION.csv"
    path = root / relative
    with path.open(encoding="utf-8", newline="") as handle:
        by_name = {row["test"]: row for row in csv.DictReader(handle)}
    requested = (
        ("BEST_INNER_MEASURED_PREDICTED", "BEST inner measured/predicted"),
        ("BEST_OUTER_MEASURED_PREDICTED", "BEST outer measured/predicted"),
        ("BEST_OUTER_INNER_DOUBLE_RATIO", "BEST outer/inner double ratio"),
        ("GALLEX_CR1", "GALLEX Cr1 pulse-shape ratio"),
        ("GALLEX_CR2", "GALLEX Cr2 pulse-shape ratio"),
        ("SAGE_CR51", "SAGE 51Cr ratio"),
        ("SAGE_AR37", "SAGE 37Ar ratio"),
    )
    checks = []
    for check_id, source_name in requested:
        if source_name not in by_name:
            raise ValueError(f"Archived public-reproduction row is missing: {source_name}")
        row = by_name[source_name]
        observed = float(row["calculated"])
        expected = float(row["published"])
        tolerance = float(row["absolute_tolerance"])
        checks.append(
            ReproductionCheck(
                check_id,
                observed,
                expected,
                tolerance,
                abs(observed - expected) <= tolerance and row["status"] == "PASS",
                "PUBLIC_RESULT_REPRODUCTION_ONLY",
                f"{relative}; {row['source']}",
            )
        )
    return tuple(checks), sha256_file(path)


def six_gallium_diagonal_combination() -> dict[str, object]:
    ratios = np.asarray((0.791, 0.766, 0.953, 0.812, 0.95, 0.79), dtype=np.float64)
    sigmas = np.asarray((0.05, 0.05, 0.11, 0.105, 0.12, 0.095), dtype=np.float64)
    weights = 1.0 / sigmas**2
    mean = float(np.sum(weights * ratios) / np.sum(weights))
    sigma = float(1.0 / math.sqrt(float(np.sum(weights))))
    chi_square = float(np.sum(((ratios - mean) / sigmas) ** 2))
    return {
        "classification": "SENSITIVITY_ONLY",
        "collaboration_equivalent": False,
        "covariance_scenario": "COV_DIAGONAL",
        "ratios": ratios.tolist(),
        "sigmas": sigmas.tolist(),
        "weighted_mean": mean,
        "weighted_sigma": sigma,
        "chi_square_about_weighted_mean": chi_square,
        "forbidden_interpretation": ["combined significance", "sigma evidence", "collaboration result"],
    }


def load_katrin_grid(root: Path) -> GridChiSquare:
    relative = "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json"
    payload = json.loads((root / relative).read_text(encoding="utf-8"))
    return grid_from_sequences(
        payload["mnu2sterile"],
        payload["sin2thetaee"],
        payload["chiSquareMatrix"],
        axis_0_name="mnu2sterile",
        axis_1_name="sin2thetaee",
    )


def reproduce_public_results(root: Path) -> dict[str, object]:
    archived_checks, audit_sha256 = _archived_gallium_checks(root)
    checks = list(archived_checks)
    grid = load_katrin_grid(root)
    minimum, minimum_index, minimum_axes = grid.minimum()
    checks.extend(
        (
            ReproductionCheck(
                "KATRIN_GRID_DIMENSIONS",
                grid.shape,
                (50, 50),
                0.0,
                grid.shape == (50, 50),
                "PUBLIC_RESULT_REPRODUCTION_ONLY",
                "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json",
            ),
            ReproductionCheck(
                "KATRIN_FINITE_GRID_MINIMUM",
                minimum,
                1374.7638148637948,
                1e-10,
                math.isfinite(minimum) and abs(minimum - 1374.7638148637948) <= 1e-10,
                "PUBLIC_RESULT_REPRODUCTION_ONLY",
                "LSC_6_3_0_VALIDATION/06_KATRIN/records/19369714/files/Main_result_KNM1to5_chi_square_map.json",
            ),
        )
    )
    return {
        "schema_version": "1.0.0",
        "classification": "PUBLIC_RESULT_REPRODUCTION_ONLY",
        "LSC_used": False,
        "checks": [check.as_dict() for check in checks],
        "passed": all(check.passed for check in checks),
        "passed_count": sum(check.passed for check in checks),
        "total_count": len(checks),
        "gallium_reproduction_audit_sha256": audit_sha256,
        "katrin_grid": {
            "shape": list(grid.shape),
            "finite_minimum": minimum,
            "minimum_index": list(minimum_index),
            "minimum_axes": list(minimum_axes),
            "interpolation_authorized": grid.interpolation_authorized,
            "mapping_state": "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING",
        },
        "six_gallium_diagonal": six_gallium_diagonal_combination(),
    }
