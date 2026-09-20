"""Technical safeguards for no-refit and interpretation boundaries."""

from __future__ import annotations

from dataclasses import dataclass

from lsc_kernel.errors import FrozenModelRefitForbidden


FROZEN_LSC_MODEL_IDS = frozenset({"LSC", "LSC_6_3_0", "M5", "M6"})


@dataclass(frozen=True, slots=True)
class NoRefitPolicy:
    policy_version: str = "1.0.0"

    def authorize(self, *, operation: str, target_model: str, parameter_scope: str) -> bool:
        operation_key = operation.upper()
        target_key = target_model.upper()
        scope_key = parameter_scope.upper()
        if target_key in FROZEN_LSC_MODEL_IDS and operation_key in {"FIT", "REFIT", "OPTIMIZE", "CALIBRATE"}:
            raise FrozenModelRefitForbidden(
                "Frozen LSC parameters may not be fitted, refitted, optimized, or calibrated.",
                details={"operation": operation_key, "target_model": target_key, "parameter_scope": scope_key},
            )
        if target_key in FROZEN_LSC_MODEL_IDS and operation_key == "PROFILE" and "FROZEN_LSC" in scope_key:
            raise FrozenModelRefitForbidden(
                "Nuisance profiling may not change a frozen LSC parameter.",
                details={"operation": operation_key, "target_model": target_key, "parameter_scope": scope_key},
            )
        return True

    def as_dict(self) -> dict[str, object]:
        return {
            "policy_version": self.policy_version,
            "frozen_lsc_operations_forbidden": ["FIT", "REFIT", "OPTIMIZE", "CALIBRATE"],
            "baseline_fitting_allowed": True,
            "nuisance_profiling_allowed": True,
            "constraint": "Baseline fitting and nuisance profiling may occur only in preregistered scopes and never alter frozen LSC parameters.",
            "error": "FrozenModelRefitForbidden",
        }


ASSUMPTION_ONLY_FORBIDDEN_TERMS = (
    "discovery",
    "exclusion",
    "sigma evidence",
    "decisive preference",
)


def interpretation_allowed(*, sensitivity_only: bool, requested_claim: str) -> bool:
    if not sensitivity_only:
        return True
    lowered = requested_claim.casefold()
    return not any(term in lowered for term in ASSUMPTION_ONLY_FORBIDDEN_TERMS)
