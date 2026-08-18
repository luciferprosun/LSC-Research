# LSC 6.4.0 adverse development-result record

Status: **`DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`**

This record preserves the owner-authorized linear A2/C/A attempt exactly as it stood at STEP 07C. It is a scientific development result, not an implementation defect, model validation, model falsification, successful fit, or release candidate.

## Frozen scientific attempt

| Object | Frozen value |
|---|---|
| Model | LSC 6.4.0 |
| Configuration | A2/C/A |
| Response | `F_m(E)=d ln sigma_m(E)/d ln E`; `S_a=alpha_0 F_m`; `R_pred,a=1+alpha_0<F_m>_a` |
| Response classification | `NEW_PHYSICAL_HYPOTHESIS_6_4_0` |
| Tensor | disabled |
| Sharing | one universal `alpha_0`; no zone-, isotope-, or experiment-specific LSC coefficient |
| Response SHA-256 | `c548592b44d0f75ecfd24f2392e07492920711415b207cf74c4bd31526fdceb8` |
| Cross-section scenario | `BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE` |
| Cross-section payload SHA-256 | `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5` |
| Interpolation | natural cubic spline, analytic derivative, no extrapolation |
| Pre-fit freeze SHA-256 | `60380837f348cc41dc3d0b240fcba0b61a95c9f61cfab2bc3f5e7db71e9ea179` |
| Development data | published BEST inner aggregate ratio only |
| Exposure | `MODEL_EXPOSED`, `RETROSPECTIVE_NON_BLIND`, `DEVELOPMENT_DATA` |
| Objective | one-parameter diagonal Gaussian chi-square |
| Covariance | `COV_DIAGONAL`, `ASSUMPTION_BASED_SENSITIVITY_ONLY` |
| Frozen fit domain | `[-0.06137569484389956, 0.09541395625505644]` |
| Executions authorized/performed | 1 / 1 |

## Preserved outcome

| Quantity | Result |
|---|---:|
| unconstrained diagnostic optimum | `-0.1159773471000784` |
| constrained optimizer result | `-0.06137569305004568` |
| objective at constrained result | `3.872735360003486` |
| objective at exact lower bound | `3.872735105537897` |
| objective at null | `17.47239999999999` |
| optimizer convergence | PASS |
| boundary status | `BOUNDARY_DOMINATED` |
| parameter bundle | NOT CREATED |
| LSC 6.4.0 RC | NOT CREATED |

The preregistered failure rule was triggered because the unconstrained optimum lies below the frozen first-order domain and the constrained solution is boundary dominated. No certified interval was produced.

## Immutable interpretation

- The linear bound is not widened.
- Neither the constrained boundary value nor the unconstrained diagnostic value is a frozen LSC parameter.
- The response, spline, cross-section payload, development observation, covariance scenario, objective, and result are not changed.
- No holdout evaluation, retrospective smoke, BEST-2 prediction, parameter bundle, RC, tag, or publication followed the failure.
- A later finite response is a separately authorized successor hypothesis and cannot be relabelled as LSC 6.4.0.

Canonical machine-readable preservation is recorded in `LSC_6_4_0_ADVERSE_RESULT_FREEZE.json`. The frozen STEP 07C repository identity is commit `e53db798f1f3f448034a6e0af6399e8256189cd5`.
