# LSC 6.3.0 Recoverability Decision

## Decision

Overall verdict: **`NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE`**

This verdict is bounded by the evidence available and searched through 2026-08-16. It does not assert that a complete numerical object never existed. It states that the historical release can be identified and its symbolic physics can be recovered, but its complete executable numerical state cannot be reconstructed from admissible evidence without making new scientific or numerical decisions.

The resulting STEP 06 decision is:

`LSC_6_3_0_NUMERICALLY_UNRECOVERABLE_SUCCESSOR_BOUNDARY_DEFINED`

## Three independent recoverability levels

| Level | Verdict | Evidence | Consequence |
|---|---|---|---|
| Identity recoverability | `FULLY_RECOVERABLE` | Historical commit `6ffa07bdde533fcc2a550e36c762b8edd9236c47`, freeze commit `a6d582694d55fa0260ef7ab07ed83fd06feef607`, version DOI `10.5281/zenodo.20377427`, concept DOI `10.5281/zenodo.19780615`, and release metadata agree. | The historical object remains uniquely identifiable and citable. |
| Symbolic recoverability | `FULLY_RECOVERABLE` | Canonical E1-E12 source is recovered and bound to SHA-256 `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981`. Active parameter names, roles, and freeze boundary are recovered. | The symbolic framework may be preserved or formalized with explicit provenance. This does not authorize numerical execution. |
| Numerical recoverability | `NUMERICALLY_UNRECOVERABLE_WITH_CURRENT_EVIDENCE` | STEP 01 and targeted STEP 05 searches did not locate the complete vector, ordering, response functions, values, units, frames, tensor state, initialization, defaults, bounds, evaluator, or prediction table. | Exact historical 6.3.0 prediction and validation remain unauthorized. Any explicit numerical completion is a successor version. |

## Q1 - Was the historical 6.3.0 identity recovered?

**YES.** The release identity, commit, DOI lineage, canonical freeze boundary, and archived release are mutually consistent. This is an identity/provenance result, not an executable-model result.

## Q2 - Was the symbolic E1-E12 physics recovered?

**YES, as a symbolic specification.** All E1-E12 descriptors are machine-readable and hash-bound. Two dependency edges remain explicitly unverified where the historical source does not determine an exact prediction binding; the kernel does not invent those dependencies. The recovered symbolic object contains no complete numerical parameter state.

## Q3 - Was the complete numerical state recovered?

**NO.** The parameter-by-parameter adjudication leaves every evaluator-critical numerical object `STILL_MISSING` or rejects the available historical candidate. The absence includes:

- complete `theta` and canonical ordering;
- numerical `lambda0` and `lambdaA`;
- exact `f0_a` and `fA_a`;
- active tensor values, ordering, normalization, orientation, and complete frame;
- complete units, transformations, covariance, initialization, bounds, defaults, and normalization order;
- executable evaluator inputs, canonical prediction configuration, and frozen prediction table.

## Q4 - Can 6.3.0 be executed numerically without additional decisions?

**NO.** Execution would require choosing at least one missing value, convention, mapping, or algorithm. Such a choice would be a new specification decision, not recovery. The fail-closed evaluator therefore returns `prediction_authorized=false`.

## Q5 - Can an exact frozen validation of 6.3.0 be performed?

**NO.** The universal numerical-bundle prerequisite for T1-T11 is incomplete. T12 also lacks timing, surveyed orientation, exact geometry, active tensor, frame, unit, and statistical prerequisites. External vetoes additionally lack justified mappings. This is `TEST_BLOCKED`, not a failed physical test.

## Q6 - Can 6.3.0 be completed honestly without creating a new version?

**NO.** Any numerical value or convention that is not directly authenticated as historical 6.3.0 content changes the recoverable object. A new complete numerical model must have a new version identity and a parameter decision log. The approved successor candidate is 6.3.1 only if E1-E12 and the model class remain unchanged.

## Scientific state taxonomy

| State | Current value | Meaning |
|---|---|---|
| `MODEL_FALSIFIED` | `false` | No authorized numerical test produced evidence against the model. |
| `MODEL_NOT_NUMERICALLY_RECOVERABLE` | `true` | The historical numerical predictor cannot be independently reconstructed from current admissible evidence. |
| `TEST_BLOCKED` | `true` | Required model, data, covariance, mapping, or directional prerequisites are absent. |

These states must never be conflated. Reproducibility failure is not physical falsification, while lack of falsification does not make 6.3.0 a complete reproducible predictor.

## Evidence basis and scope

This decision is derived from:

- [STEP 01 recovery report](../recovery/STEP_01_FROZEN_OBJECT_RECOVERY_REPORT.md);
- [STEP 02 frozen kernel report](../kernel/STEP_02_FROZEN_SPECIFICATION_KERNEL_REPORT.md);
- [STEP 03 methodology report](../validation/STEP_03_VALIDATION_METHODOLOGY_REPORT.md);
- [STEP 04 statistical engine report](../statistics/STEP_04_BASELINE_LIKELIHOOD_REPORT.md);
- [STEP 05 acquisition report](../acquisition/STEP_05_BLOCKER_ACQUISITION_REPORT.md);
- [frozen parameter adjudication](../acquisition/FROZEN_PARAMETER_ADJUDICATION.csv);
- [negative findings](../acquisition/NEGATIVE_FINDINGS.md).

Private author devices, deleted remote-only objects, unpublished workspaces, and collaboration-held objects were unavailable. A future authentic discovery can be adjudicated as new evidence, but it cannot silently revise this recorded decision.
