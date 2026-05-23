from __future__ import annotations

from baselines.null_model import predict as null_predict
from baselines.sterile_baseline import predict as sterile_predict
from likelihood.chi2 import chi2
from loaders.gallium_loader import GalliumPoint


def sample_points() -> list[GalliumPoint]:
    return [
        GalliumPoint("BEST", "inner_zone", 0.79, 0.05),
        GalliumPoint("BEST", "outer_zone", 0.77, 0.05),
        GalliumPoint("GALLEX", "Cr1_final_1998", 1.01, 0.115),
    ]


def test_null_model_output_size() -> None:
    points = sample_points()
    pred = null_predict(points)
    assert len(pred) == len(points)


def test_sterile_model_output_size() -> None:
    points = sample_points()
    pred = sterile_predict(points)
    assert len(pred) == len(points)


def test_chi2_nonnegative() -> None:
    points = sample_points()
    pred = null_predict(points)
    result = chi2(points, pred)
    assert result.chi2 >= 0.0


def test_leave_one_out_null() -> None:
    points = sample_points()
    for i in range(len(points)):
        subset = [p for j, p in enumerate(points) if j != i]
        pred = null_predict(subset)
        result = chi2(subset, pred)
        assert result.chi2 >= 0.0
