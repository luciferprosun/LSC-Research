"""Fail-closed unit contract."""

from __future__ import annotations

from dataclasses import dataclass

from lsc_kernel.errors import FrozenUnitUnknown


MISSING_FROZEN_UNIT = "MISSING_FROZEN_UNIT"


@dataclass(frozen=True, slots=True)
class UnitRequirement:
    field: str
    expected_unit: str
    status: str

    def validate(self, supplied_unit: str | None) -> None:
        if self.status == MISSING_FROZEN_UNIT:
            raise FrozenUnitUnknown(
                f"No authentic frozen unit is available for {self.field!r}.",
                details={"field": self.field, "status": self.status},
            )
        if self.status == "NOT_APPLICABLE":
            if supplied_unit not in (None, "NOT_APPLICABLE"):
                raise FrozenUnitUnknown(
                    f"Field {self.field!r} does not accept a unit.",
                    details={"field": self.field, "supplied_unit": supplied_unit},
                )
            return
        if supplied_unit != self.expected_unit:
            raise FrozenUnitUnknown(
                f"Unit mismatch for {self.field!r}.",
                details={"field": self.field, "expected": self.expected_unit, "actual": supplied_unit},
            )


KNOWN_OBSERVABLE_UNITS = {
    "R_a": "DIMENSIONLESS",
    "R_inner": "DIMENSIONLESS",
    "R_outer": "DIMENSIONLESS",
}
