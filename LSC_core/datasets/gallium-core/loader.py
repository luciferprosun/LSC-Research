from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATASET_PATH = Path(__file__).with_name("dataset.json")


def load_dataset(path: str | Path = DATASET_PATH) -> dict[str, Any]:
    """Load the neutrino source-experiment dataset."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_experiment(name: str, path: str | Path = DATASET_PATH) -> dict[str, Any] | None:
    """Return an experiment by case-insensitive short or full name."""
    needle = name.strip().casefold()
    dataset = load_dataset(path)
    for experiment in dataset.get("experiments", []):
        names = [
            str(experiment.get("experiment_name", "")),
            str(experiment.get("full_name", "")),
        ]
        if any(needle == candidate.casefold() for candidate in names):
            return experiment
    return None


if __name__ == "__main__":
    data = load_dataset()
    print(f"experiments={len(data.get('experiments', []))}")
    best = get_experiment("BEST")
    if best:
        print(best["experiment_name"], best["measured_results"][0]["R"])
