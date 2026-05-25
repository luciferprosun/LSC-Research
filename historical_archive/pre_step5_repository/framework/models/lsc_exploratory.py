from __future__ import annotations

from typing import Iterable

from loaders.gallium_loader import GalliumPoint


def predict(points: Iterable[GalliumPoint], alpha: float = 0.0) -> dict[str, float]:
    """
    Exploratory placeholder only.
    Kept separate from validated baselines by design.
    """
    return {f"{p.experiment}:{p.label}": (1.0 + alpha) for p in points}
