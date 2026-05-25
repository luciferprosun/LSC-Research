from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


DATA_ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = DATA_ROOT / "data" / "dataset.json"


@dataclass(frozen=True)
class Observation:
    name: str
    experiment: str
    source: str
    observed_r: float
    feature: np.ndarray
    anchor: bool
    citation: str
    notes: str = ""


def load_dataset(path: str | Path = DATASET_PATH) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _exp_map(dataset: dict) -> dict[str, dict]:
    return {str(exp["experiment_name"]): exp for exp in dataset.get("experiments", [])}


def source_mean_cross_section(dataset: dict, isotope: str) -> float:
    rows = dataset["source_line_library"][isotope]
    return sum(float(row["intensity"]) * float(row["cross_section_cm2"]) for row in rows)


def effective_length_proxy(experiment: str, geometry: dict, label: str | None = None) -> float:
    if experiment == "BEST" and label == "inner_zone":
        radius = float(geometry["dimensions"]["inner_zone"]["radius_m"])
        return 4.0 * radius / 3.0

    if experiment == "BEST" and label == "outer_zone":
        zone = geometry["dimensions"]["outer_zone"]
        radius = float(zone["radius_m"])
        height = float(zone["height_m"])
        return (radius + height / 2.0) / 2.0

    if experiment == "GALLEX":
        dims = geometry["dimensions"]
        radius = float(dims["tank_diameter_m"]) / 2.0
        height = float(dims["tank_height_m"])
        return (radius + height / 2.0) / 2.0

    if experiment == "SAGE":
        dims = geometry["dimensions"]
        radius = float(dims["cylinder_radius_m"])
        height = float(dims["cylinder_height_m"])
        return (radius + height / 2.0) / 2.0

    raise KeyError(f"Unsupported geometry for {experiment!r}")


def shape_anisotropy_proxy(experiment: str, geometry: dict, label: str | None = None) -> float:
    if experiment == "BEST" and label == "inner_zone":
        return 0.0

    if experiment == "BEST" and label == "outer_zone":
        zone = geometry["dimensions"]["outer_zone"]
        radius = float(zone["radius_m"])
        height = float(zone["height_m"])
    elif experiment == "GALLEX":
        dims = geometry["dimensions"]
        radius = float(dims["tank_diameter_m"]) / 2.0
        height = float(dims["tank_height_m"])
    elif experiment == "SAGE":
        dims = geometry["dimensions"]
        radius = float(dims["cylinder_radius_m"])
        height = float(dims["cylinder_height_m"])
    else:
        raise KeyError(f"Unsupported geometry for {experiment!r}")

    radial_moment = radius * radius / 4.0
    axial_moment = height * height / 12.0
    return abs(axial_moment - radial_moment) / (axial_moment + 2.0 * radial_moment)


def feature_vector(
    experiment: str,
    geometry: dict,
    source_isotope: str,
    label: str | None = None,
    zone_split: float = 0.0,
    source_norm: float | None = None,
) -> np.ndarray:
    if source_norm is None:
        raise ValueError("source_norm is required")

    length = effective_length_proxy(experiment, geometry, label=label)
    shape = shape_anisotropy_proxy(experiment, geometry, label=label)
    return np.array(
        [
            1.0 / length,
            shape,
            source_norm,
            zone_split,
            1.0,
        ],
        dtype=float,
    )


def _result_lookup(experiment: dict) -> dict[str, dict]:
    return {str(item["label"]): item for item in experiment.get("measured_results", [])}


def build_observations(dataset: dict | None = None) -> list[Observation]:
    dataset = load_dataset() if dataset is None else dataset
    exps = _exp_map(dataset)

    source_51 = source_mean_cross_section(dataset, "51Cr") / 1e-45
    source_37 = source_mean_cross_section(dataset, "37Ar") / 1e-45

    best = exps["BEST"]
    gallex = exps["GALLEX"]
    sage = exps["SAGE"]

    best_results = _result_lookup(best)
    gallex_results = _result_lookup(gallex)
    sage_results = _result_lookup(sage)

    obs: list[Observation] = []

    inner_feature = feature_vector(
        "BEST",
        best["detector_geometry"],
        "51Cr",
        label="inner_zone",
        zone_split=-1.0,
        source_norm=source_51,
    )
    outer_feature = feature_vector(
        "BEST",
        best["detector_geometry"],
        "51Cr",
        label="outer_zone",
        zone_split=1.0,
        source_norm=source_51,
    )

    obs.append(
        Observation(
            name="BEST_inner",
            experiment="BEST",
            source="51Cr",
            observed_r=float(best_results["inner_zone"]["R"]),
            feature=inner_feature,
            anchor=True,
            citation="BEST PRL 2022",
            notes="Inner target volume.",
        )
    )
    obs.append(
        Observation(
            name="BEST_outer",
            experiment="BEST",
            source="51Cr",
            observed_r=float(best_results["outer_zone"]["R"]),
            feature=outer_feature,
            anchor=True,
            citation="BEST PRL 2022",
            notes="Outer target volume.",
        )
    )
    obs.append(
        Observation(
            name="BEST_ratio",
            experiment="BEST",
            source="51Cr",
            observed_r=float(best_results["outer_to_inner_ratio"]["R"]),
            feature=outer_feature - inner_feature,
            anchor=False,
            citation="BEST PRL 2022",
            notes="Derived ratio R_outer / R_inner.",
        )
    )

    gallex_feature = feature_vector(
        "GALLEX",
        gallex["detector_geometry"],
        "51Cr",
        source_norm=source_51,
    )

    obs.extend(
        [
            Observation(
                name="GALLEX_Cr1",
                experiment="GALLEX",
                source="51Cr",
                observed_r=float(gallex_results["Cr1_reanalysis_or_common_ga_anomaly_table"]["R"]),
                feature=gallex_feature,
                anchor=False,
                citation="GALLEX reanalysis 2010",
                notes="Cr1 reanalysis/common-gallium value.",
            ),
            Observation(
                name="GALLEX_Cr2",
                experiment="GALLEX",
                source="51Cr",
                observed_r=float(gallex_results["Cr2_reanalysis_or_common_ga_anomaly_table"]["R"]),
                feature=gallex_feature,
                anchor=False,
                citation="GALLEX reanalysis 2010",
                notes="Cr2 reanalysis/common-gallium value.",
            ),
            Observation(
                name="GALLEX_combined",
                experiment="GALLEX",
                source="51Cr",
                observed_r=float(gallex_results["combined_reanalysis_2010"]["R"]),
                feature=gallex_feature,
                anchor=True,
                citation="GALLEX reanalysis 2010",
                notes="Combined reanalysis value.",
            ),
        ]
    )

    sage_feature_51 = feature_vector(
        "SAGE",
        sage["detector_geometry"],
        "51Cr",
        source_norm=source_51,
    )
    sage_feature_37 = feature_vector(
        "SAGE",
        sage["detector_geometry"],
        "37Ar",
        source_norm=source_37,
    )

    obs.extend(
        [
            Observation(
                name="SAGE_51Cr",
                experiment="SAGE",
                source="51Cr",
                observed_r=float(sage_results["SAGE_51Cr"]["R"]),
                feature=sage_feature_51,
                anchor=True,
                citation="SAGE PRL 1996 / PRC 1999",
                notes="Cr-51 source calibration.",
            ),
            Observation(
                name="SAGE_37Ar",
                experiment="SAGE",
                source="37Ar",
                observed_r=float(sage_results["SAGE_37Ar"]["R"]),
                feature=sage_feature_37,
                anchor=True,
                citation="SAGE PRC 2006",
                notes="Ar-37 source calibration.",
            ),
        ]
    )

    return obs


def anchor_names(observations: Iterable[Observation]) -> list[str]:
    return [obs.name for obs in observations if obs.anchor]

