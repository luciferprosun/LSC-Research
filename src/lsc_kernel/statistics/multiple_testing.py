"""Pre-result multiple-testing adjudication frozen in Step 04."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

from .errors import StatisticalInputError


PRIMARY_FAMILY_ID = "LSC_PRIMARY_FIXED_SEQUENCE_V1"
PRIMARY_ORDER = ("T11", "T7", "T3", "T1", "T10")
FAMILY_WISE_ALPHA = 0.05


@dataclass(frozen=True, slots=True)
class PrimaryEndpointPolicy:
    family_id: str = PRIMARY_FAMILY_ID
    tests: tuple[str, ...] = PRIMARY_ORDER
    family_wise_alpha: float = FAMILY_WISE_ALPHA
    strategy: str = "FIXED_SEQUENCE_HIERARCHICAL_GATEKEEPING"
    ordering_basis: str = (
        "Broad simpler-baseline comparison, then cross-experiment generalization, legacy transfer, "
        "within-BEST zone transfer, and finally the more assumption-intensive sterile comparison."
    )
    stop_rule: str = (
        "Test each endpoint at alpha=0.05 in the declared order; stop confirmatory testing at the first "
        "non-rejection, blocker, invalid p-value, or unavailable prerequisite. All later outputs are descriptive."
    )
    selected_without_lsc_results: bool = True

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def fixed_sequence_decisions(p_values: Mapping[str, float | None]) -> dict[str, str]:
    """Apply the frozen rule to supplied test-fixture p-values; no LSC computation occurs here."""
    unknown = set(p_values) - set(PRIMARY_ORDER)
    if unknown:
        raise StatisticalInputError(f"Unknown primary endpoint IDs: {sorted(unknown)}")
    decisions: dict[str, str] = {}
    gate_open = True
    for test_id in PRIMARY_ORDER:
        if not gate_open:
            decisions[test_id] = "DESCRIPTIVE_AFTER_GATE_CLOSED"
            continue
        value = p_values.get(test_id)
        if value is None:
            decisions[test_id] = "BLOCKED_OR_NOT_EVALUATED_STOP"
            gate_open = False
        elif not 0.0 <= float(value) <= 1.0:
            raise StatisticalInputError(f"Invalid p-value for {test_id}.")
        elif float(value) <= FAMILY_WISE_ALPHA:
            decisions[test_id] = "REJECT_LOCAL_NULL_CONTINUE"
        else:
            decisions[test_id] = "DO_NOT_REJECT_STOP"
            gate_open = False
    return decisions


def multiple_testing_dependency_map() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "selected_before_LSC_numerical_evaluation": True,
        "families": {
            "primary": list(PRIMARY_ORDER),
            "secondary_descriptive": ["T2", "T4", "T6"],
            "sensitivity_only": ["T5", "T8", "T9"],
            "exploratory_future": [],
            "blocked": ["T12"],
        },
        "dependencies": [
            {"tests": ["T1", "T2", "T6"], "shared_data": ["BEST"], "independent": False},
            {"tests": ["T3", "T4", "T7", "T11"], "shared_data": ["BEST", "GALLEX_GNO"], "independent": False},
            {"tests": ["T5", "T7", "T8", "T9", "T10", "T11"], "shared_data": ["gallium experiments"], "independent": False},
            {"tests": ["T10"], "shared_data": ["gallium", "external releases after mapping"], "independent": False},
            {"tests": ["T12"], "shared_data": ["directional inputs unavailable"], "independent": "NOT_ASSESSABLE"},
        ],
        "consequence": "Tests are not treated as twelve independent endpoints.",
    }


def adjudicated_multiple_testing_policy() -> dict[str, object]:
    return {
        "schema_version": "2.0.0",
        "status": "MULTIPLE_TESTING_POLICY_FROZEN",
        "adjudication_stage": "STEP_04_BEFORE_ANY_LSC_NUMERICAL_EVALUATION",
        "result_information_used": False,
        "primary_endpoint_policy": PrimaryEndpointPolicy().as_dict(),
        "families": multiple_testing_dependency_map()["families"],
        "dependency_map": multiple_testing_dependency_map()["dependencies"],
        "selected_strategy": {
            "strategy": "FIXED_SEQUENCE_HIERARCHICAL_GATEKEEPING",
            "justification": [
                "Primary questions are scientifically ordered and heavily reuse the same gallium observations.",
                "A fixed sequence controls family-wise type-I error at 0.05 without assuming endpoint independence.",
                "It prevents a failed or blocked prerequisite from being bypassed by a later favorable result.",
            ],
            "limitations": [
                "Each endpoint still requires a valid preregistered test statistic and calibration before a p-value exists.",
                "Current missing frozen LSC objects and covariance/mapping blockers stop the sequence before evaluation.",
                "Secondary and sensitivity outputs cannot rescue a closed primary gate.",
            ],
        },
        "alternatives_considered_not_selected": [
            {
                "strategy": "HOLM_FAMILY_WISE_CONTROL",
                "validity": "Valid for a simultaneously available primary family under arbitrary dependence.",
                "reason_not_selected": "Less aligned with the scientific prerequisite order and requires all primary p-values before adjudication.",
            },
            {
                "strategy": "BENJAMINI_HOCHBERG_FALSE_DISCOVERY_RATE",
                "validity": "Potentially valid under an appropriate dependence contract.",
                "reason_not_selected": "Controls expected false discoveries rather than the stronger family-wise error needed for a confirmatory claim.",
            },
            {
                "strategy": "PRESPECIFIED_PRIMARY_WITH_DESCRIPTIVE_SECONDARIES",
                "validity": "Valid if a single endpoint is selected before results.",
                "reason_not_selected": "The frozen methodology contains several ordered generalization requirements, so a single endpoint would discard required gates.",
            },
        ],
        "prohibitions": [
            "No post-result reordering or strategy selection.",
            "No treating T1-T12 as independent.",
            "No confirmatory alpha for secondary or sensitivity-only tests.",
            "No global confirmation while any required primary gate is blocked or the LSC numerical bundle is missing.",
        ],
    }
