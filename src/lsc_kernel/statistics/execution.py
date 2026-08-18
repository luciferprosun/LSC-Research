"""Manifest-producing execution boundary for independent baseline models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from numpy.typing import ArrayLike

from .baselines import (
    BaselineFit,
    assert_baseline_execution_authorized,
    constant_deficit_baseline,
    cross_section_registry_baselines,
    cross_section_variant_baseline,
    detector_systematic_baseline,
    experiment_normalization_baseline,
    hierarchical_experiment_baseline,
    null_baseline,
    sterile_3p1_baseline,
)
from .covariance import CovarianceMatrix
from .cross_validation import assert_split_authorized
from .errors import StatisticalInputError
from .metrics import information_criteria
from .result_schema import BaselineResult, StatisticalExecutionManifest
from lsc_kernel.validation.registries import GalliumCrossSectionModelRegistry


ASSUMPTION_BASED_COVARIANCE = frozenset({
    "COV_DIAGONAL",
    "COV_UNCORRELATED_SYSTEMATICS",
    "COV_FULLY_COMMON_SELECTED",
    "COV_PLAUSIBLE_SCAN",
})


@dataclass(frozen=True, slots=True)
class ManifestedBaselineExecution:
    manifest: StatisticalExecutionManifest
    result: BaselineResult
    prediction: tuple[float, ...]


class BaselineExecutionEngine:
    """Every public baseline execution produces a bound manifest and result."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def _dispatch(
        self,
        model_id: str,
        observed: ArrayLike,
        expected: ArrayLike,
        covariance: CovarianceMatrix,
        options: Mapping[str, Any],
    ) -> BaselineFit:
        if model_id == "M0":
            return null_baseline(observed, expected, covariance)
        if model_id == "M1":
            return constant_deficit_baseline(observed, expected, covariance)
        if model_id == "M2":
            required = {"expectation_by_model", "model_choice"}
            if not required <= set(options):
                raise StatisticalInputError("M2 requires expectation_by_model and model_choice.")
            return cross_section_variant_baseline(
                observed,
                options["expectation_by_model"],
                covariance,
                model_choice=str(options["model_choice"]),
                profile_source_normalization=bool(options.get("profile_source_normalization", False)),
                model_registry=GalliumCrossSectionModelRegistry.from_repository(self.repository_root),
            )
        if model_id == "M3":
            if "baselines_m" not in options or "energies_mev" not in options:
                raise StatisticalInputError("M3 requires explicit baselines_m and energies_mev.")
            return sterile_3p1_baseline(
                observed,
                expected,
                covariance,
                options["baselines_m"],
                options["energies_mev"],
                initial=tuple(options.get("initial", (0.1, 1.0))),
                bounds=tuple(options.get("bounds", ((0.0, 1.0), (0.0, 100.0)))),
            )
        if model_id == "M4_EXPERIMENT_NORMALIZATION":
            if "experiment_ids" not in options:
                raise StatisticalInputError("Experiment-normalization model requires experiment_ids.")
            return experiment_normalization_baseline(
                observed, expected, covariance, options["experiment_ids"]
            )
        if model_id == "M4_DETECTOR_SYSTEMATIC":
            if "detector_response" not in options:
                raise StatisticalInputError("Detector-systematic model requires detector_response.")
            return detector_systematic_baseline(
                observed, expected, covariance, options["detector_response"]
            )
        if model_id == "M4_HIERARCHICAL_EXPERIMENT":
            return hierarchical_experiment_baseline()
        raise StatisticalInputError(f"No Step 04 baseline dispatcher exists for {model_id!r}.")

    def execute(
        self,
        *,
        model_id: str,
        observed: ArrayLike,
        expected: ArrayLike,
        covariance: CovarianceMatrix,
        dataset_id: str,
        dataset_hash: str,
        split_id: str,
        covariance_scenario: str,
        timestamp: str,
        classification: str,
        nuisance_treatment: str = "NONE",
        likelihood_normalization_comparable: bool = False,
        options: Mapping[str, Any] | None = None,
        code_commit: str | None = None,
    ) -> ManifestedBaselineExecution:
        assert_split_authorized(
            split_id,
            allow_non_physical_fixture=classification == "NON_PHYSICAL_TEST_FIXTURE",
        )
        canonical = assert_baseline_execution_authorized(model_id)
        fit = self._dispatch(canonical, observed, expected, covariance, options or {})
        parameter_names = tuple(name for name, _ in fit.fitted_parameters)
        optimizer_name = fit.optimization.optimizer if fit.optimization is not None else "NONE"
        variant = str((options or {}).get("model_choice", "")) if canonical == "M2" else ""
        model_version = "STEP04_BASELINE_1.0.0" + (f":{variant}" if variant else "")
        manifest = StatisticalExecutionManifest.build(
            repository_root=self.repository_root,
            dataset_hashes={dataset_id: dataset_hash},
            model=fit.model_id,
            model_version=model_version,
            parameters_fitted=parameter_names,
            nuisance_treatment=nuisance_treatment,
            covariance_scenario=covariance_scenario,
            split=split_id,
            metric=fit.evaluation.statistic_type,
            optimizer=optimizer_name,
            classification=classification,
            timestamp=timestamp,
            code_commit=code_commit,
        )
        information = None
        if likelihood_normalization_comparable and fit.evaluation.n_fitted_parameters < fit.evaluation.n_observations:
            information = information_criteria(
                minus_two_log_likelihood=fit.evaluation.profiled_statistic,
                n_parameters=fit.evaluation.n_fitted_parameters,
                n_observations=fit.evaluation.n_observations,
                likelihood_normalization_comparable=True,
            )
        manifest_hash = str(manifest.as_dict()["execution_manifest_hash"])
        result = BaselineResult(
            execution_manifest_hash=manifest_hash,
            model_id=fit.model_id,
            dataset_id=dataset_id,
            split_id=split_id,
            statistic=fit.evaluation.profiled_statistic,
            statistic_type=fit.evaluation.statistic_type,
            fitted_parameters=fit.fitted_parameters,
            nuisance_parameters=fit.evaluation.nuisance_values,
            n_observations=fit.evaluation.n_observations,
            n_parameters=fit.evaluation.n_fitted_parameters,
            dof_if_valid=fit.evaluation.dof_if_valid,
            AIC_if_valid=(information.aic if information else None),
            BIC_if_valid=(information.bic if information else None),
            predictive_score_if_valid=None,
            covariance_scenario=covariance_scenario,
            sensitivity_only=covariance_scenario in ASSUMPTION_BASED_COVARIANCE,
            convergence=fit.evaluation.convergence,
            warnings=fit.evaluation.warnings,
        )
        return ManifestedBaselineExecution(manifest, result, fit.prediction)

    def execute_cross_section_scan(
        self,
        *,
        observed: ArrayLike,
        expected: ArrayLike,
        expectation_by_model: Mapping[str, ArrayLike],
        covariance: CovarianceMatrix,
        isotope: str,
        dataset_id: str,
        dataset_hash: str,
        split_id: str,
        covariance_scenario: str,
        timestamp: str,
        classification: str,
        nuisance_treatment: str = "NONE",
        profile_source_normalization: bool = False,
        code_commit: str | None = None,
    ) -> tuple[ManifestedBaselineExecution, ...]:
        """Manifest the complete registered isotope scan; partial scans fail closed."""
        registry = GalliumCrossSectionModelRegistry.from_repository(self.repository_root)
        # Validate completeness before creating any partial result.
        fits = cross_section_registry_baselines(
            observed,
            expectation_by_model,
            covariance,
            model_registry=registry,
            isotope=isotope,
            profile_source_normalization=profile_source_normalization,
        )
        model_choices = tuple(
            assumption.split("=", 1)[1]
            for fit in fits
            for assumption in fit.assumptions
            if assumption.startswith("CROSS_SECTION_MODEL=")
        )
        return tuple(
            self.execute(
                model_id="M2",
                observed=observed,
                expected=expected,
                covariance=covariance,
                dataset_id=dataset_id,
                dataset_hash=dataset_hash,
                split_id=split_id,
                covariance_scenario=covariance_scenario,
                timestamp=timestamp,
                classification=classification,
                nuisance_treatment=nuisance_treatment,
                options={
                    "expectation_by_model": expectation_by_model,
                    "model_choice": model_choice,
                    "profile_source_normalization": profile_source_normalization,
                },
                code_commit=code_commit,
            )
            for model_choice in model_choices
        )
