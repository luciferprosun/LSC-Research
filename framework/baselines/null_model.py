from __future__ import annotations

from typing import Iterable

from loaders.gallium_loader import GalliumPoint


def predict(points: Iterable[GalliumPoint], value: float = 1.0) -> dict[str, float]:
    return {f"{p.experiment}:{p.label}": float(value) for p in points}
