# Baseline benchmark report

## Classification

This report contains only `NON_PHYSICAL_TEST_FIXTURE`, `PUBLIC_RESULT_REPRODUCTION_ONLY`, baseline behavior, and `STATISTICAL_ENGINE_CONTROL`. It contains no LSC prediction or metric.

## Analytical fixtures

All 6/6 fixtures pass:

- diagonal Gaussian chi-square: exact 4.0;
- correlated Gaussian chi-square: exact 2/3;
- shared nuisance: optimum 0.5 and profiled chi-square 0.5;
- singular covariance: default rejection and explicitly reported pseudoinverse result 1.0;
- cross-validation: exact train/hold-out separation;
- model selection: one-parameter constant normalization ranks ahead of M0 on its synthetic generating example.

All fixture values are `NON_PHYSICAL_TEST_FIXTURE`. They are not LSC coefficients or predictions.

The manifest-producing execution boundary also runs 13/13 declared non-physical baseline controls: M0, M1, every registered 51Cr M2 cross-section variant, M3, experiment-normalization M4, and detector-systematic M4. Every execution converges, has a unique execution-manifest hash, and declares `LSC_used=false`.

## Public-result reproduction

All 9/9 checks pass within their frozen tolerances:

| Check | Reproduced | Reference |
|---|---:|---:|
| BEST inner measured/predicted | 0.7910662824 | 0.791 |
| BEST outer measured/predicted | 0.7658402204 | 0.766 |
| BEST outer/inner double ratio | 0.9681113168 | 0.97 |
| GALLEX Cr1 | 0.9526813880 | 0.953 |
| GALLEX Cr2 | 0.8118668596 | 0.812 |
| SAGE 51Cr | 0.95 | 0.95 |
| SAGE 37Ar | 0.7913669065 | 0.79 |
| KATRIN grid | 50×50 | 50×50 |
| KATRIN finite minimum | 1374.7638148637948 | 1374.7638148637948 |

The diagonal six-gallium control gives weighted mean 0.8050639047, diagonal standard error 0.0294424030, and chi-square 3.9864878596 about that mean. It remains `SENSITIVITY_ONLY`, is not collaboration-equivalent, and is not a combined-significance result.

## Statistical control datasets

- MicroBooNE 364×364: shape, symmetry, finite values, PSD and rank diagnostics complete.
- PROSPECT three 990×990 files: shape, symmetry, finite values, rank, signed-eigenvalue counts and conditioning diagnostics complete. The background matrix is rank-deficient; the statistical and systematic matrices are full-rank but indefinite. Negative modes are preserved as warnings, and no automatic likelihood use is allowed.
- STEREO covariance/response: shared prompt-energy axis compatible; response values finite; distinct neutrino-energy axis preserved.
- IceCube release index: all 52 entries pass path and size checks, and eight numerical CSV objects pass hash, shape, and finite-value checks; LSC mapping remains blocked.

Machine-readable evidence is under `statistics/`. The result is a verification of the statistical instrument and archived public numbers, not validation of LSC.
