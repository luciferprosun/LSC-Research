"""Evidence-derived current status of the fail-closed kernel."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from lsc_kernel import __version__
from lsc_kernel.frozen.equations import equation_descriptors
from lsc_kernel.frozen.identity import FrozenModelIdentity
from lsc_kernel.frozen.parameter_schema import FrozenParameterSchema
from lsc_kernel.frozen.provenance import ProvenancePolicy
from lsc_kernel.validation.contracts import validation_test_definitions
from lsc_kernel.validation.datasets import canonical_dataset_registry
from lsc_kernel.validation.registries import (
    baseline_model_registry,
    covariance_scenario_registry,
    falsification_registry,
    nuisance_parameter_registry,
    multiple_testing_policy,
    split_registry,
)


@dataclass(frozen=True, slots=True)
class KernelStatus:
    kernel_version: str
    kernel_schema_version: str
    frozen_model_version: str
    frozen_commit: str
    symbolic_model_ready: bool
    numerical_model_ready: bool
    parameter_bundle_complete: bool
    unit_contract_complete: bool
    frame_contract_complete: bool
    tensor_contract_complete: bool
    evaluator_available: bool
    prediction_authorized: bool
    validation_authorized: bool
    dataset_contracts_ready: bool
    test_registry_ready: bool
    preregistration_ready: bool
    covariance_policy_ready: bool
    nuisance_policy_ready: bool
    baseline_registry_ready: bool
    split_policy_ready: bool
    falsification_policy_ready: bool
    execution_harness_ready: bool
    numerical_validation_authorized: bool
    likelihood_engine_ready: bool
    covariance_engine_ready: bool
    nuisance_engine_ready: bool
    baseline_engine_ready: bool
    cross_validation_ready: bool
    public_reproduction_ready: bool
    statistical_controls_ready: bool
    multiple_testing_policy_status: str
    LSC_numerical_execution_authorized: bool
    frozen_bundle_recovery_status: str
    frozen_bundle_complete: bool
    best_covariance_status: str
    sage_covariance_status: str
    gallex_covariance_status: str
    nuclear_covariance_status: str
    katrin_mapping_status: str
    icecube_mapping_status: str
    M3_geometry_status: str
    M4_hierarchical_status: str
    T12_data_status: str
    minimum_validation_unlock_set_complete: bool
    full_validation_unlock_set_complete: bool
    step05_execution_boundary_active: bool
    acquisition_verdict: str
    recoverability_decision_frozen: bool
    historical_6_3_0_preserved: bool
    publication_boundary_defined: bool
    successor_version_required: bool
    successor_version_candidate: str
    historical_validation_class: str
    prospective_validation_policy_ready: bool
    executable_successor_ready: bool
    publication_ready: bool
    publication_readiness_level: str
    step06_verdict: str
    blockers: tuple[str, ...]
    provenance_registry_hash: str
    verdict: str

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["blockers"] = list(self.blockers)
        return result


def build_kernel_status(
    provenance: ProvenancePolicy,
    *,
    schema: FrozenParameterSchema | None = None,
    identity: FrozenModelIdentity | None = None,
) -> KernelStatus:
    schema = schema or FrozenParameterSchema.canonical()
    identity = identity or FrozenModelIdentity.canonical()
    canonical_equations = provenance.admit_specification("canonical-equations")
    equations = equation_descriptors()
    symbolic_ready = (
        len(equations) == 12
        and {equation.equation_id for equation in equations} == {f"E{i}" for i in range(1, 13)}
        and canonical_equations.classification.value == "AUTHENTIC_FROZEN"
    )
    blockers = tuple(definition.canonical_name for definition in schema.numerical_blockers)
    units_complete = not any(
        definition.required_for_executable_evaluation and definition.unit_status == "MISSING_FROZEN_UNIT"
        for definition in schema.definitions
    )
    frames_complete = not any(
        definition.required_for_executable_evaluation and definition.frame_status == "MISSING_FROZEN_FRAME"
        for definition in schema.definitions
    )
    tensor_names = {"active_anisotropy_tensor", "tensor_orientation"}
    tensor_complete = not any(
        definition.canonical_name in tensor_names and definition.frozen_status != "AUTHENTIC_FROZEN"
        for definition in schema.definitions
    )
    test_definitions = validation_test_definitions()
    tests_complete = all(test.executable for test in test_definitions)
    dataset_contracts_ready = len(canonical_dataset_registry().records) == 13
    test_registry_ready = [test.test_id for test in test_definitions] == [f"T{i}" for i in range(1, 13)]
    covariance_policy_ready = len(covariance_scenario_registry()["scenarios"]) == 5
    nuisance_policy_ready = bool(nuisance_parameter_registry()["nuisances"])
    baseline_registry_ready = len(baseline_model_registry()["historical_models"]) == 7
    split_policy_ready = bool(split_registry()["splits"])
    falsification_policy_ready = bool(falsification_registry()["rules"])
    methodology_ready = all((
        dataset_contracts_ready,
        test_registry_ready,
        covariance_policy_ready,
        nuisance_policy_ready,
        baseline_registry_ready,
        split_policy_ready,
        falsification_policy_ready,
    ))
    numerical_ready = not blockers and units_complete and frames_complete and tensor_complete
    from lsc_kernel.statistics.baselines import constant_deficit_baseline
    from lsc_kernel.statistics.chi_square import diagonal_gaussian_chi_square
    from lsc_kernel.statistics.controls import run_statistical_control_diagnostics
    from lsc_kernel.statistics.covariance import CovarianceMatrix
    from lsc_kernel.statistics.cross_validation import CrossValidationEngine
    from lsc_kernel.statistics.nuisance import NuisanceEngine
    from lsc_kernel.statistics.reproduction import reproduce_public_results

    multiple_testing_status = str(multiple_testing_policy()["status"])
    return KernelStatus(
        kernel_version=__version__,
        kernel_schema_version=identity.kernel_schema_version,
        frozen_model_version=identity.canonical_version,
        frozen_commit=identity.historical_git_commit,
        symbolic_model_ready=symbolic_ready,
        numerical_model_ready=numerical_ready,
        parameter_bundle_complete=not blockers,
        unit_contract_complete=units_complete,
        frame_contract_complete=frames_complete,
        tensor_contract_complete=tensor_complete,
        evaluator_available=True,
        prediction_authorized=False,
        validation_authorized=False,
        dataset_contracts_ready=dataset_contracts_ready,
        test_registry_ready=test_registry_ready,
        preregistration_ready=methodology_ready,
        covariance_policy_ready=covariance_policy_ready,
        nuisance_policy_ready=nuisance_policy_ready,
        baseline_registry_ready=baseline_registry_ready,
        split_policy_ready=split_policy_ready,
        falsification_policy_ready=falsification_policy_ready,
        execution_harness_ready=methodology_ready,
        numerical_validation_authorized=False,
        likelihood_engine_ready=callable(diagonal_gaussian_chi_square),
        covariance_engine_ready=callable(CovarianceMatrix),
        nuisance_engine_ready=callable(NuisanceEngine),
        baseline_engine_ready=callable(constant_deficit_baseline),
        cross_validation_ready=callable(CrossValidationEngine),
        public_reproduction_ready=callable(reproduce_public_results),
        statistical_controls_ready=callable(run_statistical_control_diagnostics),
        multiple_testing_policy_status=multiple_testing_status,
        LSC_numerical_execution_authorized=False,
        frozen_bundle_recovery_status="AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE",
        frozen_bundle_complete=False,
        best_covariance_status="NOT_LOCATED_FULL_MATRIX_SUMMARY_PRESCRIPTION_ONLY",
        sage_covariance_status="NOT_LOCATED",
        gallex_covariance_status="NOT_LOCATED",
        nuclear_covariance_status="MARGINAL_ONLY",
        katrin_mapping_status="MAPPING_NOT_JUSTIFIED",
        icecube_mapping_status="MAPPING_NOT_JUSTIFIED",
        M3_geometry_status="PUBLISHED_AVERAGE_GEOMETRY",
        M4_hierarchical_status="SPECIFICATION_INCOMPLETE",
        T12_data_status="BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT",
        minimum_validation_unlock_set_complete=False,
        full_validation_unlock_set_complete=False,
        step05_execution_boundary_active=True,
        acquisition_verdict="BLOCKER_ADJUDICATION_COMPLETE_FROZEN_BUNDLE_STILL_MISSING",
        recoverability_decision_frozen=True,
        historical_6_3_0_preserved=True,
        publication_boundary_defined=True,
        successor_version_required=True,
        successor_version_candidate="6.3.1",
        historical_validation_class="RETROSPECTIVE_NON_BLIND",
        prospective_validation_policy_ready=True,
        executable_successor_ready=False,
        publication_ready=False,
        publication_readiness_level="P1_SPECIFICATION_BOUNDARY_READY",
        step06_verdict="LSC_6_3_0_NUMERICALLY_UNRECOVERABLE_SUCCESSOR_BOUNDARY_DEFINED",
        blockers=blockers,
        provenance_registry_hash=identity.provenance_registry_checksum,
        verdict=(
            "FROZEN_SPECIFICATION_KERNEL_READY_NUMERICAL_EXECUTION_BLOCKED"
            if symbolic_ready and not numerical_ready
            else "FROZEN_SPECIFICATION_KERNEL_STATUS_REQUIRES_REVIEW"
        ),
    )
