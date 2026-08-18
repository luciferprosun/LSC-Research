"""Validated covariance matrices and preregistered scenario construction."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .errors import CovarianceScenarioUnavailable, CovarianceValidationError, SingularCovarianceError


class SingularPolicy(StrEnum):
    REJECT = "REJECT"
    PSEUDOINVERSE = "PSEUDOINVERSE"


PREREGISTERED_PLAUSIBLE_RHOS = (0.0, 0.25, 0.50, 0.75, 0.90)


@dataclass(frozen=True, slots=True)
class CovarianceDiagnostics:
    shape: tuple[int, int]
    symmetric: bool
    finite: bool
    positive_semidefinite: bool
    minimum_eigenvalue: float
    maximum_eigenvalue: float
    rank: int
    condition_number: float
    singular: bool
    symmetry_tolerance: float
    psd_tolerance: float
    rank_tolerance: float
    inversion_strategy: str
    pseudo_inverse_rcond: float | None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CovarianceMatrix:
    """Immutable validated covariance with no implicit repair path."""

    def __init__(
        self,
        values: ArrayLike,
        *,
        symmetry_tolerance: float = 1e-12,
        psd_tolerance: float = 1e-12,
        rank_tolerance: float | None = None,
        singular_policy: SingularPolicy | str = SingularPolicy.REJECT,
        pseudo_inverse_rcond: float = 1e-12,
    ) -> None:
        try:
            resolved_policy = SingularPolicy(singular_policy)
        except ValueError as error:
            raise CovarianceValidationError(f"Unknown singular covariance policy {singular_policy!r}.") from error
        tolerances = (symmetry_tolerance, psd_tolerance, pseudo_inverse_rcond)
        if any(not np.isfinite(float(value)) or float(value) <= 0 for value in tolerances):
            raise CovarianceValidationError("Covariance tolerances and pseudoinverse rcond must be finite and positive.")
        if pseudo_inverse_rcond > 1:
            raise CovarianceValidationError("Pseudo-inverse rcond must not exceed 1.")
        if rank_tolerance is not None and (not np.isfinite(float(rank_tolerance)) or rank_tolerance <= 0):
            raise CovarianceValidationError("Explicit covariance rank tolerance must be finite and positive.")
        matrix = np.asarray(values, dtype=np.float64)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
            raise CovarianceValidationError("Covariance must be a non-empty square matrix.")
        if not np.isfinite(matrix).all():
            raise CovarianceValidationError("Covariance contains non-finite values.")
        if not np.allclose(matrix, matrix.T, rtol=0.0, atol=symmetry_tolerance):
            raise CovarianceValidationError("Covariance is not symmetric within the declared tolerance.")
        eigenvalues = np.linalg.eigvalsh(matrix)
        eigen_scale = max(float(np.max(np.abs(eigenvalues))), np.finfo(np.float64).tiny)
        if float(eigenvalues[0]) < -psd_tolerance * eigen_scale:
            raise CovarianceValidationError("Covariance is not positive semidefinite within tolerance.")
        resolved_rank_tolerance = (
            float(rank_tolerance)
            if rank_tolerance is not None
            else float(max(matrix.shape) * np.finfo(np.float64).eps * eigen_scale)
        )
        rank = int(np.linalg.matrix_rank(matrix, tol=resolved_rank_tolerance))
        singular = rank < matrix.shape[0]
        if singular and resolved_policy is SingularPolicy.REJECT:
            inversion_strategy = "REJECT_SINGULAR"
            condition = float("inf")
        else:
            inversion_strategy = "PSEUDOINVERSE" if singular else "DIRECT_SOLVE"
            condition = float(np.linalg.cond(matrix))
        copy = matrix.copy()
        copy.setflags(write=False)
        self._matrix = copy
        self._diagnostics = CovarianceDiagnostics(
            shape=(int(matrix.shape[0]), int(matrix.shape[1])),
            symmetric=True,
            finite=True,
            positive_semidefinite=True,
            minimum_eigenvalue=float(eigenvalues[0]),
            maximum_eigenvalue=float(eigenvalues[-1]),
            rank=rank,
            condition_number=condition,
            singular=singular,
            symmetry_tolerance=float(symmetry_tolerance),
            psd_tolerance=float(psd_tolerance),
            rank_tolerance=resolved_rank_tolerance,
            inversion_strategy=inversion_strategy,
            pseudo_inverse_rcond=(float(pseudo_inverse_rcond) if resolved_policy is SingularPolicy.PSEUDOINVERSE else None),
        )
        self.singular_policy = resolved_policy
        self.pseudo_inverse_rcond = float(pseudo_inverse_rcond)

    @property
    def values(self) -> NDArray[np.float64]:
        return self._matrix

    @property
    def diagnostics(self) -> CovarianceDiagnostics:
        return self._diagnostics

    def require_dimension(self, dimension: int) -> None:
        if self._matrix.shape != (dimension, dimension):
            raise CovarianceValidationError(
                f"Covariance dimension {self._matrix.shape} does not match observations ({dimension})."
            )

    def solve(self, residual: ArrayLike) -> tuple[NDArray[np.float64], tuple[str, ...]]:
        vector = np.asarray(residual, dtype=np.float64)
        if vector.ndim != 1:
            raise CovarianceValidationError("Residual must be one-dimensional.")
        self.require_dimension(int(vector.size))
        if not np.isfinite(vector).all():
            raise CovarianceValidationError("Residual contains non-finite values.")
        if self._diagnostics.singular:
            if self.singular_policy is SingularPolicy.REJECT:
                raise SingularCovarianceError("Singular covariance rejected by explicit policy.")
            inverse = np.linalg.pinv(self._matrix, rcond=self.pseudo_inverse_rcond, hermitian=True)
            return inverse @ vector, (
                f"PSEUDOINVERSE_USED:rcond={self.pseudo_inverse_rcond:.17g}",
                f"RANK={self._diagnostics.rank}/{self._matrix.shape[0]}",
            )
        return np.linalg.solve(self._matrix, vector), ()

    def quadratic_form(self, residual: ArrayLike) -> tuple[float, tuple[str, ...]]:
        vector = np.asarray(residual, dtype=np.float64)
        weighted, warnings = self.solve(vector)
        value = float(vector @ weighted)
        if value < -self._diagnostics.psd_tolerance:
            raise CovarianceValidationError("Quadratic form is negative beyond tolerance.")
        return max(0.0, value), warnings


def diagonal_covariance(sigmas: Sequence[float]) -> NDArray[np.float64]:
    values = np.asarray(sigmas, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all() or np.any(values <= 0):
        raise CovarianceValidationError("Sigmas must be a non-empty finite positive vector.")
    return np.diag(values**2)


def equicorrelation_covariance(sigmas: Sequence[float], rho: float) -> NDArray[np.float64]:
    values = np.asarray(sigmas, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or np.any(values <= 0) or not np.isfinite(values).all():
        raise CovarianceValidationError("Sigmas must be finite and positive.")
    lower = -1.0 / (values.size - 1) if values.size > 1 else -1.0
    if not lower < rho < 1.0:
        raise CovarianceValidationError(f"rho must satisfy {lower} < rho < 1 for this dimension.")
    correlation = np.full((values.size, values.size), float(rho), dtype=np.float64)
    np.fill_diagonal(correlation, 1.0)
    return np.outer(values, values) * correlation


def build_covariance_scenario(
    scenario_id: str,
    *,
    statistical_sigmas: Sequence[float],
    systematic_sigmas: Sequence[float] | None = None,
    shared_sigmas: Sequence[float] | None = None,
    rho: float | None = None,
    collaboration_matrix: ArrayLike | None = None,
    collaboration_authenticated: bool = False,
    collaboration_source_sha256: str | None = None,
    collaboration_provenance_status: str | None = None,
    singular_policy: SingularPolicy = SingularPolicy.REJECT,
) -> CovarianceMatrix:
    stat = np.asarray(statistical_sigmas, dtype=np.float64)
    if stat.ndim != 1 or stat.size == 0 or not np.isfinite(stat).all() or np.any(stat <= 0):
        raise CovarianceValidationError("Statistical sigmas must be a non-empty finite positive vector.")
    if scenario_id == "COV_DIAGONAL":
        values = diagonal_covariance(stat)
    elif scenario_id == "COV_UNCORRELATED_SYSTEMATICS":
        if systematic_sigmas is None:
            raise CovarianceValidationError("Systematic sigmas are required for this scenario.")
        sys = np.asarray(systematic_sigmas, dtype=np.float64)
        if sys.shape != stat.shape or not np.isfinite(sys).all() or np.any(sys < 0):
            raise CovarianceValidationError(
                "Systematic sigmas must be finite, non-negative, and match statistical dimensions."
            )
        values = np.diag(stat**2 + sys**2)
    elif scenario_id == "COV_FULLY_COMMON_SELECTED":
        if shared_sigmas is None:
            raise CovarianceValidationError("Selected shared sigmas are required for this scenario.")
        shared = np.asarray(shared_sigmas, dtype=np.float64)
        if shared.shape != stat.shape or not np.isfinite(shared).all() or np.any(shared < 0):
            raise CovarianceValidationError(
                "Shared sigmas must be finite, non-negative, and match statistical dimensions."
            )
        values = np.diag(stat**2) + np.outer(shared, shared)
    elif scenario_id == "COV_PLAUSIBLE_SCAN":
        if rho is None or float(rho) not in PREREGISTERED_PLAUSIBLE_RHOS:
            raise CovarianceValidationError(
                f"rho must be one of the preregistered values {PREREGISTERED_PLAUSIBLE_RHOS}."
            )
        values = equicorrelation_covariance(stat, float(rho))
    elif scenario_id == "COV_COLLABORATION":
        source_hash_valid = (
            isinstance(collaboration_source_sha256, str)
            and len(collaboration_source_sha256) == 64
            and all(character in "0123456789abcdef" for character in collaboration_source_sha256.lower())
        )
        if (
            collaboration_matrix is None
            or not collaboration_authenticated
            or not source_hash_valid
            or collaboration_provenance_status != "AUTHENTIC_SOURCE"
        ):
            raise CovarianceScenarioUnavailable(
                "COV_COLLABORATION requires an authenticated collaboration matrix, SHA-256, and AUTHENTIC_SOURCE provenance."
            )
        values = np.asarray(collaboration_matrix, dtype=np.float64)
    else:
        raise CovarianceValidationError(f"Unknown covariance scenario {scenario_id!r}.")
    return CovarianceMatrix(values, singular_policy=singular_policy)
