# Kernel Status

Machine source: `frozen_core/manifests/kernel_status.json`

Verdict: `FROZEN_SPECIFICATION_KERNEL_READY_NUMERICAL_EXECUTION_BLOCKED`

| Field | Current state |
|---|---|
| Frozen identity | verified |
| Symbolic E1-E12 | ready |
| Parameter contract | available |
| Numerical model | not ready |
| Complete parameter bundle | no |
| Complete unit contract | no |
| Complete frame contract | no |
| Complete active tensor contract | no |
| Fail-closed evaluator | available |
| Dataset contracts | ready |
| T1-T12 registry | ready |
| Preregistration package | ready |
| Covariance/nuisance/baseline/split/falsification policies | ready |
| Dry-run execution harness | ready |
| Step 05 blocker adjudication | complete |
| Frozen bundle recovery | AUTHENTIC_FROZEN_BUNDLE_INCOMPLETE |
| BEST full covariance | not located; summary prescription only |
| SAGE/GALLEX full covariance | not located |
| Nuclear covariance | marginal only |
| KATRIN/IceCube mapping | not justified |
| M3 geometry | published average geometry |
| M4 hierarchical specification | incomplete |
| T12 data | blocked directional data insufficient |
| Minimum/full unlock sets | incomplete |
| Step 05 execution boundary | active |
| STEP 06 recoverability decision | frozen |
| Historical 6.3.0 preserved | yes |
| Publication boundary | defined |
| Successor required/candidate | yes / 6.3.1 |
| Historical validation class | RETROSPECTIVE_NON_BLIND |
| Prospective validation policy | ready |
| Executable successor | not ready |
| Publication readiness | P1_SPECIFICATION_BOUNDARY_READY |
| Publication ready | no |
| Numerical prediction authorized | no |
| Validation execution authorized | no |
| Numerical validation authorized | no |

## Golden current-state result

```text
FROZEN MODEL IDENTITY: VERIFIED
E1-E12 SYMBOLIC SPECIFICATION: AVAILABLE
PARAMETER CONTRACT: AVAILABLE
NUMERICAL PARAMETER BUNDLE: INCOMPLETE
DIRECTIONAL FRAME: INCOMPLETE
ACTIVE TENSOR: INCOMPLETE

NUMERICAL LSC PREDICTION: BLOCKED
VALIDATION EXECUTION: BLOCKED

REASON:
Missing authentic frozen numerical objects.
```

The golden software test passes because this refusal is produced. It does not manufacture an example LSC curve or scientific result.

The Step 03 golden methodology test additionally requires data contracts, T1-T12, preregistration, covariance sensitivity scenarios and baseline contracts to be `READY`, while the numerical bundle, prediction, validation, T12 and BEST-2 remain respectively incomplete, blocked, blocked, blocked and future-only.

## Reproduce

```bash
PYTHONPATH=src python3 -m lsc_kernel.cli.main identity
PYTHONPATH=src python3 -m lsc_kernel.cli.main status
PYTHONPATH=src python3 -m lsc_kernel.cli.main can-predict
PYTHONPATH=src python3 -m lsc_kernel.cli.main plan-validation T3
```

The can-predict command exits with code 2 in the current state. Planning remains non-numerical and never produces an LSC result.

The separate STEP 05 acquisition verdict is BLOCKER_ADJUDICATION_COMPLETE_FROZEN_BUNDLE_STILL_MISSING. It supplements rather than replaces the stable frozen-kernel verdict above.

The STEP 06 decision verdict is LSC_6_3_0_NUMERICALLY_UNRECOVERABLE_SUCCESSOR_BOUNDARY_DEFINED. It preserves the stable fail-closed kernel verdict while establishing that any explicit numerical completion requires a distinct successor identity. No executable 6.3.1 model or publication exists yet.
