from __future__ import annotations

import unittest

from kernel_helpers import ROOT, bundle_mapping, parameter_entry

from lsc_kernel.errors import (
    FrozenParameterMissing,
    PostDataArtifactRejected,
    ValidationNotAuthorized,
)
from lsc_kernel.frozen.evaluator import FrozenLSCEvaluator
from lsc_kernel.frozen.identity import FrozenModelIdentity
from lsc_kernel.validation.contracts import T12Gate, validation_test_definitions
from lsc_kernel.validation.observations import ObservationSet
from lsc_kernel.validation.predictions import PredictionRequest


class EvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = FrozenLSCEvaluator.from_repository(ROOT)

    def request(self) -> PredictionRequest:
        return PredictionRequest(
            request_id="NON_PHYSICAL_TEST_FIXTURE",
            model_identity=FrozenModelIdentity.canonical().as_dict(),
            observations=ObservationSet("NON_PHYSICAL_TEST_FIXTURE", {}, {}, {}),
            requested_outputs=("authorization_check_only",),
        )

    def test_current_kernel_status_is_fail_closed(self) -> None:
        status = self.evaluator.status
        self.assertTrue(status.symbolic_model_ready)
        self.assertTrue(status.evaluator_available)
        self.assertFalse(status.numerical_model_ready)
        self.assertFalse(status.parameter_bundle_complete)
        self.assertFalse(status.unit_contract_complete)
        self.assertFalse(status.frame_contract_complete)
        self.assertFalse(status.tensor_contract_complete)
        self.assertFalse(status.prediction_authorized)
        self.assertFalse(status.validation_authorized)

    def test_incomplete_bundle_cannot_predict(self) -> None:
        with self.assertRaises(FrozenParameterMissing):
            self.evaluator.predict(self.request(), bundle_mapping({}))

    def test_post_data_bundle_cannot_predict(self) -> None:
        entries = {
            name: parameter_entry(
                artifact_id="postdata-toy-c0-c1",
                classification="HISTORICAL_POST_DATA",
                sha256="bea6a9a0e9878ec2aa97402b897edd2547f9597a66da2cef1b12e4ab84dbe780",
            )
            for name in self.evaluator.schema.required_names
        }
        with self.assertRaises(PostDataArtifactRejected):
            self.evaluator.predict(self.request(), bundle_mapping(entries))

    def test_can_predict_reports_concrete_blockers(self) -> None:
        allowed, blockers = self.evaluator.can_predict()
        self.assertFalse(allowed)
        self.assertIn("theta", blockers)
        self.assertIn("active_anisotropy_tensor", blockers)

    def test_golden_real_repository_state_passes_by_refusing_execution(self) -> None:
        status = self.evaluator.status
        golden = {
            "FROZEN_MODEL_IDENTITY": "VERIFIED",
            "E1_E12_SYMBOLIC_SPECIFICATION": "AVAILABLE" if status.symbolic_model_ready else "MISSING",
            "PARAMETER_CONTRACT": "AVAILABLE",
            "NUMERICAL_PARAMETER_BUNDLE": "INCOMPLETE" if not status.parameter_bundle_complete else "COMPLETE",
            "DIRECTIONAL_FRAME": "INCOMPLETE" if not status.frame_contract_complete else "COMPLETE",
            "ACTIVE_TENSOR": "INCOMPLETE" if not status.tensor_contract_complete else "COMPLETE",
            "NUMERICAL_LSC_PREDICTION": "BLOCKED" if not status.prediction_authorized else "AUTHORIZED",
            "VALIDATION_EXECUTION": "BLOCKED" if not status.validation_authorized else "AUTHORIZED",
            "REASON": "Missing authentic frozen numerical objects.",
        }
        self.assertEqual(golden["FROZEN_MODEL_IDENTITY"], "VERIFIED")
        self.assertEqual(golden["E1_E12_SYMBOLIC_SPECIFICATION"], "AVAILABLE")
        self.assertEqual(golden["NUMERICAL_PARAMETER_BUNDLE"], "INCOMPLETE")
        self.assertEqual(golden["NUMERICAL_LSC_PREDICTION"], "BLOCKED")
        self.assertEqual(golden["VALIDATION_EXECUTION"], "BLOCKED")


class ValidationContractTests(unittest.TestCase):
    def test_t1_t12_are_interfaces_only(self) -> None:
        definitions = validation_test_definitions()
        self.assertEqual([item.test_id for item in definitions], [f"T{i}" for i in range(1, 13)])
        self.assertTrue(all(not item.executable for item in definitions))
        self.assertEqual(definitions[-1].readiness.value, "BLOCKED")
        self.assertEqual(definitions[-1].canonical_name, "Directional and sidereal test")

    def test_missing_timing_blocks_t12(self) -> None:
        context = {
            "precise_timing": False,
            "surveyed_orientation": True,
            "sufficient_geometry": True,
            "complete_active_tensor": True,
            "required_reference_frames": True,
        }
        with self.assertRaises(ValidationNotAuthorized) as raised:
            T12Gate.assert_authorized(context)
        self.assertIn("precise_timing", raised.exception.details["blockers"])

    def test_missing_orientation_blocks_t12(self) -> None:
        context = {
            "precise_timing": True,
            "surveyed_orientation": False,
            "sufficient_geometry": True,
            "complete_active_tensor": True,
            "required_reference_frames": True,
        }
        with self.assertRaises(ValidationNotAuthorized) as raised:
            T12Gate.assert_authorized(context)
        self.assertIn("surveyed_orientation", raised.exception.details["blockers"])

    def test_exposure_midpoint_is_never_event_time_fallback(self) -> None:
        context = {flag: True for flag in (
            "precise_timing",
            "surveyed_orientation",
            "sufficient_geometry",
            "complete_active_tensor",
            "required_reference_frames",
            "required_units",
        )}
        context["timing_basis"] = "exposure_midpoint"
        with self.assertRaises(ValidationNotAuthorized) as raised:
            T12Gate.assert_authorized(context)
        self.assertIn("EXPOSURE_MIDPOINT_IS_NOT_EVENT_TIME", raised.exception.details["blockers"])

    def test_even_complete_metadata_does_not_invent_t12_specification(self) -> None:
        evaluator = FrozenLSCEvaluator.from_repository(ROOT)
        context = {flag: True for flag in (
            "precise_timing",
            "surveyed_orientation",
            "sufficient_geometry",
            "complete_active_tensor",
            "required_reference_frames",
            "required_units",
        )}
        with self.assertRaises(ValidationNotAuthorized) as raised:
            evaluator.authorize_validation("T12", context=context)
        self.assertEqual(raised.exception.details["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
