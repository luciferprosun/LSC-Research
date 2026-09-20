"""Predeclared cross-validation folds with a train/hold-out leakage guard."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Iterable, Sequence

import numpy as np
from numpy.typing import NDArray

from lsc_kernel.validation.registries import split_registry

from .errors import DataLeakageError, StatisticalInputError


def assert_split_authorized(split_id: str, *, allow_non_physical_fixture: bool = False) -> None:
    registered = {item["split_id"] for item in split_registry()["splits"]}
    if split_id in registered:
        return
    if allow_non_physical_fixture and split_id.startswith("FIXTURE_"):
        return
    raise StatisticalInputError(f"Split ID {split_id!r} is not in the frozen Step 03 split registry.")


@dataclass(frozen=True, slots=True)
class CrossValidationFold:
    split_id: str
    fold_id: str
    training_indices: tuple[int, ...]
    holdout_indices: tuple[int, ...]
    nuisance_refit_policy: str

    def validate(self, n_observations: int) -> None:
        training = set(self.training_indices)
        holdout = set(self.holdout_indices)
        if not training or not holdout or training & holdout:
            raise DataLeakageError("Training and hold-out sets must be non-empty and disjoint.")
        if any(index < 0 or index >= n_observations for index in training | holdout):
            raise DataLeakageError("Fold index is outside the observation vector.")

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FoldFitResult:
    fitted_parameters: tuple[tuple[str, float], ...]
    holdout_predictions: tuple[float, ...]
    fitted_on_indices: tuple[int, ...]
    execution_manifest_hash: str


@dataclass(frozen=True, slots=True)
class CrossValidationResult:
    execution_manifest_hash: str
    split_id: str
    fold_id: str
    training_observations: tuple[int, ...]
    holdout_observations: tuple[int, ...]
    fitted_parameters: tuple[tuple[str, float], ...]
    parameters_transferred_without_refit: tuple[str, ...]
    nuisance_refit_policy: str
    holdout_predictions: tuple[float, ...]


def leave_one_out_folds(
    n_observations: int,
    *,
    split_id: str,
    allow_non_physical_fixture: bool = False,
) -> tuple[CrossValidationFold, ...]:
    assert_split_authorized(split_id, allow_non_physical_fixture=allow_non_physical_fixture)
    if n_observations < 2:
        raise StatisticalInputError("Leave-one-out requires at least two observations.")
    all_indices = tuple(range(n_observations))
    return tuple(
        CrossValidationFold(
            split_id,
            f"{split_id}_FOLD_{held_out:03d}",
            tuple(index for index in all_indices if index != held_out),
            (held_out,),
            "TRAINING_FOLD_ONLY",
        )
        for held_out in all_indices
    )


def group_holdout_folds(
    group_ids: Sequence[str],
    *,
    split_id: str,
    ordered_groups: Sequence[str] | None = None,
    allow_non_physical_fixture: bool = False,
) -> tuple[CrossValidationFold, ...]:
    assert_split_authorized(split_id, allow_non_physical_fixture=allow_non_physical_fixture)
    groups = tuple(str(item) for item in group_ids)
    if len(groups) < 2:
        raise StatisticalInputError("Group hold-out requires at least two observations.")
    order = tuple(ordered_groups) if ordered_groups is not None else tuple(dict.fromkeys(groups))
    if set(order) != set(groups) or len(order) != len(set(order)):
        raise StatisticalInputError("Declared group order must contain each observed group exactly once.")
    folds = []
    for group in order:
        holdout = tuple(index for index, item in enumerate(groups) if item == group)
        training = tuple(index for index, item in enumerate(groups) if item != group)
        folds.append(
            CrossValidationFold(
                split_id,
                f"{split_id}_{group}",
                training,
                holdout,
                "TRAINING_FOLD_ONLY",
            )
        )
    return tuple(folds)


def transfer_fold(
    group_ids: Sequence[str],
    *,
    split_id: str,
    training_groups: Iterable[str],
    holdout_groups: Iterable[str],
    allow_non_physical_fixture: bool = False,
) -> CrossValidationFold:
    assert_split_authorized(split_id, allow_non_physical_fixture=allow_non_physical_fixture)
    groups = tuple(str(item) for item in group_ids)
    training_set = set(training_groups)
    holdout_set = set(holdout_groups)
    if training_set & holdout_set:
        raise DataLeakageError("Transfer training and hold-out group declarations overlap.")
    return CrossValidationFold(
        split_id,
        f"{split_id}_TRANSFER",
        tuple(index for index, item in enumerate(groups) if item in training_set),
        tuple(index for index, item in enumerate(groups) if item in holdout_set),
        "TRAINING_FOLD_ONLY",
    )


class CrossValidationEngine:
    """The callback receives training rows only and must return hold-out predictions."""

    def run(
        self,
        observations: Sequence[float],
        folds: Iterable[CrossValidationFold],
        fit_and_predict: Callable[[NDArray[np.float64], tuple[int, ...], tuple[int, ...]], FoldFitResult],
        *,
        execution_classification: str = "REGISTERED_VALIDATION",
    ) -> tuple[CrossValidationResult, ...]:
        values = np.asarray(observations, dtype=np.float64)
        if values.ndim != 1 or values.size < 2 or not np.isfinite(values).all():
            raise StatisticalInputError("Cross-validation observations must be a finite one-dimensional vector.")
        results = []
        for fold in folds:
            assert_split_authorized(
                fold.split_id,
                allow_non_physical_fixture=execution_classification == "NON_PHYSICAL_TEST_FIXTURE",
            )
            fold.validate(int(values.size))
            training_values = values[np.asarray(fold.training_indices)]
            outcome = fit_and_predict(training_values.copy(), fold.training_indices, fold.holdout_indices)
            if tuple(outcome.fitted_on_indices) != tuple(fold.training_indices):
                raise DataLeakageError("Fit provenance does not exactly match the declared training indices.")
            if len(outcome.holdout_predictions) != len(fold.holdout_indices):
                raise StatisticalInputError("Hold-out prediction count does not match the fold contract.")
            if (
                len(outcome.execution_manifest_hash) != 64
                or any(character not in "0123456789abcdef" for character in outcome.execution_manifest_hash.lower())
            ):
                raise StatisticalInputError("Every cross-validation fold fit requires a StatisticalExecutionManifest hash.")
            results.append(
                CrossValidationResult(
                    execution_manifest_hash=outcome.execution_manifest_hash,
                    split_id=fold.split_id,
                    fold_id=fold.fold_id,
                    training_observations=fold.training_indices,
                    holdout_observations=fold.holdout_indices,
                    fitted_parameters=outcome.fitted_parameters,
                    parameters_transferred_without_refit=tuple(name for name, _ in outcome.fitted_parameters),
                    nuisance_refit_policy=fold.nuisance_refit_policy,
                    holdout_predictions=outcome.holdout_predictions,
                )
            )
        return tuple(results)
