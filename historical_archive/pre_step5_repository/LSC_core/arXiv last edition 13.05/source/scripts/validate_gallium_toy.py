#!/usr/bin/env python3
"""Toy validation for the LSC arXiv package.

This script intentionally uses only the Python standard library. It is not a
full gallium likelihood. It provides a transparent baseline comparison using
public summary ratios and diagonal uncertainties.

Improvements over the earlier draft:
- fit linear toy templates rather than hard-coding offsets where possible;
- report AICc and BIC in addition to chi2/AIC;
- include leave-one-out predictive residuals for simple overfit pressure;
- separate BEST-only anisotropy from common suppression more cleanly.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "gallium_source_summary.csv"
OUT = ROOT / "outputs"


def read_rows() -> list[dict[str, str]]:
    with DATA.open(newline="") as f:
        return list(csv.DictReader(f))


def weighted_mean(values: list[float], sigmas: list[float]) -> float:
    weights = [1.0 / (s * s) for s in sigmas]
    return sum(w * v for w, v in zip(weights, values)) / sum(weights)


def chi2(values: list[float], sigmas: list[float], preds: list[float]) -> float:
    return sum(((v - p) / s) ** 2 for v, s, p in zip(values, sigmas, preds))


def aicc(chi2_value: float, n_points: int, n_params: int) -> float:
    aic = chi2_value + 2 * n_params
    denom = n_points - n_params - 1
    if denom <= 0:
        return float("inf")
    return aic + (2 * n_params * (n_params + 1)) / denom


def bic(chi2_value: float, n_points: int, n_params: int) -> float:
    return chi2_value + n_params * math.log(n_points)


def fit_constant(values: list[float], sigmas: list[float]) -> float:
    return weighted_mean(values, sigmas)


def fit_linear_template(
    values: list[float], sigmas: list[float], template: list[float]
) -> tuple[float, float]:
    weights = [1.0 / (s * s) for s in sigmas]
    sw = sum(weights)
    st = sum(w * t for w, t in zip(weights, template))
    stt = sum(w * t * t for w, t in zip(weights, template))
    sy = sum(w * y for w, y in zip(weights, values))
    sty = sum(w * t * y for w, t, y in zip(weights, template, values))
    det = sw * stt - st * st
    if abs(det) < 1e-12:
        return fit_constant(values, sigmas), 0.0
    c0 = (sy * stt - st * sty) / det
    c1 = (sw * sty - st * sy) / det
    return c0, c1


def predict_constant(n_rows: int, value: float) -> list[float]:
    return [value for _ in range(n_rows)]


def best_anisotropy_template(rows: list[dict[str, str]]) -> list[float]:
    template = []
    for row in rows:
        zone = row["zone"].strip().lower()
        if zone == "inner":
            template.append(1.0)
        elif zone == "outer":
            template.append(-1.0)
        else:
            template.append(0.0)
    return template


def source_template(rows: list[dict[str, str]], source_name: str) -> list[float]:
    return [1.0 if row["source"] == source_name else 0.0 for row in rows]


def leave_one_out_chi2(
    rows: list[dict[str, str]],
    model_name: str,
    values: list[float],
    sigmas: list[float],
) -> tuple[float, list[float]]:
    preds = []
    for idx in range(len(rows)):
        train_rows = [row for j, row in enumerate(rows) if j != idx]
        train_values = [v for j, v in enumerate(values) if j != idx]
        train_sigmas = [s for j, s in enumerate(sigmas) if j != idx]
        pred = model_predictions(train_rows)[model_name][idx if idx < len(train_rows) else -1]
        if model_name == "M0_null_ratio_1":
            pred = 1.0
        preds.append(pred)
    loo = sum(((v - p) / s) ** 2 for v, s, p in zip(values, sigmas, preds))
    return loo, preds


def leave_one_out_predictions(
    rows: list[dict[str, str]], values: list[float], sigmas: list[float]
) -> dict[str, tuple[float, list[float]]]:
    results = {}
    for model_name in [
        "M0_null_ratio_1",
        "M1_nuisance_only",
        "M3_toy_sterile_averaged",
        "M5_lsc_trace_only",
        "M6_lsc_trace_plus_best_anisotropy",
    ]:
        preds = []
        for idx in range(len(rows)):
            train_rows = [row for j, row in enumerate(rows) if j != idx]
            train_values = [v for j, v in enumerate(values) if j != idx]
            train_sigmas = [s for j, s in enumerate(sigmas) if j != idx]
            train_preds = model_predictions(train_rows)
            if model_name == "M0_null_ratio_1":
                pred = 1.0
            elif model_name == "M6_lsc_trace_plus_best_anisotropy":
                row = rows[idx]
                zone = row["zone"].strip().lower()
                params = fit_model_parameters(train_rows, train_values, train_sigmas)
                pred = params[model_name]["c0"]
                if zone == "inner":
                    pred += params[model_name]["c1"]
                elif zone == "outer":
                    pred -= params[model_name]["c1"]
            else:
                if model_name == "M3_toy_sterile_averaged":
                    pred = train_preds[model_name][0]
                else:
                    pred = train_preds[model_name][0]
            preds.append(pred)
        loo = sum(((v - p) / s) ** 2 for v, s, p in zip(values, sigmas, preds))
        results[model_name] = (loo, preds)
    return results


def fit_model_parameters(
    rows: list[dict[str, str]], values: list[float], sigmas: list[float]
) -> dict[str, dict[str, float]]:
    nuisance = fit_constant(values, sigmas)
    best_template = best_anisotropy_template(rows)
    c0_best, c1_best = fit_linear_template(values, sigmas, best_template)

    # Sterile-like toy benchmark remains a one-parameter common deficit.
    sterile_level = 0.80

    return {
        "M1_nuisance_only": {"c0": nuisance},
        "M3_toy_sterile_averaged": {"c0": sterile_level},
        "M5_lsc_trace_only": {"c0": nuisance},
        "M6_lsc_trace_plus_best_anisotropy": {"c0": c0_best, "c1": c1_best},
    }


def model_predictions(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    values = [float(r["ratio"]) for r in rows]
    sigmas = [float(r["total_uncertainty"]) for r in rows]
    params = fit_model_parameters(rows, values, sigmas)
    n = len(rows)
    best_template = best_anisotropy_template(rows)

    return {
        "M0_null_ratio_1": [1.0 for _ in rows],
        "M1_nuisance_only": predict_constant(n, params["M1_nuisance_only"]["c0"]),
        "M3_toy_sterile_averaged": predict_constant(
            n, params["M3_toy_sterile_averaged"]["c0"]
        ),
        "M5_lsc_trace_only": predict_constant(n, params["M5_lsc_trace_only"]["c0"]),
        "M6_lsc_trace_plus_best_anisotropy": [
            params["M6_lsc_trace_plus_best_anisotropy"]["c0"]
            + params["M6_lsc_trace_plus_best_anisotropy"]["c1"] * t
            for t in best_template
        ],
    }


def write_model_comparison(rows: list[dict[str, str]], preds: dict[str, list[float]]) -> None:
    values = [float(r["ratio"]) for r in rows]
    sigmas = [float(r["total_uncertainty"]) for r in rows]
    n = len(values)
    loo = leave_one_out_predictions(rows, values, sigmas)

    model_params = {
        "M0_null_ratio_1": 0,
        "M1_nuisance_only": 1,
        "M3_toy_sterile_averaged": 1,
        "M5_lsc_trace_only": 1,
        "M6_lsc_trace_plus_best_anisotropy": 2,
    }

    OUT.mkdir(exist_ok=True)
    with (OUT / "model_comparison.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "model",
                "chi2",
                "n_points",
                "n_parameters",
                "dof",
                "reduced_chi2",
                "aic",
                "aicc",
                "bic",
                "loo_chi2",
            ]
        )
        for name, pred in preds.items():
            c2 = chi2(values, sigmas, pred)
            k = model_params[name]
            dof = max(n - k, 1)
            loo_chi2_value = loo[name][0]
            writer.writerow(
                [
                    name,
                    f"{c2:.6f}",
                    n,
                    k,
                    dof,
                    f"{c2 / dof:.6f}",
                    f"{c2 + 2 * k:.6f}",
                    f"{aicc(c2, n, k):.6f}",
                    f"{bic(c2, n, k):.6f}",
                    f"{loo_chi2_value:.6f}",
                ]
            )


def write_residuals(rows: list[dict[str, str]], preds: dict[str, list[float]]) -> None:
    with (OUT / "residuals.csv").open("w", newline="") as f:
        fieldnames = [
            "experiment",
            "source",
            "zone",
            "ratio",
            "sigma",
            "model",
            "prediction",
            "residual",
            "pull",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, row in enumerate(rows):
            ratio = float(row["ratio"])
            sigma = float(row["total_uncertainty"])
            for name, pred in preds.items():
                residual = ratio - pred[i]
                writer.writerow(
                    {
                        "experiment": row["experiment"],
                        "source": row["source"],
                        "zone": row["zone"],
                        "ratio": f"{ratio:.6f}",
                        "sigma": f"{sigma:.6f}",
                        "model": name,
                        "prediction": f"{pred[i]:.6f}",
                        "residual": f"{residual:.6f}",
                        "pull": f"{residual / sigma:.6f}",
                    }
                )


def write_parameter_summary(rows: list[dict[str, str]]) -> None:
    values = [float(r["ratio"]) for r in rows]
    sigmas = [float(r["total_uncertainty"]) for r in rows]
    params = fit_model_parameters(rows, values, sigmas)

    with (OUT / "model_parameters.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "parameter", "value"])
        for model, model_params in params.items():
            for name, value in model_params.items():
                writer.writerow([model, name, f"{value:.6f}"])


def write_summary(rows: list[dict[str, str]], preds: dict[str, list[float]]) -> None:
    values = [float(r["ratio"]) for r in rows]
    sigmas = [float(r["total_uncertainty"]) for r in rows]
    wm = weighted_mean(values, sigmas)
    wm_sigma = math.sqrt(1.0 / sum(1.0 / (s * s) for s in sigmas))
    null_chi2 = chi2(values, sigmas, preds["M0_null_ratio_1"])
    comparison_rows = list(csv.DictReader((OUT / "model_comparison.csv").open()))
    best_aicc_row = min(comparison_rows, key=lambda row: float(row["aicc"]))

    lines = [
        "# Toy Gallium Validation Summary",
        "",
        f"Number of public summary points: {len(rows)}",
        f"Weighted mean ratio: {wm:.4f} +/- {wm_sigma:.4f}",
        f"Null-model chi2 against ratio=1: {null_chi2:.4f}",
        f"Best AICc model in this toy comparison: {best_aicc_row['model']}",
        "",
        "Interpretation:",
        "This is a diagonal-error toy validation using public summary ratios.",
        "It is not a full official likelihood reproduction and does not use a covariance matrix.",
        "The BEST anisotropy toy is now fit as a common suppression plus an inner/outer contrast term,",
        "which is cleaner than hard-coding fixed offsets by hand.",
    ]
    (OUT / "validation_summary.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    rows = read_rows()
    preds = model_predictions(rows)
    write_model_comparison(rows, preds)
    write_residuals(rows, preds)
    write_parameter_summary(rows)
    write_summary(rows, preds)
    print("Wrote outputs to", OUT)


if __name__ == "__main__":
    main()
