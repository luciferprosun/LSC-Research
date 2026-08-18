from __future__ import annotations

import json
import unittest

from kernel_helpers import ROOT

from lsc_kernel.errors import ExternalVetoBlockedMappingMissing, FrozenModelRefitForbidden, ValidationNotAuthorized
from lsc_kernel.status import ValidationReadiness
from lsc_kernel.validation.best2 import BEST2FuturePredictionContract
from lsc_kernel.validation.contracts import T12Gate
from lsc_kernel.validation.datasets import canonical_dataset_registry
from lsc_kernel.validation.execution import DryRunValidationHarness
from lsc_kernel.validation.external import (
    assert_external_veto_authorized,
    load_and_validate_icecube_release_index,
    load_and_validate_katrin_grid,
)
from lsc_kernel.validation.policies import NoRefitPolicy, interpretation_allowed
from lsc_kernel.validation.registries import (
    GalliumCrossSectionModelRegistry,
    baseline_model_registry,
    covariance_scenario_registry,
    multiple_testing_policy,
    split_registry,
    validation_test_registry,
)


class DatasetContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = canonical_dataset_registry()

    def test_all_required_datasets_have_unique_contracts(self) -> None:
        expected = {
            "BEST", "GALLEX_GNO", "SAGE_CR51", "SAGE_AR37", "GALLIUM_CROSS_SECTIONS", "KATRIN",
            "ICECUBE", "BOREXINO", "DAYA_BAY", "PROSPECT", "STEREO", "MICROBOONE", "BEST2_FUTURE",
        }
        self.assertEqual(set(self.registry.by_id), expected)
        self.assertTrue(all(record.contract.dataset_id == record.dataset_id for record in self.registry.records))

    def test_all_pinned_source_hashes_are_immutable(self) -> None:
        self.assertEqual(self.registry.verify_source_hashes(ROOT), ())
        self.assertEqual(self.registry.verify_source_structures(ROOT), ())

    def test_mandated_row_counts_and_roles_are_preserved(self) -> None:
        by_id = self.registry.by_id
        self.assertEqual(by_id["BEST"].number_of_objects, 20)
        self.assertIn("1070", " ".join(by_id["BEST"].known_limitations))
        self.assertIn("1069", " ".join(by_id["BEST"].known_limitations))
        self.assertEqual(by_id["GALLEX_GNO"].number_of_objects, 83)
        self.assertEqual(by_id["SAGE_CR51"].number_of_objects, 12)
        self.assertEqual(by_id["SAGE_AR37"].number_of_objects, 11)
        self.assertEqual(by_id["BOREXINO"].validation_role, "METHODOLOGY_CONTROL")

    def test_best2_has_no_observations_and_is_future_blind(self) -> None:
        record = self.registry.by_id["BEST2_FUTURE"]
        self.assertEqual(record.number_of_objects, 0)
        self.assertEqual(record.blindness_level.value, "FUTURE_BLIND")
        self.assertEqual(BEST2FuturePredictionContract().prediction_values, ())


class RegistryTests(unittest.TestCase):
    def test_t1_t12_are_unique_and_use_exact_readiness_enum(self) -> None:
        tests = validation_test_registry()
        self.assertEqual([test.test_id for test in tests], [f"T{i}" for i in range(1, 13)])
        valid = {value.value for value in ValidationReadiness}
        self.assertTrue(all(test.readiness.value in valid for test in tests))
        self.assertTrue(all(test.blockers for test in tests))
        self.assertEqual(tests[-1].readiness, ValidationReadiness.BLOCKED)
        self.assertIn("PRECISE_TIMING_MISSING", tests[-1].blockers)

    def test_cross_section_registry_has_required_families_and_no_default(self) -> None:
        registry = GalliumCrossSectionModelRegistry.from_repository(ROOT).as_dict()
        names = {item["model_name"] for item in registry["models"]}
        self.assertIn("Bahcall", names)
        self.assertIn("Haxton", names)
        self.assertTrue(any("Kostensalo" in name for name in names))
        self.assertTrue(any("Elliott-Gavrin-Haxton" in name for name in names))
        self.assertIsNone(registry["default_model"])

    def test_historical_baseline_labels_and_aliases_are_preserved(self) -> None:
        registry = baseline_model_registry()
        self.assertEqual([model["model_id"] for model in registry["historical_models"]], [f"M{i}" for i in range(7)])
        self.assertEqual(registry["aliases"]["M_STERILE_3P1"], "M3")
        self.assertFalse(registry["historical_models"][5]["fitting_allowed"])
        self.assertFalse(registry["historical_models"][6]["fitting_allowed"])

    def test_covariance_sensitivity_cannot_be_called_significance(self) -> None:
        registry = covariance_scenario_registry()
        scenarios = {item["scenario_id"]: item for item in registry["scenarios"]}
        self.assertEqual(len(scenarios), 5)
        self.assertFalse(scenarios["COV_COLLABORATION"]["available"])
        for scenario_id in (
            "COV_DIAGONAL", "COV_UNCORRELATED_SYSTEMATICS", "COV_FULLY_COMMON_SELECTED", "COV_PLAUSIBLE_SCAN"
        ):
            self.assertEqual(scenarios[scenario_id]["provenance_status"], "ASSUMPTION_BASED_SENSITIVITY_ONLY")
            self.assertIn("discovery", scenarios[scenario_id]["forbidden_claims"])
        self.assertFalse(interpretation_allowed(sensitivity_only=True, requested_claim="5 sigma evidence"))

    def test_multiple_testing_is_frozen_before_lsc_evaluation(self) -> None:
        policy = multiple_testing_policy()
        self.assertEqual(policy["status"], "MULTIPLE_TESTING_POLICY_FROZEN")
        self.assertFalse(policy["result_information_used"])

    def test_splits_are_stable_and_historical_not_blind(self) -> None:
        registry = split_registry()
        ids = [item["split_id"] for item in registry["splits"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(not item["holdout_is_clean_unexposed"] for item in registry["splits"]))
        self.assertTrue(all(item["blindness_level"] == "NON_BLIND_HISTORICAL" for item in registry["splits"]))


class EnforcementAndHarnessTests(unittest.TestCase):
    def test_frozen_lsc_fit_is_rejected_but_baseline_fit_is_allowed(self) -> None:
        policy = NoRefitPolicy()
        with self.assertRaises(FrozenModelRefitForbidden):
            policy.authorize(operation="fit", target_model="M6", parameter_scope="FROZEN_LSC_PARAMETERS")
        self.assertTrue(policy.authorize(operation="fit", target_model="M3", parameter_scope="BASELINE_PARAMETERS"))
        self.assertTrue(policy.authorize(operation="profile", target_model="M6", parameter_scope="NUISANCE_ONLY"))

    def test_t12_remains_hard_blocked_and_midpoint_is_rejected(self) -> None:
        context = {
            "precise_timing": True,
            "surveyed_orientation": True,
            "sufficient_geometry": True,
            "complete_active_tensor": True,
            "required_reference_frames": True,
            "required_units": True,
            "timing_basis": "exposure_midpoint",
        }
        with self.assertRaises(ValidationNotAuthorized):
            T12Gate.assert_authorized(context)

    def test_external_veto_requires_explicit_mapping(self) -> None:
        for constraint_id in ("KATRIN", "ICECUBE"):
            with self.assertRaises(ExternalVetoBlockedMappingMissing):
                assert_external_veto_authorized(constraint_id)

    def test_external_public_packages_validate_without_running_veto(self) -> None:
        katrin = load_and_validate_katrin_grid(ROOT)
        icecube = load_and_validate_icecube_release_index(ROOT)
        self.assertEqual(katrin["shape"], [50, 50])
        self.assertEqual(katrin["grid_kind"], "ABSOLUTE_CHI_SQUARE")
        self.assertEqual(icecube["file_records"], 52)
        self.assertEqual(katrin["mapping_state"], "EXTERNAL_VETO_BLOCKED_MAPPING_MISSING")

    def test_execution_manifest_is_deterministic_and_fail_closed(self) -> None:
        harness = DryRunValidationHarness(ROOT)
        first = harness.plan("T3")
        second = harness.plan("T3")
        self.assertEqual(first, second)
        manifest = first["execution_manifest"]
        required = {
            "test_id", "model_identity", "model_hash", "dataset_hashes", "transformation_version", "split_id",
            "baseline_versions", "covariance_scenario", "nuisance_policy", "metric", "code_commit",
            "environment_hash", "timestamp", "authorization_state", "execution_manifest_hash",
        }
        self.assertTrue(required <= set(manifest))
        self.assertFalse(manifest["prediction_authorized"])
        self.assertFalse(manifest["numerical_validation_authorized"])
        self.assertFalse(first["LSC_prediction_performed"])
        self.assertFalse(first["validation_result_computed"])

    def test_preregistration_json_has_no_missing_required_package_files(self) -> None:
        required = {
            "PREREGISTRATION_MASTER.md", "tests.json", "datasets.json", "splits.json", "covariance_scenarios.json",
            "baseline_models.json", "nuisance_registry.json", "falsification_rules.json", "reporting_policy.md",
        }
        self.assertTrue(all((ROOT / "preregistration" / item).is_file() for item in required))
        alias = json.loads((ROOT / "preregistration/datasets.json").read_text(encoding="utf-8"))
        self.assertEqual(alias["$ref"], "validation_datasets.json")

    def test_golden_methodology_state_passes_by_remaining_blocked(self) -> None:
        status = json.loads((ROOT / "frozen_core/manifests/kernel_status.json").read_text(encoding="utf-8"))
        golden = {
            "FROZEN_MODEL_IDENTITY": "VERIFIED",
            "SYMBOLIC_KERNEL": "READY" if status["symbolic_model_ready"] else "MISSING",
            "VALIDATION_DATA_CONTRACTS": "READY" if status["dataset_contracts_ready"] else "MISSING",
            "TEST_REGISTRY": "READY" if status["test_registry_ready"] else "MISSING",
            "PREREGISTRATION_PACKAGE": "READY" if status["preregistration_ready"] else "MISSING",
            "COVARIANCE_SENSITIVITY_SCENARIOS": "READY" if status["covariance_policy_ready"] else "MISSING",
            "BASELINE_CONTRACTS": "READY" if status["baseline_registry_ready"] else "MISSING",
            "LSC_NUMERICAL_BUNDLE": "INCOMPLETE" if not status["numerical_model_ready"] else "COMPLETE",
            "LSC_PREDICTION": "BLOCKED" if not status["prediction_authorized"] else "AUTHORIZED",
            "LSC_VALIDATION_EXECUTION": "BLOCKED" if not status["numerical_validation_authorized"] else "AUTHORIZED",
            "T12": "BLOCKED",
            "BEST_2": "FUTURE_ONLY",
        }
        self.assertEqual(golden["SYMBOLIC_KERNEL"], "READY")
        self.assertEqual(golden["VALIDATION_DATA_CONTRACTS"], "READY")
        self.assertEqual(golden["TEST_REGISTRY"], "READY")
        self.assertEqual(golden["PREREGISTRATION_PACKAGE"], "READY")
        self.assertEqual(golden["LSC_NUMERICAL_BUNDLE"], "INCOMPLETE")
        self.assertEqual(golden["LSC_PREDICTION"], "BLOCKED")
        self.assertEqual(golden["LSC_VALIDATION_EXECUTION"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
