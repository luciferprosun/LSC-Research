# Step 04 baseline and likelihood report

## Result

Project: LSC Validation Kernel

Status: PASS

Statistical-engine verdict: `BASELINE_LIKELIHOOD_ENGINE_READY_LSC_NUMERICAL_EXECUTION_BLOCKED`

Step 04 proves that the independent likelihood, covariance, nuisance, baseline, comparison, and cross-validation machinery works against analytical fixtures and archived public controls. It does not evaluate LSC. The missing authentic frozen numerical object remains the reason LSC prediction and validation are blocked.

## A. Input state

- Step 03 input commit: `4553c25205c1c2fcb13c2c97c3a0d1af724a78fe`;
- Step 02 commit: `f129e1f1d099c5a02574a9e262148d4b17c9f1fd`;
- historical LSC 6.3.0 HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- freeze commit: `a6d582694d55fa0260ef7ab07ed83fd06feef607`;
- freeze tag: `pre-validation-kernel-recovery`;
- input branch: `main`;
- input worktree: clean;
- numerical LSC execution at entry: blocked.

All required Step 02/03 reports, policies, registries, and preregistration documents were read before implementation.

## B. Likelihood engine

Implemented a formal `LikelihoodModel` and deterministic Gaussian likelihood layer with diagonal and full-covariance chi-square, masks, explicit fitted-parameter counts, pull terms, and release-native grid lookup. Results distinguish raw from profiled statistics, observations, fitted parameters, degrees of freedom when justified, convergence, assumptions, diagnostics, nuisance values, and warnings.

Normalized predictive log-likelihood is not inferred from chi-square. Grid interpolation is not authorized. Malformed/non-finite/dimensionally inconsistent inputs fail closed.

## C. Covariance engine

`CovarianceMatrix` validates square shape, dimensions, finite values, symmetry, eigenvalue spectrum, PSD state, rank, singularity, and condition number. Direct solve is used only for admissible nonsingular matrices. Singular input is rejected unless an explicit pseudoinverse policy and tolerance are supplied; use and effective rank are reported.

Implemented exactly the five Step 03 scenario IDs. `COV_COLLABORATION` remains unavailable without an authenticated matrix. The other four remain `SENSITIVITY_ONLY`, and the plausible correlation grid is fixed before results.

## D. Nuisance engine

Implemented fixed, Gaussian-pull, bounded, correlated, shared, and experiment-specific nuisance contracts. Additive and fractional-multiplicative effect vectors are explicit. All fitted/fixed values, priors, bounds, optimizer diagnostics, data statistic, pull statistic, and covariance diagnostics are reportable.

The analytical shared-nuisance optimum and statistic are reproduced exactly within tolerance. Nuisance profiling cannot alter frozen LSC parameters.

## E. Baseline models

- M0 null/published expectation: executable;
- M1 constant deficit: executable with one fitted normalization;
- M2 cross-section variant: executable per explicitly selected registered model, with no default/correct model;
- M3 standard sterile 3+1: executable with explicit L/E and bounds, with no LSC parameters or inferred geometry;
- M4 experiment normalization: executable with parameter-count growth reported;
- M4 detector systematic: executable with explicit response;
- M4 hierarchical experiment: `SPECIFICATION_INCOMPLETE`, because no canonical hierarchy/prior was frozen;
- M5/M6/frozen LSC: fit and statistical dispatch forbidden.

Baseline outcomes cannot alter LSC, T1-T12, covariance scenarios, splits, or primary endpoints.

## F. Model comparison and cross-validation

Delta chi-square, likelihood-ratio statistic, AIC, BIC, predictive log-likelihood, and model-comparison result contracts are implemented with prerequisite checks. No automatic Wilks, coverage, significance, or normalized-likelihood assumption is made.

Leave-one-run-out, leave-one-experiment-out, zone, isotope, and experiment transfer folds use stable IDs. Training and hold-out indices must be disjoint. Fit callbacks receive training values only and must return exact fit provenance; a mismatch raises `DataLeakageError`. Nuisance refit policy and transferred parameters are recorded per fold.

## G. Multiple-testing adjudication

Status changed before LSC evaluation from `MULTIPLE_TESTING_POLICY_UNRESOLVED` to `MULTIPLE_TESTING_POLICY_FROZEN`.

Selected family: `LSC_PRIMARY_FIXED_SEQUENCE_V1`.

Primary order: `T11 -> T7 -> T3 -> T1 -> T10`, with fixed-sequence hierarchical gatekeeping at family-wise alpha 0.05 and a mandatory stop at the first non-rejection, blocker, invalid endpoint, or unavailable prerequisite. T2/T4/T6 are secondary descriptive; T5/T8/T9 are sensitivity-only; T12 remains blocked.

Holm FWER, Benjamini-Hochberg FDR, and one-primary-plus-descriptive-secondary strategies were recorded as alternatives. The selected strategy follows the scientific dependency order and does not assume the heavily shared datasets are independent. No result information was used.

## H. Statistical fixtures

All 6/6 `NON_PHYSICAL_TEST_FIXTURE` controls pass:

1. diagonal Gaussian analytic result;
2. correlated Gaussian analytic result;
3. shared nuisance exact optimum;
4. singular rejection and explicit pseudoinverse;
5. cross-validation leakage guard;
6. known baseline model ranking.

No fixture value is an LSC parameter or prediction.

## I. Public reproduction

All 9/9 `PUBLIC_RESULT_REPRODUCTION_ONLY` checks pass: BEST inner and outer measured/predicted, BEST double ratio, GALLEX Cr1/Cr2, SAGE 51Cr/37Ar, KATRIN 50×50 dimensions, and KATRIN finite minimum.

The six-gallium diagonal combination is retained only as `SENSITIVITY_ONLY`; it is not collaboration-equivalent and is not reported as a combined significance.

## J. External and statistical controls

- KATRIN: 50×50 absolute chi-square grid, finite minimum and axes validated; no interpolation and no LSC mapping;
- IceCube: 52-entry release index plus eight numerical CSV objects have path, size, hash, shape, and finite-value checks; LSC mapping remains blocked;
- MicroBooNE: 364×364 shape, symmetry, finite, rank/eigenvalue/condition diagnostics complete;
- PROSPECT: three 990×990 files have shape/symmetry/finite diagnostics; the background matrix is rank-deficient, while the statistical and systematic matrices are full-rank but indefinite. Negative modes are disclosed, not repaired, and block automatic standalone likelihood use;
- STEREO: covariance/response prompt-energy compatibility and finite response validated without conflating prompt and neutrino-energy axes.

These are `STATISTICAL_ENGINE_CONTROL`, not direct physical evidence for LSC.

## K. LSC hard gate

`lsc-kernel can-predict` remains `NO`. `lsc-kernel run-validation T3 --model LSC` is rejected before likelihood evaluation. Optimizer and baseline dispatch independently reject LSC/M5/M6. External veto mappings remain unavailable. The golden state is:

```text
FROZEN MODEL IDENTITY: VERIFIED
SYMBOLIC KERNEL: READY
VALIDATION METHODOLOGY: READY
LIKELIHOOD ENGINE: READY
COVARIANCE ENGINE: READY
NUISANCE ENGINE: READY
BASELINE MODELS: READY
CROSS VALIDATION: READY
PUBLIC REPRODUCTION: PASS
STATISTICAL CONTROL DATASETS: PASS

LSC NUMERICAL BUNDLE: INCOMPLETE
LSC PREDICTION: BLOCKED
LSC VALIDATION: BLOCKED
T12: BLOCKED
BEST-2: FUTURE_ONLY
```

## L. Tests and reproducibility

- Python suite: 120/120 PASS, plus 18 parameterized subtests;
- analytical fixtures: 6/6 PASS;
- public reproduction: 9/9 PASS;
- deterministic Step 02/03/04 artifact regeneration: PASS;
- dataset contract source hashes and structures: PASS;
- full preserved archive manifest hash check: 1882/1882 PASS;
- nested Git repositories: clean and unchanged;
- publication-path policy scan: PASS;
- `git diff --check`: PASS;
- NumPy: 2.5.2;
- SciPy: 1.18.0;
- physics fits/refits: 0;
- numerical LSC predictions: 0;
- BEST-2 predictions: 0;
- public pushes/releases: 0.

The exact final test count and commit identity are also reported in the completion response after the single Step 04 commit.

## M. Machine-readable artifacts

- `statistics/statistical_fixtures.json`;
- `statistics/baseline_execution_controls.json`;
- `statistics/public_reproduction.json`;
- `statistics/statistical_control_diagnostics.json`;
- `statistics/baseline_benchmark.json`;
- `statistics/fixture_execution_manifest.json`;
- result and execution-manifest JSON Schemas;
- `preregistration/multiple_testing_policy.json`;
- `preregistration/multiple_testing_dependency_map.json`;
- extended `frozen_core/manifests/kernel_status.json`.

Execution manifests always declare `LSC_used=false`. The deterministic fixture timestamp is a non-wall-clock label, not a fabricated scientific observation time.

## N. Historical integrity and Git state

The frozen E1-E12 descriptors, parameter schema, provenance registry, Step 01 recovery evidence, historical LSC repository, source archive, data files, and freeze tag were not modified. No fit, rebase, history rewrite, force push, public push, or release occurred.

One logical commit is created with subject `Step 04: implement baseline and likelihood engine`. Its SHA is intentionally obtained from Git after this report is staged; no document pretends to know the hash of the commit that contains itself.

## O. Remaining blockers and Step 05 readiness

Remaining blockers are:

1. complete authentic frozen numerical parameter bundle and evaluator inputs;
2. authenticated collaboration covariance/likelihood workspaces;
3. source-defined handling or transformation for PROSPECT matrices before standalone likelihood use;
4. exact LSC-to-KATRIN and LSC-to-IceCube mappings;
5. complete gallium geometry averaging inputs for production M3 use;
6. canonical hierarchical-model distribution/prior if that optional baseline is retained;
7. T12 timing, surveyed orientation, geometry, active tensor, frames, units, statistic and power rule;
8. BEST-2 as-built/source/schedule inputs before any sealed future prediction.

`READY FOR STEP 05: YES`, limited to a blocker-closure/provenance-adjudication step. Numerical LSC validation remains unauthorized until an authentic complete bundle passes the frozen contracts.

Recommended Step 05 decision: acquire and adjudicate missing authentic numerical/model, collaboration-covariance, geometry, and external-mapping objects against the existing fail-closed contracts. Do not fit or validate LSC merely because the statistical engine is now ready.
