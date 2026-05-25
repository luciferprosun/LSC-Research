from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GalliumPoint:
    experiment: str
    label: str
    ratio: float
    sigma: float


def load_dataset(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _extract_sigma(result: dict[str, Any]) -> float | None:
    if "R_error" in result and isinstance(result["R_error"], (int, float)):
        return float(result["R_error"])
    plus = result.get("R_error_plus")
    minus = result.get("R_error_minus")
    if isinstance(plus, (int, float)) and isinstance(minus, (int, float)):
        return float(0.5 * (plus + minus))
    return None


def extract_ratio_points(dataset: dict[str, Any]) -> list[GalliumPoint]:
    points: list[GalliumPoint] = []
    for experiment in dataset.get("experiments", []):
        experiment_name = str(experiment.get("experiment_name", "UNKNOWN"))
        for result in experiment.get("measured_results", []):
            r = result.get("R")
            sigma = _extract_sigma(result)
            label = str(result.get("label", "unnamed"))
            if isinstance(r, (int, float)) and isinstance(sigma, (int, float)) and sigma > 0:
                points.append(
                    GalliumPoint(
                        experiment=experiment_name,
                        label=label,
                        ratio=float(r),
                        sigma=float(sigma),
                    )
                )
    return points
