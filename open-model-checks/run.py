"""Reproduce the two model checks and their report using Python 3.10+ only."""

import csv
import json
import math
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TRAIN_END = "2017-12"
PERIOD = 132  # Demonstration choice: eleven years at monthly cadence.
DELAY = 12


def read_rows(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def check_gallium():
    rates = {row["zone"]: Decimal(row["ratio"]) for row in read_rows("best-rates.csv")}
    inner, outer = rates["inner"], rates["outer"]
    # These two response factors are invented solely to illustrate an identity.
    factors = [Decimal("0.71"), Decimal("0.87")]
    equal_weights = [Decimal("0.5"), Decimal("0.5")]
    changed_weights = [Decimal("0.8"), Decimal("0.2")]
    shared = sum(weight * factor for weight, factor in zip(equal_weights, factors))
    changed = sum(weight * factor for weight, factor in zip(changed_weights, factors))
    assert shared == inner and changed != inner
    return {
        "best_inner_observed": str(inner),
        "best_outer_observed": str(outer),
        "shared_weights_outer_prediction_both_models": str(shared),
        "outer_observed_minus_prediction": str(outer - shared),
        "synthetic_changed_weights_outer_response": str(changed),
        "free_normalization_outer_response": str(inner),
    }


def dot(left, right):
    return math.fsum(a * b for a, b in zip(left, right))


def least_squares(rows, targets):
    """Solve full-rank least squares by modified Gram–Schmidt and back-substitution."""
    columns = list(zip(*rows))
    size = len(columns)
    q = []
    r = [[0.0] * size for _ in columns]
    for j, column in enumerate(columns):
        residual = list(column)
        for i, basis in enumerate(q):
            projection = dot(basis, residual)
            r[i][j] = projection
            residual = [x - projection * b for x, b in zip(residual, basis)]
        r[j][j] = math.sqrt(dot(residual, residual))
        if r[j][j] < 1e-10:
            raise ValueError("Rank-deficient training features")
        q.append([x / r[j][j] for x in residual])

    coefficients = [0.0] * size
    for i in reversed(range(size)):
        known = math.fsum(r[i][j] * coefficients[j] for j in range(i + 1, size))
        coefficients[i] = (dot(q[i], targets) - known) / r[i][i]
    return coefficients


def check_solar_flux():
    rows = read_rows("f107-monthly.csv")
    months = [row["month"] for row in rows]
    expected = [f"{year}-{month:02d}" for year in range(2005, 2025) for month in range(1, 13)]
    if months != expected:
        raise ValueError("The input must contain all 240 frozen months in order")
    flux = [float(row["flux_sfu"]) for row in rows]
    if any(not math.isfinite(value) or value <= 0.0 for value in flux):
        raise ValueError("Every observed monthly flux must be finite and positive")
    split = months.index(TRAIN_END) + 1
    train = flux[:split]
    mean = math.fsum(train) / len(train)
    scale = math.sqrt(math.fsum((x - mean) ** 2 for x in train) / len(train))
    z = [(x - mean) / scale for x in flux]

    def features(t, hnc):
        phase = 2 * math.pi * t / PERIOD
        prior = z[t - 1]
        return [1.0, math.sin(phase), math.cos(phase), math.tanh(prior) if hnc else prior, z[t - DELAY]]

    fit = range(DELAY, split)
    holdout = range(split, len(z))
    target = [z[i] for i in fit]
    linear = least_squares([features(i, False) for i in fit], target)
    hnc = least_squares([features(i, True) for i in fit], target)
    predictions = [
        {
            "month": months[i],
            "observed_sfu": flux[i],
            "persistence_sfu": flux[i - 1],
            "linear_sfu": mean + scale * dot(linear, features(i, False)),
            "hnc_sfu": mean + scale * dot(hnc, features(i, True)),
        }
        for i in holdout
    ]

    def score(field):
        errors = [row[field] - row["observed_sfu"] for row in predictions]
        return {
            "rmse_sfu": round(math.sqrt(math.fsum(e * e for e in errors) / len(errors)), 6),
            "mae_sfu": round(math.fsum(abs(e) for e in errors) / len(errors), 6),
        }

    metrics = {
        "fit_targets": len(fit),
        "fit_end": TRAIN_END,
        "test_targets": len(holdout),
        "test_first": months[split],
        "test_last": months[-1],
        "persistence": score("persistence_sfu"),
        "matched_linear": score("linear_sfu"),
        "hnc_inspired": score("hnc_sfu"),
    }
    return metrics, predictions


def main():
    gallium = check_gallium()
    solar, predictions = check_solar_flux()
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    summary = {"gallium": gallium, "solar_flux": solar}
    (results / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (results / "f107-holdout.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(predictions[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: round(v, 6) if isinstance(v, float) else v for k, v in row.items()} for row in predictions)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
