from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data import Observation, anchor_names, load_dataset, source_mean_cross_section


@dataclass(frozen=True)
class FitRow:
    name: str
    observed_r: float
    predicted_r: float
    residual: float
    pull: float | None
    kind: str


@dataclass(frozen=True)
class AnalysisResult:
    coefficients: np.ndarray
    coefficient_names: list[str]
    condition_number: float
    anchor_rows: list[FitRow]
    validation_rows: list[FitRow]
    loo_rows: list[FitRow]
    source_mean_51cr_cm2: float
    source_mean_37ar_cm2: float
    anchor_set: list[str]

    def to_json(self) -> dict:
        return {
            "coefficients": {
                name: float(value)
                for name, value in zip(self.coefficient_names, self.coefficients, strict=True)
            },
            "condition_number": float(self.condition_number),
            "anchor_set": self.anchor_set,
            "anchor_rows": [row.__dict__ for row in self.anchor_rows],
            "validation_rows": [row.__dict__ for row in self.validation_rows],
            "loo_rows": [row.__dict__ for row in self.loo_rows],
            "source_mean_51cr_cm2": float(self.source_mean_51cr_cm2),
            "source_mean_37ar_cm2": float(self.source_mean_37ar_cm2),
        }


COEFFICIENT_NAMES = [
    "beta_length",
    "beta_shape",
    "beta_source",
    "beta_zone",
    "beta_intercept",
]


def _as_arrays(observations: list[Observation]) -> tuple[np.ndarray, np.ndarray]:
    x = np.array([obs.feature for obs in observations], dtype=float)
    y = np.array([-math.log(obs.observed_r) for obs in observations], dtype=float)
    return x, y


def _predict_from_row(feature: np.ndarray, coefficients: np.ndarray) -> float:
    return float(math.exp(-float(np.dot(feature, coefficients))))


def fit_model(observations: list[Observation], selected_names: list[str]) -> tuple[np.ndarray, float]:
    selected = [obs for obs in observations if obs.name in selected_names]
    x, y = _as_arrays(selected)
    coefficients, *_ = np.linalg.lstsq(x, y, rcond=None)
    condition_number = float(np.linalg.cond(x))
    return coefficients, condition_number


def make_rows(observations: list[Observation], coefficients: np.ndarray, kind: str) -> list[FitRow]:
    rows: list[FitRow] = []
    for obs in observations:
        predicted = _predict_from_row(obs.feature, coefficients)
        residual = predicted - obs.observed_r
        pull = None
        if obs.observed_r > 0:
            pull = residual / obs.observed_r
        rows.append(
            FitRow(
                name=obs.name,
                observed_r=obs.observed_r,
                predicted_r=predicted,
                residual=residual,
                pull=pull,
                kind=kind,
            )
        )
    return rows


def leave_one_out(observations: list[Observation], selected_names: list[str]) -> list[FitRow]:
    selected = [obs for obs in observations if obs.name in selected_names]
    rows: list[FitRow] = []
    for idx, omitted in enumerate(selected):
        training = [obs for j, obs in enumerate(selected) if j != idx]
        coefficients, _ = fit_model(training, [obs.name for obs in training])
        predicted = _predict_from_row(omitted.feature, coefficients)
        residual = predicted - omitted.observed_r
        rows.append(
            FitRow(
                name=omitted.name,
                observed_r=omitted.observed_r,
                predicted_r=predicted,
                residual=residual,
                pull=None if omitted.observed_r == 0 else residual / omitted.observed_r,
                kind="loo",
            )
        )
    return rows


def run_analysis(observations: list[Observation], selected_names: list[str] | None = None) -> AnalysisResult:
    if selected_names is None:
        selected_names = anchor_names(observations)

    dataset = load_dataset()
    source_mean_51 = source_mean_cross_section(dataset, "51Cr")
    source_mean_37 = source_mean_cross_section(dataset, "37Ar")

    coefficients, condition_number = fit_model(observations, selected_names)
    anchor_obs = [obs for obs in observations if obs.name in selected_names]
    validation_obs = [obs for obs in observations if obs.name not in selected_names]

    anchor_rows = make_rows(anchor_obs, coefficients, kind="anchor")
    validation_rows = make_rows(validation_obs, coefficients, kind="validation")
    loo_rows = leave_one_out(observations, selected_names)

    return AnalysisResult(
        coefficients=coefficients,
        coefficient_names=list(COEFFICIENT_NAMES),
        condition_number=condition_number,
        anchor_rows=anchor_rows,
        validation_rows=validation_rows,
        loo_rows=loo_rows,
        source_mean_51cr_cm2=float(source_mean_51),
        source_mean_37ar_cm2=float(source_mean_37),
        anchor_set=list(selected_names),
    )
