from __future__ import annotations

import unittest

from kernel_helpers import (
    FIXTURE_SHA256,
    bundle_mapping,
    fixture_policy,
    parameter_entry,
    repository_policy,
    single_parameter_schema,
)

from lsc_kernel.errors import (
    FrozenFrameUnknown,
    FrozenIdentityMismatch,
    FrozenOrientationMissing,
    FrozenParameterMissing,
    FrozenTensorIncomplete,
    FrozenUnitUnknown,
    MalformedBundle,
)
from lsc_kernel.frozen.identity import FrozenModelIdentity
from lsc_kernel.frozen.parameter_bundle import validate_parameter_bundle
from lsc_kernel.frozen.parameter_schema import FrozenParameterSchema
from lsc_kernel.frozen.tensor import TensorContract


class ParameterSchemaTests(unittest.TestCase):
    def test_schema_contains_all_required_recovery_blockers(self) -> None:
        names = set(FrozenParameterSchema.canonical().required_names)
        required = {
            "theta",
            "parameter_ordering",
            "lambda0",
            "lambdaA",
            "f0_a",
            "fA_a",
            "active_anisotropy_tensor",
            "tensor_orientation",
            "complete_reference_frame",
            "numerical_configuration",
            "parameter_bounds",
            "numerical_defaults",
            "frozen_prediction_table",
            "executable_evaluator_inputs",
        }
        self.assertTrue(required <= names)

    def test_schema_does_not_embed_numerical_values(self) -> None:
        for definition in FrozenParameterSchema.canonical().definitions:
            self.assertNotIn("numerical_value", definition.as_dict())
            self.assertEqual(definition.frozen_status, "MISSING")

    def test_missing_required_parameters_are_detected(self) -> None:
        bundle = bundle_mapping({})
        with self.assertRaises(FrozenParameterMissing):
            validate_parameter_bundle(bundle, provenance=repository_policy())

    def test_wrong_identity_is_rejected_before_parameter_use(self) -> None:
        identity = FrozenModelIdentity.canonical().as_dict()
        identity["historical_git_commit"] = "f" * 40
        bundle = bundle_mapping({}, identity=identity)
        with self.assertRaises(FrozenIdentityMismatch):
            validate_parameter_bundle(bundle, provenance=repository_policy())

    def test_bundle_hash_mismatch_is_rejected(self) -> None:
        bundle = bundle_mapping({})
        bundle["bundle_sha256"] = "0" * 64
        with self.assertRaises(MalformedBundle):
            validate_parameter_bundle(bundle, provenance=repository_policy())

    def test_non_authentic_bundle_state_is_rejected(self) -> None:
        bundle = bundle_mapping({})
        bundle["provenance_state"] = "UNVERIFIED"
        from lsc_kernel.frozen.parameter_bundle import compute_bundle_hash

        bundle["bundle_sha256"] = compute_bundle_hash(bundle)
        with self.assertRaises(MalformedBundle):
            validate_parameter_bundle(bundle, provenance=repository_policy())

    def test_unknown_critical_parameter_is_rejected(self) -> None:
        schema = single_parameter_schema()
        bundle = bundle_mapping(
            {
                "lambda0": parameter_entry(),
                "unexpected_critical": parameter_entry(),
            }
        )
        with self.assertRaises(MalformedBundle):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)

    def test_valid_software_contract_fixture_is_accepted(self) -> None:
        schema = single_parameter_schema()
        bundle = bundle_mapping({"lambda0": parameter_entry()})
        validated = validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)
        self.assertEqual(validated.parameters["lambda0"]["value"], 1.0)

    def test_parameter_source_must_be_listed_in_source_references(self) -> None:
        schema = single_parameter_schema()
        bundle = bundle_mapping({"lambda0": parameter_entry()})
        bundle["source_references"] = ["different-source"]
        from lsc_kernel.frozen.parameter_bundle import compute_bundle_hash

        bundle["bundle_sha256"] = compute_bundle_hash(bundle)
        with self.assertRaises(MalformedBundle):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)

    def test_incorrect_dimensions_are_rejected(self) -> None:
        schema = single_parameter_schema()
        bundle = bundle_mapping({"lambda0": parameter_entry(value=[1.0], dimensions=[1])})
        with self.assertRaises(FrozenTensorIncomplete):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)

    def test_unknown_required_unit_is_rejected(self) -> None:
        schema = single_parameter_schema(unit_status="MISSING_FROZEN_UNIT", units="UNKNOWN")
        bundle = bundle_mapping({"lambda0": parameter_entry()})
        with self.assertRaises(FrozenUnitUnknown):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)

    def test_unknown_required_frame_is_rejected(self) -> None:
        schema = single_parameter_schema(
            frame_status="MISSING_FROZEN_FRAME",
            frame="UNKNOWN",
        )
        bundle = bundle_mapping({"lambda0": parameter_entry()})
        with self.assertRaises(FrozenFrameUnknown):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)

    def test_wrong_artifact_hash_is_rejected(self) -> None:
        schema = single_parameter_schema()
        bundle = bundle_mapping({"lambda0": parameter_entry(sha256="b" * 64)})
        from lsc_kernel.errors import FrozenParameterProvenanceError

        with self.assertRaises(FrozenParameterProvenanceError):
            validate_parameter_bundle(bundle, provenance=fixture_policy(), schema=schema)


class TensorContractTests(unittest.TestCase):
    def test_symmetric_traceless_fixture_passes_structural_check(self) -> None:
        shape = TensorContract().validate_structure([[1.0, 0.0], [0.0, -1.0]])
        self.assertEqual(shape, (2, 2))

    def test_malformed_tensor_is_rejected(self) -> None:
        for value in (
            [[1.0, 0.0], [1.0]],
            [[1.0, 2.0], [0.0, -1.0]],
            [[1.0, 0.0], [0.0, 1.0]],
        ):
            with self.subTest(value=value), self.assertRaises(FrozenTensorIncomplete):
                TensorContract().validate_structure(value)

    def test_missing_orientation_is_explicit(self) -> None:
        with self.assertRaises(FrozenOrientationMissing):
            TensorContract().require_orientation(None)


if __name__ == "__main__":
    unittest.main()
