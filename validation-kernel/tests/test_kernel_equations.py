from __future__ import annotations

import unittest

from lsc_kernel.errors import FrozenEquationBlocked
from lsc_kernel.frozen.dependency_graph import dependency_edges, graph_as_dict, topological_order
from lsc_kernel.frozen.equations import equation_descriptors, execute_algebraic_equation


class EquationTests(unittest.TestCase):
    def test_exact_symbolic_e1_e12_set_is_loadable(self) -> None:
        equations = equation_descriptors()
        self.assertEqual([item.equation_id for item in equations], [f"E{i}" for i in range(1, 13)])
        self.assertTrue(all(item.provenance_status == "AUTHENTIC_FROZEN" for item in equations))

    def test_only_non_predictive_algebraic_parts_execute(self) -> None:
        self.assertEqual(execute_algebraic_equation("E6", N_obs_a=8, N0_a=10), 0.8)
        result = execute_algebraic_equation("E9", R_inner=0.8, R_outer=0.72)
        self.assertEqual(result[:2], (0.8, 0.72))
        self.assertAlmostEqual(result[2], 0.9)
        tensor = execute_algebraic_equation("E4", A_a_ij=[[1.0, 0.0], [0.0, -1.0]])
        self.assertTrue(tensor["symmetric"])
        self.assertTrue(tensor["traceless"])

    def test_lsc_response_equation_remains_blocked(self) -> None:
        with self.assertRaises(FrozenEquationBlocked):
            execute_algebraic_equation("E2")

    def test_division_by_zero_is_rejected(self) -> None:
        with self.assertRaises(FrozenEquationBlocked):
            execute_algebraic_equation("E6", N_obs_a=1, N0_a=0)

    def test_dependency_graph_is_deterministic_and_acyclic(self) -> None:
        first = graph_as_dict()
        second = graph_as_dict()
        self.assertEqual(first, second)
        self.assertEqual(len(topological_order()), 12)
        self.assertEqual(set(topological_order()), {f"E{i}" for i in range(1, 13)})

    def test_unverified_dependencies_remain_explicit(self) -> None:
        uncertain = [edge for edge in dependency_edges() if edge.status == "UNVERIFIED_DEPENDENCY"]
        self.assertEqual({(edge.source, edge.target) for edge in uncertain}, {("E5", "E10"), ("E7", "E10")})


if __name__ == "__main__":
    unittest.main()
