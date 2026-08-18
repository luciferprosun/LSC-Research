"""Structural tensor contract without a substituted historical tensor."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from numbers import Real
from typing import Sequence

from lsc_kernel.errors import FrozenOrientationMissing, FrozenTensorIncomplete


@dataclass(frozen=True, slots=True)
class TensorContract:
    symbol: str = "A_a^{ij}"
    expected_rank: int = 2
    dimension_size: int | None = None
    square: bool = True
    symmetric: bool = True
    traceless: bool = True
    orientation_required: bool = True
    frame_requirement: str = "COMPATIBLE_WITH_n_lab"
    frame_status: str = "MISSING_FROZEN_FRAME"
    provenance_source: str = "canonical-equations:E3-E4-E12"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)

    def validate_structure(self, value: object, *, tolerance: float = 1e-12) -> tuple[int, int]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
            raise FrozenTensorIncomplete("Active tensor must be a non-empty rank-2 array.")
        rows = list(value)
        if any(not isinstance(row, Sequence) or isinstance(row, (str, bytes)) for row in rows):
            raise FrozenTensorIncomplete("Active tensor must have rank exactly two.")
        matrix = [list(row) for row in rows]
        width = len(matrix[0])
        if width == 0 or any(len(row) != width for row in matrix):
            raise FrozenTensorIncomplete("Active tensor rows must have equal non-zero length.")
        if len(matrix) != width:
            raise FrozenTensorIncomplete("E4 requires a square tensor.")
        if self.dimension_size is not None and len(matrix) != self.dimension_size:
            raise FrozenTensorIncomplete(
                "Tensor dimension disagrees with the frozen contract.",
                details={"expected": self.dimension_size, "actual": len(matrix)},
            )
        if any(isinstance(item, bool) or not isinstance(item, Real) for row in matrix for item in row):
            raise FrozenTensorIncomplete("Tensor components must be real numerical scalars.")
        if self.symmetric:
            for i in range(len(matrix)):
                for j in range(i + 1, len(matrix)):
                    if abs(float(matrix[i][j]) - float(matrix[j][i])) > tolerance:
                        raise FrozenTensorIncomplete("E4 symmetry constraint is violated.")
        if self.traceless and abs(sum(float(matrix[i][i]) for i in range(len(matrix)))) > tolerance:
            raise FrozenTensorIncomplete("E4 tracelessness constraint is violated.")
        return (len(matrix), width)

    def require_orientation(self, orientation: object | None) -> None:
        if self.orientation_required and orientation is None:
            raise FrozenOrientationMissing(
                "The active tensor has no authentic frozen orientation.",
                details={"symbol": self.symbol},
            )
