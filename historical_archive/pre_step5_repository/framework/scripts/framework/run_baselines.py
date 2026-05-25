#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from baselines import null_model, sterile_baseline
from likelihood.chi2 import chi2
from loaders.gallium_loader import extract_ratio_points, load_dataset


def main() -> None:
    dataset_path = REPO_ROOT / "data/raw/gallium_core_dataset.json"
    if not dataset_path.exists():
        raise SystemExit(f"Missing dataset: {dataset_path}")

    dataset = load_dataset(dataset_path)
    points = extract_ratio_points(dataset)
    if not points:
        raise SystemExit("No usable ratio points found in dataset.")

    null_pred = null_model.predict(points)
    sterile_pred = sterile_baseline.predict(points)

    null_res = chi2(points, null_pred)
    sterile_res = chi2(points, sterile_pred)

    print("points:", len(points))
    print(f"null chi2={null_res.chi2:.4f} ndof={null_res.ndof}")
    print(f"sterile_baseline chi2={sterile_res.chi2:.4f} ndof={sterile_res.ndof}")


if __name__ == "__main__":
    main()
