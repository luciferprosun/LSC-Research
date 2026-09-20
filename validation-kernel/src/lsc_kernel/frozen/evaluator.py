"""Fail-closed evaluator boundary for the recovered historical specification."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from lsc_kernel.errors import (
    FrozenIdentityMismatch,
    PredictionNotAuthorized,
    ValidationNotAuthorized,
)
from lsc_kernel.frozen.equations import equation_descriptors, execute_algebraic_equation
from lsc_kernel.frozen.identity import FrozenModelIdentity, validate_identity
from lsc_kernel.frozen.kernel_status import KernelStatus, build_kernel_status
from lsc_kernel.frozen.parameter_bundle import FrozenParameterBundle, validate_parameter_bundle
from lsc_kernel.frozen.parameter_schema import FrozenParameterSchema
from lsc_kernel.frozen.provenance import ProvenancePolicy
from lsc_kernel.validation.contracts import T12Gate, validation_test_definitions
from lsc_kernel.validation.predictions import PredictionRequest, PredictionResult


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class FrozenLSCEvaluator:
    """Specification evaluator that refuses unauthorized numerical prediction."""

    def __init__(
        self,
        identity: FrozenModelIdentity,
        provenance: ProvenancePolicy,
        schema: FrozenParameterSchema | None = None,
    ) -> None:
        self.identity = validate_identity(identity)
        self.provenance = provenance
        self.schema = schema or FrozenParameterSchema.canonical()
        equations = self.provenance.admit_specification("canonical-equations")
        self.provenance.admit_specification("canonical-parameter-structures")
        source_manifest = self.provenance.admit_specification("derived-source-manifest")
        expected_equation_hash = self.identity.symbolic_equation_set_identity.rsplit(":", 1)[-1]
        if equations.sha256 != expected_equation_hash:
            raise FrozenIdentityMismatch("Equation registry object does not match the frozen identity.")
        if source_manifest.sha256 != self.identity.source_manifest_checksum:
            raise FrozenIdentityMismatch("Source manifest registry object does not match the frozen identity.")

    @classmethod
    def from_repository(cls, repository_root: Path | str) -> "FrozenLSCEvaluator":
        root = Path(repository_root)
        identity = FrozenModelIdentity.canonical()
        registry_path = root / "docs" / "provenance" / "FROZEN_PROVENANCE_REGISTRY.csv"
        if _sha256(registry_path) != identity.provenance_registry_checksum:
            raise FrozenIdentityMismatch(
                "The provenance registry checksum does not match the frozen identity.",
                details={"registry": "docs/provenance/FROZEN_PROVENANCE_REGISTRY.csv"},
            )
        return cls(identity, ProvenancePolicy.from_csv(registry_path))

    @property
    def status(self) -> KernelStatus:
        return build_kernel_status(self.provenance, schema=self.schema, identity=self.identity)

    @property
    def symbolic_equations(self) -> tuple[object, ...]:
        return equation_descriptors()

    def validate_bundle(self, bundle: FrozenParameterBundle | Mapping[str, Any]) -> FrozenParameterBundle:
        return validate_parameter_bundle(
            bundle,
            provenance=self.provenance,
            schema=self.schema,
            identity=self.identity,
        )

    def execute_equation(self, equation_id: str, **inputs: object) -> Any:
        """Execute only explicitly non-predictive algebraic pieces."""

        return execute_algebraic_equation(equation_id, **inputs)

    def can_predict(self) -> tuple[bool, tuple[str, ...]]:
        current = self.status
        return current.prediction_authorized, current.blockers

    def predict(
        self,
        request: PredictionRequest,
        bundle: FrozenParameterBundle | Mapping[str, Any],
    ) -> PredictionResult:
        validate_identity(request.model_identity, self.identity)
        self.validate_bundle(bundle)
        current = self.status
        if not current.prediction_authorized:
            raise PredictionNotAuthorized(
                "Numerical LSC prediction is blocked by missing authentic frozen numerical objects.",
                details={"blockers": list(current.blockers)},
            )
        raise PredictionNotAuthorized(
            "A complete full-model numerical execution implementation is not present in Step 02.",
            details={"blockers": ["complete_full_model_execution_path"]},
        )

    def authorize_validation(
        self,
        test_id: str,
        *,
        context: Mapping[str, Any],
        bundle: FrozenParameterBundle | Mapping[str, Any] | None = None,
    ) -> None:
        known = {definition.test_id: definition for definition in validation_test_definitions()}
        if test_id not in known:
            raise ValidationNotAuthorized(
                f"Unknown validation test ID {test_id!r}.",
                details={"test_id": test_id},
            )
        if test_id == "T12":
            T12Gate.assert_authorized(context)
        if bundle is not None:
            self.validate_bundle(bundle)
        definition = known[test_id]
        raise ValidationNotAuthorized(
            f"{test_id} numerical LSC validation is not authorized by the Step 03 planning layer.",
            details={"test_id": test_id, "status": definition.readiness.value},
        )
