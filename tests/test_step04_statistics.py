from __future__ import annotations

import json
import math
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

from kernel_helpers import ROOT

from lsc_kernel.cli.main import main as cli_main
from lsc_kernel.errors import FrozenModelRefitForbidden
from lsc_kernel.statistics.baselines import (
    assert_baseline_execution_authorized,
    constant_deficit_baseline,
    cross_section_registry_baselines,
    cross_section_variant_baseline,
    detector_systematic_baseline,
    experiment_normalization_baseline,
    hierarchical_experiment_baseline,
    null_baseline,
    sterile_3p1_baseline,
    sterile_survival_probability,
)
from lsc_kernel.statistics.chi_square import (
    diagonal_gaussian_chi_square,
    full_covariance_gaussian_chi_square,
    pull_term_chi_square,
)
from lsc_kernel.statistics.covariance import (
    PREREGISTERED_PLAUSIBLE_RHOS,
    CovarianceMatrix,
    SingularPolicy,
    build_covariance_scenario,
)
from lsc_kernel.statistics.controls import run_statistical_control_diagnostics
from lsc_kernel.statistics.cross_validation import (
    CrossValidationEngine,
    FoldFitResult,
    group_holdout_folds,
    leave_one_out_folds,
    transfer_fold,
)
from lsc_kernel.statistics.errors import (
    BaselineSpecificationIncomplete,
    CovarianceScenarioUnavailable,
    CovarianceValidationError,
    DataLeakageError,
    LSCStatisticalExecutionForbidden,
    MetricPrerequisiteError,
    SingularCovarianceError,
    StatisticalInputError,
)
from lsc_kernel.statistics.fixtures import run_analytical_fixtures, run_baseline_execution_controls
from lsc_kernel.statistics.execution import BaselineExecutionEngine
from lsc_kernel.statistics.likelihood import GaussianLikelihood
from lsc_kernel.statistics.metrics import cross_validation_score, information_criteria, predictive_log_likelihood
from lsc_kernel.statistics.model_comparison import compare_baselines
from lsc_kernel.statistics.multiple_testing import (
    PRIMARY_ORDER,
    fixed_sequence_decisions,
    multiple_testing_dependency_map,
)
from lsc_kernel.statistics.nuisance import NuisanceEngine, NuisanceKind, NuisanceParameter
from lsc_kernel.statistics.optimization import optimize_baseline
from lsc_kernel.statistics.reproduction import load_katrin_grid, reproduce_public_results
from lsc_kernel.statistics.result_schema import StatisticalExecutionManifest
from lsc_kernel.validation.external import assert_external_veto_authorized
from lsc_kernel.validation.external import load_and_validate_icecube_release_index
from lsc_kernel.validation.registries import GalliumCrossSectionModelRegistry, multiple_testing_policy
from lsc_kernel.errors import ExternalVetoBlockedMappingMissing
from tools.generate_step04_artifacts import generate as generate_step04_artifacts


class LikelihoodAndCovarianceTests(unittest.TestCase):
    def test_diagonal_and_correlated_analytic_values(self) -> None:
        diagonal = diagonal_gaussian_chi_square((1.0, 2.0), (0.0, 2.0), (0.5, 1.0))
        self.assertAlmostEqual(diagonal.raw_statistic, 4.0, places=12)
        likelihood = GaussianLikelihood(
            model_id="M0",
            execution_classification="NON_PHYSICAL_TEST_FIXTURE",
            observations=(1.0, 2.0),
            predictions=(0.0, 2.0),
            uncertainties=(0.5, 1.0),
        ).evaluate()
        self.assertEqual(likelihood, diagonal)
        correlated = full_covariance_gaussian_chi_square(
            (1.0, 1.0), (0.0, 0.0), CovarianceMatrix(((2.0, 1.0), (1.0, 2.0)))
        )
        self.assertAlmostEqual(correlated.raw_statistic, 2.0 / 3.0, places=12)
        self.assertAlmostEqual(pull_term_chi_square((1.0,), (0.0,), (2.0,)), 0.25, places=12)

    def test_formal_likelihood_interface_preserves_mask_and_counts(self) -> None:
        result = GaussianLikelihood(
            model_id="M0",
            execution_classification="NON_PHYSICAL_TEST_FIXTURE",
            observations=(1.0, 2.0, 4.0),
            predictions=(0.0, 2.0, 0.0),
            uncertainties=(0.5, 1.0, 2.0),
            mask=(True, False, True),
            n_fitted_parameters=1,
        ).evaluate()
        self.assertAlmostEqual(result.raw_statistic, 8.0, places=12)
        self.assertEqual(result.n_observations, 2)
        self.assertEqual(result.n_fitted_parameters, 1)
        self.assertEqual(result.dof_if_valid, 1)

    def test_malformed_likelihood_inputs_are_rejected(self) -> None:
        with self.assertRaises(StatisticalInputError):
            diagonal_gaussian_chi_square((1.0,), (1.0, 2.0), (1.0,))
        with self.assertRaises(StatisticalInputError):
            diagonal_gaussian_chi_square((1.0,), (1.0,), (0.0,))
        with self.assertRaises(CovarianceValidationError):
            CovarianceMatrix(((1.0, 2.0), (0.0, 1.0)))
        with self.assertRaises(CovarianceValidationError):
            CovarianceMatrix(((1.0, 2.0), (2.0, 1.0)))
        with self.assertRaises(CovarianceValidationError):
            CovarianceMatrix(((1.0,),), pseudo_inverse_rcond=2.0)

    def test_likelihood_boundary_rejects_frozen_lsc_model_identity(self) -> None:
        with self.assertRaises(LSCStatisticalExecutionForbidden):
            GaussianLikelihood(
                model_id="LSC",
                execution_classification="UNAUTHORIZED_LSC",
                observations=(1.0,),
                predictions=(1.0,),
                uncertainties=(1.0,),
            ).evaluate()

    def test_singular_policy_never_repairs_silently(self) -> None:
        rejected = CovarianceMatrix(((1.0, 1.0), (1.0, 1.0)), singular_policy=SingularPolicy.REJECT)
        with self.assertRaises(SingularCovarianceError):
            rejected.quadratic_form((1.0, 1.0))
        pseudo = CovarianceMatrix(
            ((1.0, 1.0), (1.0, 1.0)), singular_policy=SingularPolicy.PSEUDOINVERSE,
            pseudo_inverse_rcond=1e-11,
        )
        value, warnings = pseudo.quadratic_form((1.0, 1.0))
        self.assertAlmostEqual(value, 1.0, places=12)
        self.assertIn("PSEUDOINVERSE_USED:rcond=9.9999999999999994e-12", warnings)
        string_policy = CovarianceMatrix(((1.0, 1.0), (1.0, 1.0)), singular_policy="PSEUDOINVERSE")
        self.assertEqual(string_policy.diagnostics.inversion_strategy, "PSEUDOINVERSE")
        with self.assertRaises(CovarianceValidationError):
            CovarianceMatrix(((1.0,),), pseudo_inverse_rcond=0.0)

    def test_dimensions_and_covariance_scenarios_are_enforced(self) -> None:
        covariance = CovarianceMatrix(np.eye(2))
        with self.assertRaises(CovarianceValidationError):
            covariance.require_dimension(3)
        for rho in PREREGISTERED_PLAUSIBLE_RHOS:
            built = build_covariance_scenario(
                "COV_PLAUSIBLE_SCAN", statistical_sigmas=(1.0, 2.0), rho=rho
            )
            self.assertEqual(built.diagnostics.shape, (2, 2))
        with self.assertRaises(CovarianceValidationError):
            build_covariance_scenario("COV_PLAUSIBLE_SCAN", statistical_sigmas=(1.0, 2.0), rho=0.3)
        with self.assertRaises(CovarianceValidationError):
            build_covariance_scenario(
                "COV_UNCORRELATED_SYSTEMATICS",
                statistical_sigmas=(-1.0,),
                systematic_sigmas=(0.1,),
            )
        with self.assertRaises(CovarianceValidationError):
            build_covariance_scenario(
                "COV_FULLY_COMMON_SELECTED",
                statistical_sigmas=(1.0,),
                shared_sigmas=(-0.1,),
            )
        with self.assertRaises(CovarianceScenarioUnavailable):
            build_covariance_scenario("COV_COLLABORATION", statistical_sigmas=(1.0,))
        authenticated = build_covariance_scenario(
            "COV_COLLABORATION",
            statistical_sigmas=(1.0,),
            collaboration_matrix=((1.0,),),
            collaboration_authenticated=True,
            collaboration_source_sha256="c" * 64,
            collaboration_provenance_status="AUTHENTIC_SOURCE",
        )
        self.assertEqual(authenticated.diagnostics.shape, (1, 1))


class NuisanceAndOptimizationTests(unittest.TestCase):
    def test_shared_gaussian_nuisance_has_known_optimum(self) -> None:
        parameter = NuisanceParameter(
            "shared", NuisanceKind.SHARED, 0.0, None, None, 0.0, 1.0, (1.0,)
        )
        result = NuisanceEngine((parameter,)).profile(
            (2.0,), (1.0,), CovarianceMatrix(((1.0,),)), model_id="M4"
        )
        self.assertAlmostEqual(dict(result.values)["shared"], 0.5, places=7)
        self.assertAlmostEqual(result.evaluation.profiled_statistic, 0.5, places=12)
        self.assertTrue(result.evaluation.convergence)

    def test_fixed_and_experiment_specific_effects_are_explicit(self) -> None:
        fixed = NuisanceParameter(
            "fixed", NuisanceKind.FIXED, 0.0, None, None, None, None, (1.0, 0.0), fixed_value=0.2
        )
        experiment = NuisanceParameter(
            "experiment", NuisanceKind.EXPERIMENT_SPECIFIC, 0.0, -1.0, 1.0, 0.0, 1.0, (0.0, 1.0)
        )
        result = NuisanceEngine((fixed, experiment)).profile(
            (1.2, 1.5), (1.0, 1.0), CovarianceMatrix(np.eye(2)), model_id="M4"
        )
        self.assertAlmostEqual(dict(result.values)["fixed"], 0.2)
        self.assertEqual(result.evaluation.n_fitted_parameters, 1)

    def test_optimizer_is_deterministic_bounded_and_reports_contract(self) -> None:
        first = optimize_baseline(
            lambda values: float((values[0] - 0.25) ** 2),
            model_id="M1", initial_values=(0.9,), bounds=((0.0, 1.0),), tolerance=1e-12,
        )
        second = optimize_baseline(
            lambda values: float((values[0] - 0.25) ** 2),
            model_id="M1", initial_values=(0.9,), bounds=((0.0, 1.0),), tolerance=1e-12,
        )
        self.assertEqual(first, second)
        self.assertAlmostEqual(first.final_parameters[0], 0.25, places=7)
        self.assertTrue(first.convergence)
        self.assertGreater(first.number_of_evaluations, 0)

    def test_frozen_lsc_fit_is_rejected_at_optimizer_boundary(self) -> None:
        with self.assertRaises(FrozenModelRefitForbidden):
            optimize_baseline(
                lambda values: float(values[0] ** 2),
                model_id="M6", initial_values=(0.0,), bounds=((-1.0, 1.0),),
            )

    def test_optimizer_enforces_registry_fitting_allowed(self) -> None:
        for model_id in ("M0", "NOT_A_REGISTERED_MODEL"):
            with self.assertRaises(StatisticalInputError):
                optimize_baseline(
                    lambda values: float(values[0] ** 2),
                    model_id=model_id,
                    initial_values=(0.0,),
                    bounds=((-1.0, 1.0),),
                )

    def test_optimizer_rejects_invalid_tolerance_bounds_and_initial_values(self) -> None:
        for tolerance, initial, bounds in (
            (0.0, (0.0,), ((-1.0, 1.0),)),
            (1e-10, (0.0,), ((1.0, -1.0),)),
            (1e-10, (2.0,), ((-1.0, 1.0),)),
        ):
            with self.assertRaises(StatisticalInputError):
                optimize_baseline(
                    lambda values: float(values[0] ** 2),
                    model_id="M1",
                    initial_values=initial,
                    bounds=bounds,
                    tolerance=tolerance,
                )

    def test_correlated_and_bounded_nuisance_contracts(self) -> None:
        correlated = NuisanceParameter(
            "correlated", NuisanceKind.CORRELATED, 0.0, None, None, 0.0, None, (1.0,)
        )
        result = NuisanceEngine(
            (correlated,), correlated_prior_covariance=CovarianceMatrix(((1.0,),))
        ).profile((2.0,), (1.0,), CovarianceMatrix(((1.0,),)), model_id="M4")
        self.assertAlmostEqual(dict(result.values)["correlated"], 0.5, places=7)
        bounded = NuisanceParameter(
            "bounded", NuisanceKind.BOUNDED, 0.0, 0.0, 0.25, None, None, (1.0,)
        )
        bounded_result = NuisanceEngine((bounded,)).profile(
            (2.0,), (1.0,), CovarianceMatrix(((1.0,),)), model_id="M4"
        )
        self.assertAlmostEqual(dict(bounded_result.values)["bounded"], 0.25, places=7)
        with self.assertRaises(StatisticalInputError):
            NuisanceParameter("invalid", NuisanceKind.BOUNDED, 0.0, None, None, None, None, (1.0,))

    def test_correlated_and_independent_priors_are_profiled_separately(self) -> None:
        correlated = NuisanceParameter(
            "correlated", NuisanceKind.CORRELATED, 0.0, None, None, 0.0, None, (1.0, 0.0)
        )
        independent = NuisanceParameter(
            "independent", NuisanceKind.GAUSSIAN_PULL, 0.0, None, None, 0.0, 2.0, (0.0, 1.0)
        )
        result = NuisanceEngine(
            (correlated, independent),
            correlated_prior_covariance=CovarianceMatrix(((1.0,),)),
        ).profile((2.0, 3.0), (1.0, 1.0), CovarianceMatrix(np.eye(2)), model_id="M4")
        values = dict(result.values)
        self.assertAlmostEqual(values["correlated"], 0.5, places=7)
        self.assertAlmostEqual(values["independent"], 1.6, places=7)
        self.assertAlmostEqual(result.evaluation.profiled_statistic, 1.3, places=10)
        with self.assertRaises(StatisticalInputError):
            NuisanceEngine(
                (independent,),
                correlated_prior_covariance=CovarianceMatrix(((1.0,),)),
            )

    def test_correlated_prior_pseudoinverse_is_explicitly_reported(self) -> None:
        first = NuisanceParameter(
            "first", NuisanceKind.CORRELATED, 0.0, None, None, 0.0, None, (1.0, 0.0)
        )
        second = NuisanceParameter(
            "second", NuisanceKind.CORRELATED, 0.0, None, None, 0.0, None, (0.0, 1.0)
        )
        result = NuisanceEngine(
            (first, second),
            correlated_prior_covariance=CovarianceMatrix(
                ((1.0, 1.0), (1.0, 1.0)),
                singular_policy=SingularPolicy.PSEUDOINVERSE,
            ),
        ).profile((2.0, 2.0), (1.0, 1.0), CovarianceMatrix(np.eye(2)), model_id="M4")
        self.assertTrue(any(warning.startswith("PSEUDOINVERSE_USED") for warning in result.evaluation.warnings))


class BaselineModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.observed = np.asarray((0.8, 0.82, 0.79, 0.81))
        self.expected = np.ones(4)
        self.covariance = CovarianceMatrix(np.eye(4) * 0.01)

    def test_null_constant_cross_section_and_detector_models_execute(self) -> None:
        null = null_baseline(self.observed, self.expected, self.covariance)
        constant = constant_deficit_baseline(self.observed, self.expected, self.covariance)
        cross_section = cross_section_variant_baseline(
            self.observed, {"XS_A": np.full(4, 0.81), "XS_B": np.full(4, 0.9)},
            self.covariance, model_choice="XS_A",
        )
        profiled_cross_section = cross_section_variant_baseline(
            self.observed, {"XS_A": np.full(4, 1.0)}, self.covariance,
            model_choice="XS_A", profile_source_normalization=True,
        )
        detector = detector_systematic_baseline(
            self.observed, self.expected, self.covariance, np.full(4, 0.81)
        )
        self.assertGreater(null.evaluation.profiled_statistic, constant.evaluation.profiled_statistic)
        self.assertEqual(cross_section.model_id, "M2")
        self.assertIn("source_normalization", dict(profiled_cross_section.fitted_parameters))
        self.assertEqual(detector.model_id, "M4_DETECTOR_SYSTEMATIC")
        self.assertAlmostEqual(dict(constant.fitted_parameters)["normalization"], 0.805, places=7)

    def test_experiment_normalization_reports_parameter_growth(self) -> None:
        fitted = experiment_normalization_baseline(
            self.observed, self.expected, self.covariance, ("BEST", "BEST", "SAGE", "SAGE")
        )
        self.assertEqual(fitted.evaluation.n_fitted_parameters, 2)
        self.assertEqual(len(fitted.fitted_parameters), 2)

    def test_sterile_3p1_uses_only_explicit_geometry(self) -> None:
        baselines = np.asarray((1.0, 1.5, 2.0, 2.5))
        energies = np.full(4, 0.75)
        probabilities = sterile_survival_probability(
            baselines, energies, sin2_2theta_ee=0.2, delta_m2_ev2=1.0
        )
        fitted = sterile_3p1_baseline(
            probabilities, np.ones(4), CovarianceMatrix(np.eye(4) * 0.001), baselines, energies,
            initial=(0.15, 0.9),
        )
        self.assertTrue(fitted.evaluation.convergence)
        self.assertIn("NO_LSC_PARAMETERS", fitted.assumptions)
        with self.assertRaises(BaselineSpecificationIncomplete):
            sterile_3p1_baseline(
                self.observed, self.expected, self.covariance, (1.0,), (1.0,)
            )

    def test_hierarchical_model_stays_specification_incomplete(self) -> None:
        with self.assertRaises(BaselineSpecificationIncomplete):
            hierarchical_experiment_baseline()

    def test_lsc_models_cannot_enter_baseline_engine(self) -> None:
        for model in ("LSC", "LSC_6_3_0", "M5", "M6"):
            with self.assertRaises(FrozenModelRefitForbidden):
                assert_baseline_execution_authorized(model)

    def test_public_execution_boundary_always_emits_manifest_and_result(self) -> None:
        execution = BaselineExecutionEngine(ROOT).execute(
            model_id="M1",
            observed=self.observed,
            expected=self.expected,
            covariance=self.covariance,
            dataset_id="NON_PHYSICAL_TEST_FIXTURE",
            dataset_hash="b" * 64,
            split_id="FIXTURE_SPLIT",
            covariance_scenario="COV_DIAGONAL",
            timestamp="FIXED_TEST_TIMESTAMP",
            classification="NON_PHYSICAL_TEST_FIXTURE",
            likelihood_normalization_comparable=True,
        )
        manifest = execution.manifest.as_dict()
        self.assertFalse(manifest["LSC_used"])
        self.assertEqual(execution.result.execution_manifest_hash, manifest["execution_manifest_hash"])
        self.assertEqual(execution.result.model_id, "M1")
        self.assertTrue(execution.result.sensitivity_only)
        self.assertIsNotNone(execution.result.AIC_if_valid)
        self.assertIsNotNone(execution.result.BIC_if_valid)

    def test_public_execution_boundary_rejects_unregistered_split(self) -> None:
        with self.assertRaises(StatisticalInputError):
            BaselineExecutionEngine(ROOT).execute(
                model_id="M1",
                observed=self.observed,
                expected=self.expected,
                covariance=self.covariance,
                dataset_id="BEST",
                dataset_hash="b" * 64,
                split_id="POST_RESULT_SPLIT",
                covariance_scenario="COV_DIAGONAL",
                timestamp="FIXED_TEST_TIMESTAMP",
                classification="PUBLIC_DATA_BASELINE",
            )

    def test_cross_section_scan_uses_every_registered_isotope_model(self) -> None:
        registry = GalliumCrossSectionModelRegistry.from_repository(ROOT)
        eligible = tuple(model for model in registry.models if model.isotope == "51Cr")
        expectations = {
            model.model_id: np.full(4, model.total / eligible[0].total)
            for model in eligible
        }
        fits = cross_section_registry_baselines(
            self.observed,
            expectations,
            self.covariance,
            model_registry=registry,
            isotope="51Cr",
        )
        self.assertEqual(len(fits), len(eligible))
        executions = BaselineExecutionEngine(ROOT).execute_cross_section_scan(
            observed=self.observed,
            expected=self.expected,
            expectation_by_model=expectations,
            covariance=self.covariance,
            isotope="51Cr",
            dataset_id="NON_PHYSICAL_TEST_FIXTURE",
            dataset_hash="c" * 64,
            split_id="FIXTURE_XS_SCAN",
            covariance_scenario="COV_DIAGONAL",
            timestamp="FIXED_TEST_TIMESTAMP",
            classification="NON_PHYSICAL_TEST_FIXTURE",
        )
        self.assertEqual(len(executions), len(eligible))
        self.assertEqual(len({row.manifest.as_dict()["execution_manifest_hash"] for row in executions}), len(eligible))
        with self.assertRaises(StatisticalInputError):
            cross_section_registry_baselines(
                self.observed,
                dict(list(expectations.items())[:-1]),
                self.covariance,
                model_registry=registry,
                isotope="51Cr",
            )


class CrossValidationTests(unittest.TestCase):
    def test_leave_one_out_never_passes_holdout_to_fit_stage(self) -> None:
        observations = (1.0, 2.0, 3.0, 4.0)
        folds = leave_one_out_folds(4, split_id="FIXTURE_LOO", allow_non_physical_fixture=True)
        calls: list[tuple[int, ...]] = []

        def callback(training: np.ndarray, train: tuple[int, ...], holdout: tuple[int, ...]) -> FoldFitResult:
            calls.append(train)
            mean = float(np.mean(training))
            return FoldFitResult((("mean", mean),), tuple(mean for _ in holdout), train, "d" * 64)

        results = CrossValidationEngine().run(
            observations, folds, callback, execution_classification="NON_PHYSICAL_TEST_FIXTURE"
        )
        self.assertEqual(calls, [fold.training_indices for fold in folds])
        self.assertTrue(all(not set(row.training_observations) & set(row.holdout_observations) for row in results))

    def test_bad_fit_provenance_is_rejected_as_leakage(self) -> None:
        fold = leave_one_out_folds(3, split_id="FIXTURE_LOO", allow_non_physical_fixture=True)[0]

        def bad_callback(_: np.ndarray, train: tuple[int, ...], holdout: tuple[int, ...]) -> FoldFitResult:
            return FoldFitResult((), tuple(0.0 for _ in holdout), train + holdout, "d" * 64)

        with self.assertRaises(DataLeakageError):
            CrossValidationEngine().run(
                (1.0, 2.0, 3.0), (fold,), bad_callback,
                execution_classification="NON_PHYSICAL_TEST_FIXTURE",
            )

    def test_only_declared_group_and_transfer_splits_are_constructed(self) -> None:
        with self.assertRaises(StatisticalInputError):
            leave_one_out_folds(3, split_id="POST_RESULT_SPLIT")
        groups = ("BEST", "BEST", "GALLEX", "SAGE")
        loeo = group_holdout_folds(groups, split_id="SPLIT_LOEO_BEST")
        self.assertEqual(len(loeo), 3)
        transfer = transfer_fold(
            groups, split_id="SPLIT_BEST_TO_GALLEX", training_groups=("BEST",), holdout_groups=("GALLEX",)
        )
        transfer.validate(len(groups))
        self.assertEqual(transfer.training_indices, (0, 1))
        self.assertEqual(transfer.holdout_indices, (2,))
        with self.assertRaises(StatisticalInputError):
            group_holdout_folds(groups, split_id="INVALID_DUPLICATE_ORDER", ordered_groups=("BEST", "BEST", "GALLEX", "SAGE"))


class AdjudicationAndMetricTests(unittest.TestCase):
    def test_multiple_testing_policy_is_frozen_without_results(self) -> None:
        policy = multiple_testing_policy()
        self.assertEqual(policy["status"], "MULTIPLE_TESTING_POLICY_FROZEN")
        self.assertFalse(policy["result_information_used"])
        self.assertEqual(tuple(policy["primary_endpoint_policy"]["tests"]), PRIMARY_ORDER)
        self.assertTrue(multiple_testing_dependency_map()["selected_before_LSC_numerical_evaluation"])

    def test_fixed_sequence_stops_and_does_not_reorder(self) -> None:
        decisions = fixed_sequence_decisions({"T11": 0.01, "T7": 0.2, "T3": 0.001})
        self.assertEqual(decisions["T11"], "REJECT_LOCAL_NULL_CONTINUE")
        self.assertEqual(decisions["T7"], "DO_NOT_REJECT_STOP")
        self.assertEqual(decisions["T3"], "DESCRIPTIVE_AFTER_GATE_CLOSED")

    def test_information_metrics_check_prerequisites(self) -> None:
        result = information_criteria(
            minus_two_log_likelihood=10.0,
            n_parameters=2,
            n_observations=20,
            likelihood_normalization_comparable=True,
        )
        self.assertEqual(result.aic, 14.0)
        self.assertAlmostEqual(result.bic, 10.0 + 2.0 * math.log(20.0))
        with self.assertRaises(MetricPrerequisiteError):
            predictive_log_likelihood(1.0, normalized_likelihood_available=False)
        score = cross_validation_score((-1.0, -2.0, -3.0), expected_fold_count=3)
        self.assertEqual(score.total_predictive_log_likelihood, -6.0)
        self.assertEqual(score.mean_predictive_log_likelihood, -2.0)
        with self.assertRaises(MetricPrerequisiteError):
            cross_validation_score((-1.0, -2.0), expected_fold_count=3)

    def test_model_comparison_requires_equal_observation_contracts(self) -> None:
        engine = BaselineExecutionEngine(ROOT)
        shared = {
            "observed": (0.8, 0.8, 0.8),
            "expected": (1.0, 1.0, 1.0),
            "covariance": CovarianceMatrix(np.eye(3)),
            "dataset_id": "NON_PHYSICAL_TEST_FIXTURE",
            "dataset_hash": "e" * 64,
            "split_id": "FIXTURE_COMPARISON",
            "covariance_scenario": "COV_DIAGONAL",
            "timestamp": "FIXED_TEST_TIMESTAMP",
            "classification": "NON_PHYSICAL_TEST_FIXTURE",
        }
        candidate = engine.execute(model_id="M1", **shared).result
        reference = engine.execute(model_id="M0", **shared).result
        compare_baselines(candidate, reference, likelihood_normalization_comparable=False)
        with self.assertRaises(MetricPrerequisiteError):
            compare_baselines(
                replace(candidate, n_observations=candidate.n_observations + 1),
                reference,
                likelihood_normalization_comparable=False,
            )


class ReproductionAndHardGateTests(unittest.TestCase):
    def test_step04_artifacts_are_byte_deterministic(self) -> None:
        paths = generate_step04_artifacts(ROOT)
        before = {path: path.read_bytes() for path in paths}
        regenerated = generate_step04_artifacts(ROOT)
        self.assertEqual(paths, regenerated)
        self.assertEqual(before, {path: path.read_bytes() for path in regenerated})

    def test_analytical_fixtures_pass_without_lsc(self) -> None:
        result = run_analytical_fixtures()
        self.assertTrue(result["passed"])
        self.assertEqual(result["total_count"], 6)
        self.assertFalse(result["LSC_used"])

    def test_every_executable_baseline_uses_manifest_boundary(self) -> None:
        result = run_baseline_execution_controls(ROOT)
        self.assertTrue(result["passed"])
        self.assertEqual(result["execution_count"], 13)
        self.assertEqual(result["unique_manifest_count"], 13)
        self.assertTrue(result["all_manifests_declare_LSC_false"])
        self.assertEqual(result["hierarchical_baseline_status"], "SPECIFICATION_INCOMPLETE")
        self.assertEqual(result["frozen_LSC_baseline_status"], "FORBIDDEN_BEFORE_DISPATCH")

    def test_public_reproduction_passes_and_is_not_lsc_validation(self) -> None:
        result = reproduce_public_results(ROOT)
        self.assertTrue(result["passed"])
        self.assertEqual(result["passed_count"], 9)
        self.assertEqual(result["classification"], "PUBLIC_RESULT_REPRODUCTION_ONLY")
        self.assertEqual(result["six_gallium_diagonal"]["classification"], "SENSITIVITY_ONLY")
        self.assertFalse(result["LSC_used"])

    def test_katrin_grid_is_exact_50_by_50_and_not_interpolated(self) -> None:
        grid = load_katrin_grid(ROOT)
        self.assertEqual(grid.shape, (50, 50))
        self.assertAlmostEqual(grid.minimum()[0], 1374.7638148637948, places=10)
        self.assertFalse(grid.interpolation_authorized)
        with self.assertRaises(StatisticalInputError):
            grid.exact(-12345.0, -12345.0)

    def test_external_mapping_and_cli_lsc_validation_remain_blocked(self) -> None:
        with self.assertRaises(ExternalVetoBlockedMappingMissing):
            assert_external_veto_authorized("KATRIN")
        self.assertEqual(cli_main(("run-validation", "T3", "--model", "LSC")), 2)

    def test_icecube_release_and_numerical_objects_are_integrity_checked(self) -> None:
        result = load_and_validate_icecube_release_index(ROOT)
        self.assertEqual(result["file_records"], 52)
        self.assertEqual(result["numerical_objects_validated"], 8)
        self.assertTrue(result["all_indexed_files_exist"])
        self.assertTrue(result["all_indexed_sizes_match"])
        self.assertEqual(result["mapping_state"], "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING")

    def test_execution_manifest_is_deterministic_and_declares_lsc_false(self) -> None:
        kwargs = dict(
            repository_root=ROOT,
            dataset_hashes={"NON_PHYSICAL_TEST_FIXTURE": "a" * 64},
            model="M1",
            model_version="STEP04_BASELINE_1.0.0",
            parameters_fitted=("normalization",),
            nuisance_treatment="NONE",
            covariance_scenario="COV_DIAGONAL",
            split="FIXTURE_SPLIT",
            metric="CHI_SQUARE",
            optimizer="L-BFGS-B",
            classification="NON_PHYSICAL_TEST_FIXTURE",
            timestamp="FIXED_TEST_TIMESTAMP",
        )
        first = StatisticalExecutionManifest.build(**kwargs)
        second = StatisticalExecutionManifest.build(**kwargs)
        self.assertEqual(first, second)
        self.assertFalse(first.LSC_used)
        self.assertEqual(first.as_dict()["execution_manifest_hash"], second.as_dict()["execution_manifest_hash"])

    def test_generated_statistical_controls_have_expected_shapes(self) -> None:
        path = ROOT / "statistics/statistical_control_diagnostics.json"
        self.assertTrue(path.is_file())
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["passed"])
        self.assertEqual(result["MicroBooNE"]["diagnostics"]["shape"], [364, 364])
        self.assertTrue(all(
            row["diagnostics"]["shape"] == [990, 990]
            for row in result["PROSPECT"].values()
        ))
        self.assertTrue(result["STEREO"]["covariance_prompt_axis_matches_response_prompt_axis"])
        self.assertEqual(result["IceCube"]["numerical_objects_validated"], 8)

    def test_control_rank_counts_absolute_nonzero_spectrum(self) -> None:
        result = run_statistical_control_diagnostics(ROOT)
        prospect = result["PROSPECT"]
        self.assertEqual(prospect["StatisticalCovMatrix.txt"]["diagnostics"]["rank"], 990)
        self.assertEqual(prospect["StatisticalCovMatrix.txt"]["diagnostics"]["negative_eigenvalue_count"], 16)
        self.assertEqual(prospect["SystematicCovMatrix.txt"]["diagnostics"]["rank"], 990)
        self.assertTrue(prospect["BackgroundCovMatrix.txt"]["diagnostics"]["singular_within_tolerance"])

    def test_step04_golden_state(self) -> None:
        status = json.loads((ROOT / "frozen_core/manifests/kernel_status.json").read_text(encoding="utf-8"))
        for key in (
            "likelihood_engine_ready", "covariance_engine_ready", "nuisance_engine_ready",
            "baseline_engine_ready", "cross_validation_ready", "public_reproduction_ready",
            "statistical_controls_ready",
        ):
            self.assertTrue(status[key])
        self.assertFalse(status["numerical_model_ready"])
        self.assertFalse(status["prediction_authorized"])
        self.assertFalse(status["numerical_validation_authorized"])
        self.assertFalse(status["LSC_numerical_execution_authorized"])
        self.assertEqual(status["multiple_testing_policy_status"], "MULTIPLE_TESTING_POLICY_FROZEN")


if __name__ == "__main__":
    unittest.main()
