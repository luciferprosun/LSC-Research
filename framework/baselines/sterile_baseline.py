from __future__ import annotations

import math
from typing import Iterable

from loaders.gallium_loader import GalliumPoint


def predict(
    points: Iterable[GalliumPoint],
    sin2_2theta: float = 0.08,
    dm2: float = 1.5,
) -> dict[str, float]:
    """
    Lightweight sterile-neutrino baseline placeholder.
    This is intentionally simple and must be replaced by dataset-accurate L/E mapping.
    """
    predictions: dict[str, float] = {}
    for idx, point in enumerate(points, start=1):
        l_over_e = 1.0 + 0.1 * idx
        osc = sin2_2theta * math.sin(1.27 * dm2 * l_over_e) ** 2
        predictions[f"{point.experiment}:{point.label}"] = 1.0 - osc
    return predictions
