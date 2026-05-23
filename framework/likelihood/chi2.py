from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from loaders.gallium_loader import GalliumPoint


@dataclass(frozen=True)
class Chi2Result:
    chi2: float
    ndof: int


def chi2(points: Iterable[GalliumPoint], predictions: dict[str, float]) -> Chi2Result:
    total = 0.0
    n = 0
    for point in points:
        key = f"{point.experiment}:{point.label}"
        pred = predictions.get(key)
        if pred is None:
            continue
        total += ((point.ratio - pred) / point.sigma) ** 2
        n += 1
    return Chi2Result(chi2=total, ndof=max(n - 1, 0))
