from __future__ import annotations

import math
import unittest

from lsc621.data import build_observations, load_dataset, source_mean_cross_section
from lsc621.model import run_analysis


class LSC621Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = load_dataset()
        cls.observations = build_observations(cls.dataset)
        cls.analysis = run_analysis(cls.observations)

    def test_dataset_loads(self) -> None:
        self.assertIn("experiments", self.dataset)
        self.assertGreaterEqual(len(self.dataset["experiments"]), 3)

    def test_source_means(self) -> None:
        self.assertAlmostEqual(source_mean_cross_section(self.dataset, "51Cr"), 5.749407e-45, delta=1e-50)
        self.assertAlmostEqual(source_mean_cross_section(self.dataset, "37Ar"), 7.01196e-45, delta=1e-50)

    def test_anchor_fit_is_exact(self) -> None:
        for row in self.analysis.anchor_rows:
            self.assertAlmostEqual(row.observed_r, row.predicted_r, places=12)

    def test_best_ratio_is_close(self) -> None:
        ratio_pred = next(row.predicted_r for row in self.analysis.validation_rows if row.name == "BEST_ratio")
        self.assertAlmostEqual(ratio_pred, 0.9746835443, places=9)

    def test_gallex_split_is_not_exact(self) -> None:
        c1 = next(row.predicted_r for row in self.analysis.validation_rows if row.name == "GALLEX_Cr1")
        c2 = next(row.predicted_r for row in self.analysis.validation_rows if row.name == "GALLEX_Cr2")
        self.assertAlmostEqual(c1, c2, places=12)
        self.assertTrue(0.87 < c1 < 0.89)

    def test_loo_has_signal(self) -> None:
        worst = max(abs(row.residual) for row in self.analysis.loo_rows)
        self.assertGreater(worst, 0.15)


if __name__ == "__main__":
    unittest.main()
