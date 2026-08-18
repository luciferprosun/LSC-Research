"""Analytical NON_PHYSICAL_TEST_FIXTURE controls for the statistical engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from .baselines import constant_deficit_baseline, null_baseline
from .baselines import sterile_survival_probability
from .chi_square import diagonal_gaussian_chi_square, full_covariance_gaussian_chi_square
from .covariance import CovarianceMatrix, SingularPolicy
from .cross_validation import CrossValidationEngine, FoldFitResult, leave_one_out_folds
from .errors import SingularCovarianceError
from .nuisance import NuisanceEngine, NuisanceKind, NuisanceParameter
from .execution import BaselineExecutionEngine, ManifestedBaselineExecution
from .result_schema import canonical_json_hash
from lsc_kernel.validation.registries import GalliumCrossSectionModelRegistry


@dataclass(frozen=True, slots=True)
class FixtureResult:
    fixture_id: str
    expected: object
    observed: object
    tolerance: float
    passed: bool
    classification: str = "NON_PHYSICAL_TEST_FIXTURE"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def run_analytical_fixtures() -> dict[str, object]:
    results: list[FixtureResult] = []

    diagonal = diagonal_gaussian_chi_square((1.0, 2.0), (0.0, 2.0), (0.5, 1.0))
    results.append(FixtureResult("FIXTURE_DIAGONAL_GAUSSIAN", 4.0, diagonal.raw_statistic, 1e-12,
                                 abs(diagonal.raw_statistic - 4.0) <= 1e-12))

    correlated_covariance = CovarianceMatrix(((2.0, 1.0), (1.0, 2.0)))
    correlated = full_covariance_gaussian_chi_square((1.0, 1.0), (0.0, 0.0), correlated_covariance)
    results.append(FixtureResult("FIXTURE_CORRELATED_GAUSSIAN", 2.0 / 3.0, correlated.raw_statistic, 1e-12,
                                 abs(correlated.raw_statistic - 2.0 / 3.0) <= 1e-12))

    nuisance = NuisanceEngine((
        NuisanceParameter(
            "shared_offset",
            NuisanceKind.SHARED,
            initial=0.0,
            lower_bound=None,
            upper_bound=None,
            prior_mean=0.0,
            prior_sigma=1.0,
            effect=(1.0,),
        ),
    )).profile((2.0,), (1.0,), CovarianceMatrix(((1.0,),)), model_id="M4")
    nuisance_observed = {
        "parameter": dict(nuisance.values)["shared_offset"],
        "profiled_chi_square": nuisance.evaluation.profiled_statistic,
    }
    nuisance_expected = {"parameter": 0.5, "profiled_chi_square": 0.5}
    results.append(FixtureResult(
        "FIXTURE_SHARED_NUISANCE",
        nuisance_expected,
        nuisance_observed,
        1e-7,
        abs(nuisance_observed["parameter"] - 0.5) <= 1e-7
        and abs(nuisance_observed["profiled_chi_square"] - 0.5) <= 1e-7,
    ))

    singular_rejected = False
    singular = CovarianceMatrix(((1.0, 1.0), (1.0, 1.0)), singular_policy=SingularPolicy.REJECT)
    try:
        singular.quadratic_form((1.0, 1.0))
    except SingularCovarianceError:
        singular_rejected = True
    pseudo = CovarianceMatrix(((1.0, 1.0), (1.0, 1.0)), singular_policy=SingularPolicy.PSEUDOINVERSE)
    pseudo_value, pseudo_warnings = pseudo.quadratic_form((1.0, 1.0))
    singular_observed = {
        "reject_policy_rejected": singular_rejected,
        "pseudoinverse_value": pseudo_value,
        "pseudoinverse_reported": any(item.startswith("PSEUDOINVERSE_USED") for item in pseudo_warnings),
    }
    singular_expected = {
        "reject_policy_rejected": True,
        "pseudoinverse_value": 1.0,
        "pseudoinverse_reported": True,
    }
    results.append(FixtureResult(
        "FIXTURE_SINGULAR_COVARIANCE",
        singular_expected,
        singular_observed,
        1e-12,
        singular_rejected and abs(pseudo_value - 1.0) <= 1e-12 and singular_observed["pseudoinverse_reported"],
    ))

    folds = leave_one_out_folds(4, split_id="FIXTURE_LOO", allow_non_physical_fixture=True)
    seen_fit_inputs: list[tuple[int, ...]] = []

    def fit_predict(training: np.ndarray, train_indices: tuple[int, ...], holdout_indices: tuple[int, ...]) -> FoldFitResult:
        seen_fit_inputs.append(train_indices)
        mean = float(np.mean(training))
        return FoldFitResult(
            (("training_mean", mean),), tuple(mean for _ in holdout_indices), train_indices, "d" * 64
        )

    cv = CrossValidationEngine().run(
        (1.0, 2.0, 3.0, 4.0),
        folds,
        fit_predict,
        execution_classification="NON_PHYSICAL_TEST_FIXTURE",
    )
    leakage_free = all(
        not set(item.training_observations) & set(item.holdout_observations)
        for item in cv
    ) and tuple(seen_fit_inputs) == tuple(fold.training_indices for fold in folds)
    results.append(FixtureResult("FIXTURE_CROSS_VALIDATION", True, leakage_free, 0.0, leakage_free))

    covariance = CovarianceMatrix(np.eye(3))
    null = null_baseline((0.8, 0.8, 0.8), (1.0, 1.0, 1.0), covariance)
    constant = constant_deficit_baseline((0.8, 0.8, 0.8), (1.0, 1.0, 1.0), covariance)
    ranking = constant.evaluation.profiled_statistic < null.evaluation.profiled_statistic
    results.append(FixtureResult(
        "FIXTURE_MODEL_SELECTION",
        "M1_BEATS_M0",
        "M1_BEATS_M0" if ranking else "UNEXPECTED_RANKING",
        1e-10,
        ranking and abs(dict(constant.fitted_parameters)["normalization"] - 0.8) <= 1e-7,
    ))

    return {
        "schema_version": "1.0.0",
        "classification": "NON_PHYSICAL_TEST_FIXTURE",
        "LSC_used": False,
        "fixtures": [item.as_dict() for item in results],
        "passed": all(item.passed for item in results),
        "passed_count": sum(item.passed for item in results),
        "total_count": len(results),
    }


def run_baseline_execution_controls(root: Path) -> dict[str, object]:
    """Exercise each executable baseline through the manifest-producing boundary."""
    observed = np.asarray((0.80, 0.82, 0.79, 0.81), dtype=np.float64)
    expected = np.ones(4, dtype=np.float64)
    covariance = CovarianceMatrix(np.eye(4, dtype=np.float64) * 0.01)
    dataset_description = {
        "classification": "NON_PHYSICAL_TEST_FIXTURE",
        "observed": observed.tolist(),
        "expected": expected.tolist(),
        "covariance": covariance.values.tolist(),
    }
    dataset_hash = canonical_json_hash(dataset_description)
    engine = BaselineExecutionEngine(root)
    shared = {
        "observed": observed,
        "expected": expected,
        "covariance": covariance,
        "dataset_id": "FIXTURE_BASELINE_EXECUTION",
        "dataset_hash": dataset_hash,
        "split_id": "FIXTURE_FULL_SAMPLE",
        "covariance_scenario": "COV_DIAGONAL",
        "timestamp": "STEP04_DETERMINISTIC_BASELINE_FIXTURE_NO_WALL_CLOCK",
        "classification": "NON_PHYSICAL_TEST_FIXTURE",
        "code_commit": "4553c25205c1c2fcb13c2c97c3a0d1af724a78fe",
    }
    executions: list[ManifestedBaselineExecution] = [
        engine.execute(model_id="M0", **shared),
        engine.execute(model_id="M1", **shared),
    ]

    registry = GalliumCrossSectionModelRegistry.from_repository(root)
    isotope_models = tuple(model for model in registry.models if model.isotope == "51Cr")
    reference_total = isotope_models[0].total
    expectations = {
        model.model_id: np.full(4, model.total / reference_total, dtype=np.float64)
        for model in isotope_models
    }
    executions.extend(
        engine.execute_cross_section_scan(
            expectation_by_model=expectations,
            isotope="51Cr",
            **shared,
        )
    )

    baselines = np.asarray((1.0, 1.5, 2.0, 2.5), dtype=np.float64)
    energies = np.full(4, 0.75, dtype=np.float64)
    sterile_observed = sterile_survival_probability(
        baselines,
        energies,
        sin2_2theta_ee=0.2,
        delta_m2_ev2=1.0,
    )
    executions.append(
        engine.execute(
            model_id="M3",
            **{**shared, "observed": sterile_observed},
            options={"baselines_m": baselines, "energies_mev": energies, "initial": (0.15, 0.9)},
        )
    )
    executions.append(
        engine.execute(
            model_id="M_EXPERIMENT_NORMALIZATION",
            **shared,
            options={"experiment_ids": ("BEST", "BEST", "SAGE", "SAGE")},
        )
    )
    executions.append(
        engine.execute(
            model_id="M_DETECTOR_SYSTEMATIC",
            **shared,
            options={"detector_response": np.full(4, 0.81, dtype=np.float64)},
        )
    )

    rows = [
        {
            "manifest": execution.manifest.as_dict(),
            "result": execution.result.as_dict(),
            "prediction": list(execution.prediction),
        }
        for execution in executions
    ]
    manifests = [row["manifest"] for row in rows]
    return {
        "schema_version": "1.0.0",
        "classification": "NON_PHYSICAL_TEST_FIXTURE",
        "LSC_used": False,
        "dataset_description": dataset_description,
        "dataset_hash": dataset_hash,
        "executions": rows,
        "execution_count": len(rows),
        "unique_manifest_count": len({row["execution_manifest_hash"] for row in manifests}),
        "all_converged": all(bool(row["result"]["convergence"]) for row in rows),
        "all_manifests_declare_LSC_false": all(row["LSC_used"] is False for row in manifests),
        "cross_section_models_executed": [model.model_id for model in isotope_models],
        "hierarchical_baseline_status": "SPECIFICATION_INCOMPLETE",
        "frozen_LSC_baseline_status": "FORBIDDEN_BEFORE_DISPATCH",
        "passed": (
            len(rows) == 13
            and len({row["execution_manifest_hash"] for row in manifests}) == len(rows)
            and all(bool(row["result"]["convergence"]) for row in rows)
            and all(row["LSC_used"] is False for row in manifests)
        ),
    }
