# STEP 03 - VALIDATION METHODOLOGY RESULT

Project: LSC Validation Kernel
Status: PASS
Methodology verdict: `VALIDATION_METHODOLOGY_READY_NUMERICAL_VALIDATION_BLOCKED`

Step 03 froze a source-backed methodology and implemented a deterministic planning layer. It did not recover or invent the missing numerical LSC object, compute an LSC prediction, fit/refit LSC, evaluate a hold-out LSC prediction, calculate LSC significance, issue an external veto or create a BEST-2 prediction.

## A. Input state

- branch: `main`
- Step 02 input commit: `f129e1f1d099c5a02574a9e262148d4b17c9f1fd`
- historical LSC 6.3.0 HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`
- freeze commit: `a6d582694d55fa0260ef7ab07ed83fd06feef607`
- freeze tag: `pre-validation-kernel-recovery`
- worktree at entry: clean
- remote visibility at entry: PRIVATE
- public push: NO

All mandatory Step 01/02 recovery, provenance, missing-object and kernel reports were read before implementation. The provenance registry and frozen identity remain unchanged.

## B. Dataset contracts

`ValidationDatasetRegistry` now holds 13 immutable contracts for BEST, GALLEX/GNO, SAGE 51Cr, SAGE 37Ar, gallium cross sections, KATRIN, IceCube, Borexino, Daya Bay, PROSPECT, STEREO, MicroBooNE and BEST-2.

The registry fixes repository-relative source identity, hash, version, grade, count, observables, uncertainty/covariance/timing/geometry/orientation boundaries, allowed/prohibited tests, exposure class, blindness and deterministic row/transformation rules. All 13 pinned source hashes pass. Primary CSV schemas and mandated row counts pass.

Specific preserved facts:

- BEST: 20 rows, 10 exposures, two zones;
- BEST discrepancy: outer candidate row sum 1070 and combined source row 1069 preserved under `PRESERVE_SOURCE_DISCREPANCY`;
- GALLEX/GNO: 83 rows, including 18 Cr source rows with Cr1/Cr2 grouping;
- SAGE 51Cr: 12 records, 8 primary plus 4 controls;
- SAGE 37Ar: 11 records, 10 primary plus Ar3-2 control;
- raw sources have no write path and remain byte-identical.

## C. Cross-section models

`GalliumCrossSectionModelRegistry` loads all 15 archived model/isotope rows, including Bahcall, Haxton, Barinov, Kostensalo, Semenov and Elliott-Gavrin-Haxton alternatives. Values, marginal uncertainty, isotope, source and ground/excited-state status retain source provenance. There is no default/correct model. Cross-isotope covariance remains missing, and incompatible Krofcheck/Frekers alternatives are not combined.

## D. T1-T12 registry

The canonical numbering was recovered from `FROZEN_PREDICTION_PROTOCOL.md`:

- T1/T2: reciprocal BEST zone transfer;
- T3/T4: reciprocal BEST versus GALLEX/SAGE transfer;
- T5: 51Cr to 37Ar transfer;
- T6/T7: leave-one-run and leave-one-experiment out;
- T8/T9: cross-section and systematic/covariance sensitivity;
- T10/T11: sterile and null/baseline comparisons;
- T12: directional/sidereal.

Each test has exactly one primary readiness enum, explicit blockers and complete machine fields for question, hypothesis, data, split, target, observable, statistics, baselines, nuisance/covariance/cross-section handling, timing, geometry, orientation, outcome rule and reporting.

T12 remains `BLOCKED` with `BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT`. Precise timing, surveyed orientation, sufficient geometry, authentic active tensor, frame transforms and units are required. Exposure midpoint is rejected as event time.

## E. Baseline models

Historical M0-M6 labels and semantics are preserved. Stable aliases expose null, constant deficit, cross-section variant, detector systematic, experiment normalization, hierarchical experiment and sterile 3+1 contracts without renumbering the source hierarchy. M5/M6 remain frozen LSC models, not fit targets.

No baseline or LSC fit was executed.

## F. Covariance and nuisance policy

Five covariance scenarios are frozen:

- `COV_DIAGONAL`;
- `COV_UNCORRELATED_SYSTEMATICS`;
- `COV_FULLY_COMMON_SELECTED`;
- `COV_PLAUSIBLE_SCAN`;
- `COV_COLLABORATION`.

The first four are assumption-based and `SENSITIVITY_ONLY`; they prohibit discovery, exclusion, sigma evidence and decisive-preference language. `COV_COLLABORATION` remains unavailable until an authentic source matrix/likelihood is acquired.

Ten nuisance categories define scope and possible correlations across runs, zones, experiments and isotopes. Unknown covariance remains unknown.

## G. Splits, exposure and blindness

Sixteen stable split contracts cover BEST zone transfer, early/late, four LORO families, explicit LOEO, experiment-family hold-out, cross-experiment and cross-isotope transfer. Membership is identifier-driven and not result-adaptive.

Historical datasets are `MODEL_EXPOSED` and `NON_BLIND_HISTORICAL`; none is described as a clean blind hold-out. BEST-2 is `MODEL_PREEXISTING`, `FUTURE_BLIND`, and contains zero observed records.

## H. Preregistration and multiple testing

The `preregistration/` package contains the master policy and machine-readable datasets, tests, splits, covariance, baselines, nuisance, metrics, falsification, no-refit, external mapping, cross-section, BEST-2, execution-manifest and result-schema artifacts.

The historical project did not freeze a multiple-testing correction. Status therefore remains `MULTIPLE_TESTING_POLICY_UNRESOLVED`. Primary, secondary, sensitivity and blocked families are classified; three candidate strategies are documented, none is selected. Global confirmation claims remain prohibited until this pre-result decision is adjudicated.

## I. No-refit enforcement

`NoRefitPolicy` differentiates baseline fitting, nuisance profiling and frozen LSC evaluation. Attempts to fit, refit, optimize or calibrate M5/M6/frozen LSC raise `FrozenModelRefitForbidden`. Profiling a frozen LSC field is also rejected. Software tests demonstrate that a baseline fit can be authorized without opening a frozen-parameter fit path.

## J. External constraints

The KATRIN loader validates the current 50x50 absolute chi-square grid without assigning confidence coverage. The IceCube loader validates the 52-record release index without reinterpreting release confidence construction.

Both constraint contracts require a quantitative LSC-observable mapping. Current state is `EXTERNAL_VETO_BLOCKED_MAPPING_MISSING`; no veto or likelihood multiplication was performed. Borexino is registered as `METHODOLOGY_CONTROL`, not direct gallium evidence.

## K. BEST-2

`BEST2FuturePredictionContract` records the 58Co proposal identity, proposed geometry/exposure concepts, future prediction schema, freeze prerequisites and hash requirements. It contains no prediction values, no observed rows and no freeze timestamp. Status is `FUTURE_ONLY` / `FUTURE_BLIND`.

## L. Dry-run harness

`DryRunValidationHarness` verifies hashes and schemas, resolves a test, stable split, baseline contracts, covariance scenario and nuisance policy, then emits a deterministic `ValidationExecutionManifest` with model/data/code/environment provenance.

Every plan sets:

- `authorization_state=PLANNING_ONLY_BLOCKED`;
- `prediction_authorized=false`;
- `numerical_validation_authorized=false`;
- `LSC_prediction_performed=false`;
- `validation_result_computed=false`.

`lsc-kernel plan-validation T3` is operational and returns explicit blockers rather than a result.

## M. Reporting and falsification

The reporting policy mandates all preregistered, null, adverse, failed and blocked results, all folds/scenarios and exact provenance. The future `ValidationResult` schema is present but no scientific result is instantiated.

Falsification is separated into test-, component- and model-level rules. Simpler equal/better baselines remove the claimed predictive advantage; failures do not silently disappear, but one failure is not globally escalated unless a pre-result rule says so.

## N. Machine status

Ready:

- symbolic kernel;
- dataset contracts;
- T1-T12 registry;
- preregistration package;
- covariance sensitivity policy;
- nuisance registry;
- baseline registry;
- split registry;
- falsification registry;
- deterministic dry-run harness.

Blocked:

- numerical frozen model;
- complete parameter bundle;
- numerical LSC prediction;
- numerical LSC validation;
- T12;
- KATRIN/IceCube veto mappings;
- BEST-2 prediction.

## O. Tests and integrity

- Python software suite: 79/79 PASS;
- generated Step 02/03 artifacts: byte-deterministic PASS;
- 13 dataset source hashes: PASS;
- primary CSV row/schema checks and KATRIN 50x50 grid: PASS;
- full preserved source archive SHA-256: 1882/1882 PASS;
- nested repositories: 4/4 clean;
- publication-path scan: 0 findings;
- `git diff --check`: PASS;
- numerical prediction/provider calls: 0;
- physics fits/refits: 0;
- BEST-2 predictions: 0;
- public pushes: 0.

## P. Files created

- `src/lsc_kernel/validation/`: dataset, registry, policy, external, BEST-2, execution and result modules;
- `preregistration/`: master plus 18 machine/readable policy artifacts;
- `docs/validation/`: eight policy/specification documents and this report;
- `tests/test_step03_methodology.py`;
- `tools/generate_step03_artifacts.py`.

Existing kernel status, CLI, evaluator authorization message, architecture, README, package metadata and Step 02 regression tests were updated without modifying the frozen equations, parameter schema, provenance registry or preserved source archive.

## Q. Remaining blockers

1. complete authentic frozen numerical parameter bundle/evaluator inputs;
2. full collaboration covariance/likelihood workspaces;
3. pre-result multiple-testing adjudication for global inference;
4. exact external LSC-to-KATRIN/IceCube mappings;
5. T12 timing, surveyed orientation, geometry, tensor, frames, units and statistic/power rule;
6. BEST-2 as-built/source/schedule inputs before any sealed future prediction.

## R. Historical integrity

The historical LSC, freeze tag, provenance registry, recovery evidence and ignored `LSC_6_3_0_VALIDATION/` archive remain unchanged. No history rewrite, rebase, force push, public push or release occurred.

## S. Step 04 readiness

`READY FOR STEP 04: YES`, limited to a separately authorized pre-result methodology-adjudication and software-validation step.

Recommended Step 04 decision: seal the unresolved multiple-testing/global-inference choice, define acquisition/adjudication gates for collaboration covariance and external mappings, and implement numerical baseline/likelihood software only against non-physical fixtures or published reproduction targets. Keep numerical frozen-LSC execution blocked until an authentic complete bundle passes provenance review.
