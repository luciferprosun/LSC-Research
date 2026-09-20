"""Auditable machine representation of the authentic symbolic E1-E12 set."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from numbers import Real
from typing import Any, Callable

from lsc_kernel.errors import FrozenEquationBlocked
from lsc_kernel.frozen.tensor import TensorContract
from lsc_kernel.status import EquationReadiness


SOURCE_DOCUMENT = "01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_ACTIVE_EQUATION_SET.md"
SOURCE_ARTIFACT = "canonical-equations"


@dataclass(frozen=True, slots=True)
class EquationDescriptor:
    equation_id: str
    canonical_symbolic_representation: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    dependencies: tuple[str, ...]
    units_constraints: tuple[str, ...]
    frame_constraints: tuple[str, ...]
    source_document: str
    source_location: str
    provenance_artifact_id: str
    provenance_status: str
    implementation_function: str
    implementation_scope: str
    execution_readiness: EquationReadiness
    blockers: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["execution_readiness"] = self.execution_readiness.value
        return result


def _equation(
    equation_id: str,
    symbolic: str,
    inputs: tuple[str, ...],
    outputs: tuple[str, ...],
    dependencies: tuple[str, ...],
    units: tuple[str, ...],
    frames: tuple[str, ...],
    readiness: EquationReadiness,
    blockers: tuple[str, ...],
    implementation: str = "blocked_symbolic_equation",
    scope: str = "SYMBOLIC_DESCRIPTOR_ONLY",
) -> EquationDescriptor:
    return EquationDescriptor(
        equation_id=equation_id,
        canonical_symbolic_representation=symbolic,
        inputs=inputs,
        outputs=outputs,
        dependencies=dependencies,
        units_constraints=units,
        frame_constraints=frames,
        source_document=SOURCE_DOCUMENT,
        source_location=f"Canonical Equations / {equation_id}",
        provenance_artifact_id=SOURCE_ARTIFACT,
        provenance_status="AUTHENTIC_FROZEN",
        implementation_function=f"lsc_kernel.frozen.equations:{implementation}",
        implementation_scope=scope,
        execution_readiness=readiness,
        blockers=blockers,
    )


def equation_descriptors() -> tuple[EquationDescriptor, ...]:
    """Return E1-E12 in canonical numeric-ID order."""

    return (
        _equation(
            "E1",
            "N0_a = integral dE dOmega dt [Phi(E,t,Omega) P_alpha_beta(E,L) sigma(E) epsilon0_a(E,t,Omega) W_a(E,t,Omega)]",
            ("Phi", "P_alpha_beta", "sigma", "epsilon0_a", "W_a", "integration_domain"),
            ("N0_a",),
            (),
            ("Complete integrand and integration-unit contract is not frozen.",),
            ("Omega and geometry conventions are not completely frozen.",),
            EquationReadiness.BLOCKED_MISSING_NUMERICAL_CONTRACT,
            ("missing-numerical-defaults", "missing-e1-e12-evaluator"),
        ),
        _equation(
            "E2",
            "epsilon_LSC,a(E,t,Omega) = epsilon0_a(E,t,Omega) * [1 + lambda0*f0_a(E,t) + lambdaA*q_a(t,Omega)*fA_a(E,t)]",
            ("epsilon0_a", "lambda0", "f0_a", "lambdaA", "q_a", "fA_a"),
            ("epsilon_LSC_a",),
            ("E3",),
            ("The bracket must be compatible with a dimensionless multiplier; individual normalizations are not frozen.",),
            ("q_a and the active tensor require a compatible lab-frame contract.",),
            EquationReadiness.BLOCKED_MISSING_PARAMETER,
            ("missing-lambda0", "missing-lambdaA", "missing-f0-a", "missing-fA-a"),
        ),
        _equation(
            "E3",
            "q_a(t,Omega) = n_i^lab(t,Omega) A_a^{ij} n_j^lab(t,Omega)",
            ("n_lab", "A_a_ij"),
            ("q_a",),
            ("E4", "E11"),
            ("Direction-vector and tensor normalization units are not completely frozen.",),
            ("n_lab and A_a_ij must share a frame; the complete frame and orientation are missing.",),
            EquationReadiness.BLOCKED_MISSING_ORIENTATION,
            ("missing-active-tensor-components", "missing-tensor-orientation", "missing-coordinate-frame"),
        ),
        _equation(
            "E4",
            "A_a^{ij} = A_a^{ji}; Tr(A_a) = 0",
            ("A_a_ij",),
            ("tensor_constraint_result",),
            (),
            ("Structural symmetry and trace checks do not determine component units.",),
            ("Structural checks do not supply the missing tensor orientation or frame.",),
            EquationReadiness.NUMERIC_READY,
            (),
            implementation="validate_tensor_constraints",
            scope="NON_PREDICTIVE_STRUCTURAL_CHECK_ONLY",
        ),
        _equation(
            "E5",
            "N_LSC,a(theta) = integral dE dOmega dt [Phi P sigma epsilon_LSC,a W_a]",
            ("Phi", "P", "sigma", "epsilon_LSC_a", "W_a", "theta", "integration_domain"),
            ("N_LSC_a",),
            ("E2",),
            ("Complete integrand and integration-unit contract is not frozen.",),
            ("Geometry, exposure, and response-frame contracts are incomplete.",),
            EquationReadiness.BLOCKED_MISSING_PARAMETER,
            ("missing-full-theta", "missing-frozen-numeric-config", "missing-numerical-defaults"),
        ),
        _equation(
            "E6",
            "R_a = N_obs,a / N0_a",
            ("N_obs_a", "N0_a"),
            ("R_a",),
            ("E1",),
            ("N_obs_a and N0_a must share units; R_a is dimensionless.",),
            ("No frame is required for the arithmetic ratio itself.",),
            EquationReadiness.NUMERIC_READY,
            (),
            implementation="observed_ratio",
            scope="NON_LSC_ALGEBRAIC_TRANSFORM_ONLY",
        ),
        _equation(
            "E7",
            "Delta R_a^LSC ~= lambda0*F0_a + lambdaA*FA_a",
            ("lambda0", "F0_a", "lambdaA", "FA_a"),
            ("Delta_R_a_LSC",),
            ("E8",),
            ("Delta R is dimensionless; factor and amplitude normalizations are not frozen.",),
            ("FA_a inherits the unresolved anisotropy frame contract.",),
            EquationReadiness.BLOCKED_MISSING_PARAMETER,
            ("missing-lambda0", "missing-lambdaA", "missing-f0-a", "missing-fA-a"),
        ),
        _equation(
            "E8",
            "F0_a = <f0_a>_a; FA_a = <q_a fA_a>_a",
            ("f0_a", "q_a", "fA_a", "E1_weighting"),
            ("F0_a", "FA_a"),
            ("E1", "E3"),
            ("Weight normalization and response-template units are not frozen.",),
            ("FA_a inherits q_a frame and orientation requirements.",),
            EquationReadiness.BLOCKED_MISSING_FUNCTION,
            ("missing-f0-a", "missing-fA-a", "missing-numerical-defaults"),
        ),
        _equation(
            "E9",
            "R_BEST = (R_inner, R_outer, R_outer / R_inner)",
            ("R_inner", "R_outer"),
            ("R_BEST",),
            ("E6",),
            ("R_inner, R_outer, and their ratio are dimensionless.",),
            ("No frame is required for this tuple construction.",),
            EquationReadiness.NUMERIC_READY,
            (),
            implementation="best_binned_target",
            scope="NON_LSC_ALGEBRAIC_TRANSFORM_ONLY",
        ),
        _equation(
            "E10",
            "chi2(theta,eta) = [R_obs-R_pred(theta,eta)]^T C^-1 [R_obs-R_pred(theta,eta)] + penalty(eta)",
            ("R_obs", "R_pred", "theta", "eta", "C", "penalty"),
            ("chi2",),
            ("E5", "E6", "E7"),
            ("Covariance must be consistent with residual units; the full convention is missing.",),
            ("Directional predictions inherit unresolved frame requirements.",),
            EquationReadiness.BLOCKED_MISSING_COVARIANCE,
            ("missing-full-theta", "missing-active-units", "missing-frozen-numeric-config"),
        ),
        _equation(
            "E11",
            "n_lab(t) = R_lab<-ICRS(t, latitude, longitude, detector_orientation) * n_ICRS",
            ("t", "latitude", "longitude", "detector_orientation", "n_ICRS", "R_lab_from_ICRS"),
            ("n_lab",),
            (),
            ("Time, angle, and direction conventions are not completely frozen.",),
            ("ICRS and lab roles are named; axes, orientation, timing convention, and transform are incomplete.",),
            EquationReadiness.BLOCKED_MISSING_FRAME,
            ("missing-coordinate-frame", "missing-tensor-orientation"),
        ),
        _equation(
            "E12",
            "S_a(t) = n_lab,i(t) A^{ij} n_lab,j(t)",
            ("n_lab", "A_ij", "precise_timing", "surveyed_orientation", "geometry"),
            ("S_a_t",),
            ("E4", "E11"),
            ("Tensor normalization and time convention are not frozen.",),
            ("Complete active tensor, ICRS-to-lab transform, and surveyed orientation are required.",),
            EquationReadiness.BLOCKED_MISSING_ORIENTATION,
            (
                "missing-active-tensor-components",
                "missing-tensor-orientation",
                "missing-coordinate-frame",
                "missing-precise-timing",
                "missing-sufficient-geometry",
            ),
        ),
    )


def equation_index() -> dict[str, EquationDescriptor]:
    return {equation.equation_id: equation for equation in equation_descriptors()}


def validate_tensor_constraints(A_a_ij: object) -> dict[str, object]:
    shape = TensorContract().validate_structure(A_a_ij)
    return {"equation_id": "E4", "symmetric": True, "traceless": True, "shape": list(shape)}


def observed_ratio(N_obs_a: Real, N0_a: Real) -> float:
    if isinstance(N_obs_a, bool) or isinstance(N0_a, bool) or not isinstance(N_obs_a, Real) or not isinstance(N0_a, Real):
        raise FrozenEquationBlocked("E6 inputs must be real numerical scalars.")
    if float(N0_a) == 0.0:
        raise FrozenEquationBlocked("E6 baseline expectation N0_a must be non-zero.")
    return float(N_obs_a) / float(N0_a)


def best_binned_target(R_inner: Real, R_outer: Real) -> tuple[float, float, float]:
    inner = observed_ratio(R_inner, 1.0)
    outer = observed_ratio(R_outer, 1.0)
    return (inner, outer, observed_ratio(outer, inner))


def blocked_symbolic_equation(*_: object, **__: object) -> None:
    raise FrozenEquationBlocked("This symbolic frozen equation lacks an authorized numerical contract.")


IMPLEMENTATIONS: dict[str, Callable[..., Any]] = {
    "E4": validate_tensor_constraints,
    "E6": observed_ratio,
    "E9": best_binned_target,
}


def execute_algebraic_equation(equation_id: str, **inputs: object) -> Any:
    descriptor = equation_index().get(equation_id)
    if descriptor is None:
        raise FrozenEquationBlocked(f"Unknown frozen equation ID {equation_id!r}.")
    implementation = IMPLEMENTATIONS.get(equation_id)
    if implementation is None or descriptor.execution_readiness is not EquationReadiness.NUMERIC_READY:
        raise FrozenEquationBlocked(
            f"{equation_id} is not numerically executable from the recovered frozen object.",
            details={"equation_id": equation_id, "blockers": list(descriptor.blockers)},
        )
    try:
        return implementation(**inputs)
    except TypeError as exc:
        raise FrozenEquationBlocked(
            f"Inputs for {equation_id} do not match its algebraic contract.",
            details={"equation_id": equation_id},
        ) from exc
