# LSC 6.3.1 Executable Release Requirements

## Gate

LSC 6.3.1 must not be described as an executable model or published as an executable model release until every requirement below is complete, hash-bound, and reviewable. The current status is **NOT READY**.

## Model identity and specification

- [ ] distinct 6.3.1 model identity;
- [ ] E1-E12 equivalence declaration or justified version escalation;
- [ ] complete equation-to-code map;
- [ ] exactly one genesis-contract classification for every active element;
- [ ] no `UNRESOLVED` active element;
- [ ] no reuse of the historical 6.3.0 commit or version DOI as successor identity.

## Complete numerical object

- [ ] complete parameter vector;
- [ ] canonical serialized ordering;
- [ ] every numerical value and uncertainty;
- [ ] units and dimensions;
- [ ] frame definitions, axes, handedness, and transformations;
- [ ] tensor components, rank, dimensions, symmetry, trace rules, normalization, frame, and orientation;
- [ ] exact `f0_a` and `fA_a` definitions;
- [ ] initialization rules and evaluation order;
- [ ] bounds and explicit default policy;
- [ ] covariance and uncertainty semantics where part of the model;
- [ ] parameter decision log with data-exposure classification;
- [ ] canonical bundle SHA-256.

## Executable evaluator

- [ ] deterministic evaluator implementing the declared equations only;
- [ ] machine-readable prediction input schema;
- [ ] machine-readable output schema;
- [ ] explicit unit, frame, dimension, and domain validation;
- [ ] exact error and fail-closed behavior;
- [ ] fixed numerical algorithms, integration rules, tolerances, and precision policy;
- [ ] deterministic output on the supported environment;
- [ ] no hidden fit, calibration, or data-dependent default in prediction mode.

## Golden reference vectors

The release must contain several experiment-independent cases of:

`input -> exact or precision-bounded expected output`

The cases must cover at minimum:

- scalar-only legal execution;
- tensor structure and frame handling where active;
- unit conversion or rejection behavior;
- boundary/domain behavior;
- deterministic repeated execution;
- at least one intentional fail-closed case.

Golden vectors must not be tuned to BEST, SAGE, GALLEX/GNO, KATRIN, IceCube, or BEST-2 outcomes. Each vector requires its own SHA-256 and stated numerical tolerance.

## Reproducible environment

- [ ] source commit identity;
- [ ] dependency lockfile;
- [ ] Python/compiler/BLAS/platform declaration;
- [ ] container or equivalent reproducible environment where practical;
- [ ] deterministic seeds where randomness is unavoidable;
- [ ] build and execution instructions from a clean checkout;
- [ ] software tests, integration tests, numerical-stability tests, and release smoke tests.

## Provenance and release manifest

- [ ] source reference and hash for every preserved object;
- [ ] decision record for every new object;
- [ ] exposure/training-data disclosure for every fit-derived value;
- [ ] parameter bundle hash;
- [ ] evaluator/source hash;
- [ ] environment hash;
- [ ] golden-vector hashes;
- [ ] release-manifest hash;
- [ ] Git commit and future release tag;
- [ ] Zenodo version DOI reserved only at release preparation;
- [ ] explicit link to historical 6.3.0 and separate Validation Kernel companion.

## Validation boundary

- [ ] historical data labelled `RETROSPECTIVE_NON_BLIND` where exposed;
- [ ] prospective targets identified before outcome access;
- [ ] preregistration and multiple-testing policy retained;
- [ ] model freeze completed before retrospective execution;
- [ ] prospective prediction artifact created only after model freeze;
- [ ] no claim that 6.3.1 is an exact recovered numerical copy of 6.3.0;
- [ ] no claim that blocked tests passed or failed.

## Readiness levels

| Level | Requirement | Current state |
|---|---|---|
| `P0_HISTORICAL_PRESERVATION_READY` | Historical 6.3.0 identity and evidence preserved. | READY |
| `P1_SPECIFICATION_BOUNDARY_READY` | Recoverability and successor genesis boundary frozen. | READY |
| `P2_EXECUTABLE_SUCCESSOR_READY` | Complete bundle, evaluator, vectors, provenance, environment. | NOT READY |
| `P3_RELEASE_PACKAGE_READY` | Tagged, hashed, citation-ready package. | NOT READY |
| `P4_RETROSPECTIVE_VALIDATION_READY` | Frozen successor plus authorized retrospective execution. | NOT READY |
| `P5_PROSPECTIVE_PREDICTION_READY` | Frozen target inputs and pre-outcome prediction protocol. | NOT READY |

Passing P2 does not automatically pass P3-P5. Each higher level requires its own explicit gate.
