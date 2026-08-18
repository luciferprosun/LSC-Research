# LSC 6.4.0 alpha_0 determination report

Status: **ADVERSE RESULT PRESERVED**

Verdict: **`LSC_6_4_0_PARAMETER_DETERMINATION_FAILED`**

## Frozen protocol

The only development observation is the published BEST inner-zone aggregate ratio `0.791 +/- 0.05`, selected through the pre-existing `SPLIT_BEST_INNER_TO_OUTER` policy. BEST outer, GALLEX/GNO, SAGE Cr51, and SAGE Ar37 are excluded from the objective. These historical data are permanently labelled:

- `MODEL_EXPOSED`;
- `RETROSPECTIVE_NON_BLIND`;
- `DEVELOPMENT_DATA`.

The objective is a one-observation diagonal Gaussian chi-square under `COV_DIAGONAL`. Because the full collaboration covariance is unavailable, its inferential class is `ASSUMPTION_BASED_SENSITIVITY_ONLY`. No nuisance parameter is separately profiled and no covariance is invented.

## Pre-fit audit

All gates passed before execution:

- owner authorization A2/C/A;
- response and cross-section hashes;
- interpolation and derivative;
- input/output schemas;
- deterministic evaluator;
- golden vectors `15/15`;
- independent reference agreement;
- development/holdout split;
- objective, covariance and bounds;
- BEST-2 observed-data non-access.

Pre-fit freeze SHA-256: `60380837f348cc41dc3d0b240fcba0b61a95c9f61cfab2bc3f5e7db71e9ea179`.

## Single authorized execution

| Quantity | Value |
|---|---:|
| `mean_F_m` for Cr51 | 1.8020760538663734 |
| unconstrained diagnostic optimum | -0.1159773471000784 |
| curvature standard-error diagnostic | 0.02774577681820058 |
| frozen fit domain | [-0.06137569484389956, 0.09541395625505644] |
| constrained optimizer output | -0.06137569305004568 |
| chi-square at constrained output | 3.872735360003486 |
| chi-square at exact lower bound | 3.872735105537897 |
| chi-square at null | 17.47239999999999 |
| optimizer convergence | PASS, 38 evaluations |
| identifiability | one-dimensional and identifiable |
| boundary status | `BOUNDARY_DOMINATED` |

The unconstrained optimum lies below the frozen first-order analysis domain. The bounded optimizer consequently converges at the lower boundary. This triggers the preregistered failure rule even though the numerical optimizer itself converged.

## Consequences

- No certified `alpha_0` is frozen.
- No `LSC_6_4_0_PARAMETER_BUNDLE.json` is created.
- No retrospective smoke evaluation is run.
- No `LSC-6.4.0-rc1` is created.
- No second fit, bound widening, response change, or cross-section selection is authorized.
- The result is parameter determination, not validation or falsification of every possible LSC model.

Any future change to A2, its validity threshold, development data, or cross-section scenario requires a new owner-authorized model revision with a new pre-fit freeze. It cannot be called a refit of this candidate.
