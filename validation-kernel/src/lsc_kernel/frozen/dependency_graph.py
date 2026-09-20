"""Deterministic dependency DAG for E1-E12 without invented sequential edges."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from lsc_kernel.errors import FrozenEquationBlocked
from lsc_kernel.frozen.equations import equation_descriptors


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: str
    target: str
    status: str
    rationale: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def dependency_edges() -> tuple[DependencyEdge, ...]:
    return (
        DependencyEdge("E1", "E6", "SOURCE_DERIVED_DEPENDENCY", "E6 consumes N0_a from E1."),
        DependencyEdge(
            "E1",
            "E8",
            "SOURCE_DERIVED_DEPENDENCY",
            "E8 requires the same flux, cross-section, geometry, and exposure weighting used in E1.",
        ),
        DependencyEdge("E2", "E5", "SOURCE_DERIVED_DEPENDENCY", "E5 consumes epsilon_LSC,a from E2."),
        DependencyEdge("E3", "E2", "SOURCE_DERIVED_DEPENDENCY", "E2 consumes q_a from E3."),
        DependencyEdge("E3", "E8", "SOURCE_DERIVED_DEPENDENCY", "E8 consumes q_a from E3."),
        DependencyEdge("E4", "E3", "SOURCE_DERIVED_DEPENDENCY", "E4 constrains the tensor used by E3."),
        DependencyEdge("E4", "E12", "SOURCE_DERIVED_DEPENDENCY", "E4 constrains the tensor used by E12."),
        DependencyEdge("E6", "E9", "SOURCE_DERIVED_DEPENDENCY", "E9 is assembled from inner and outer ratios."),
        DependencyEdge("E6", "E10", "SOURCE_DERIVED_DEPENDENCY", "E10 consumes observed ratios."),
        DependencyEdge("E7", "E10", "UNVERIFIED_DEPENDENCY", "E7 may provide R_pred residuals, but the source does not freeze this binding."),
        DependencyEdge("E8", "E7", "SOURCE_DERIVED_DEPENDENCY", "E7 consumes F0_a and FA_a from E8."),
        DependencyEdge("E5", "E10", "UNVERIFIED_DEPENDENCY", "E5 may provide predictions for E10, but the exact ratio binding is not frozen."),
        DependencyEdge("E11", "E3", "SOURCE_DERIVED_DEPENDENCY", "E11 produces n_lab used by E3."),
        DependencyEdge("E11", "E12", "SOURCE_DERIVED_DEPENDENCY", "E11 produces n_lab used by E12."),
    )


def _equation_key(equation_id: str) -> int:
    return int(equation_id[1:])


def topological_order(edges: Iterable[DependencyEdge] | None = None) -> tuple[str, ...]:
    nodes = {descriptor.equation_id for descriptor in equation_descriptors()}
    graph_edges = tuple(edges if edges is not None else dependency_edges())
    incoming = {node: 0 for node in nodes}
    outgoing: dict[str, list[str]] = {node: [] for node in nodes}
    for edge in graph_edges:
        if edge.source not in nodes or edge.target not in nodes:
            raise FrozenEquationBlocked("Dependency graph references an unknown equation.")
        incoming[edge.target] += 1
        outgoing[edge.source].append(edge.target)
    ready = sorted((node for node, count in incoming.items() if count == 0), key=_equation_key)
    ordered: list[str] = []
    while ready:
        node = ready.pop(0)
        ordered.append(node)
        for target in sorted(outgoing[node], key=_equation_key):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort(key=_equation_key)
    if len(ordered) != len(nodes):
        raise FrozenEquationBlocked("The equation dependency graph contains a cycle.")
    return tuple(ordered)


def graph_as_dict() -> dict[str, Any]:
    descriptors = equation_descriptors()
    edges = dependency_edges()
    return {
        "schema_version": "1.0.0",
        "graph_type": "DIRECTED_ACYCLIC_GRAPH",
        "nodes": [descriptor.equation_id for descriptor in descriptors],
        "edges": [edge.as_dict() for edge in edges],
        "topological_order": list(topological_order(edges)),
        "policy": "No sequential edge is implied merely by equation numbering.",
    }


def graph_as_markdown() -> str:
    graph = graph_as_dict()
    lines = [
        "# E1-E12 Dependency Graph",
        "",
        "This is a source-bounded DAG. Equation numbers do not imply a sequential chain.",
        "",
        f"Topological order: `{' -> '.join(graph['topological_order'])}`",
        "",
        "| From | To | Status | Rationale |",
        "|---|---|---|---|",
    ]
    for edge in dependency_edges():
        lines.append(f"| `{edge.source}` | `{edge.target}` | `{edge.status}` | {edge.rationale} |")
    lines.append("")
    return "\n".join(lines)


def graph_as_dot() -> str:
    lines = ["digraph LSC_E1_E12 {", "  rankdir=LR;"]
    for descriptor in equation_descriptors():
        lines.append(f'  {descriptor.equation_id} [label="{descriptor.equation_id}"];')
    for edge in dependency_edges():
        style = "dashed" if edge.status == "UNVERIFIED_DEPENDENCY" else "solid"
        lines.append(f'  {edge.source} -> {edge.target} [style="{style}"];')
    lines.append("}")
    return "\n".join(lines) + "\n"
