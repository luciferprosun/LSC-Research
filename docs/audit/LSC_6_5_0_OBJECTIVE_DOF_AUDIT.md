# LSC 6.5.0 objective and effective-DOF audit

Status: **PASS WITH REQUIRED INTERPRETIVE LIMITATION**

## Counted quantities

- independent development observables: **1**;
- observables in the objective: BEST inner-zone published aggregate ratio
  `0.791 +/- 0.05` only;
- fitted LSC physical parameters: **1** (`alpha_0`);
- fitted nuisance parameters: **0**;
- effective residual degrees of freedom: `1 - 1 - 0 = 0`.

BEST outer, GALLEX/GNO, SAGE Cr51, SAGE Ar37, and BEST-2 are explicitly absent
from the objective. The covariance is the one-by-one diagonal matrix
`[[0.0025000000000000005]]`; it is not collaboration covariance and the
inference classification remains `ASSUMPTION_BASED_SENSITIVITY_ONLY`.

## Objective structure

The frozen objective is

`chi2(alpha_0) = [(0.791 - R_pred,Cr51(alpha_0)) / 0.05]^2`.

Over the relevant branch the exact response is continuous and locally
monotone. Consequently an equivalent scalar root construction exists:

`R_pred,Cr51(alpha_0) = 0.791`.

The frozen bounded optimizer and the independent bisection reconstruction
both locate this root. The reported objective
`2.169792942258529e-20` is the floating-point residual at that construction,
not a separate empirical fit achievement. The `Delta chi2 = 1` endpoints are
equivalently the roots at predictions `0.791 - 0.05` and `0.791 + 0.05` on the
appropriate sides of the minimum.

## Required interpretation

The near-zero objective is expected from the construction and is not evidence
of extraordinary empirical agreement or validation.

With zero effective residual degrees of freedom, the minimum objective has no
goodness-of-fit meaning. It cannot establish validation, confirmation,
discovery, model preference, or a calibrated p-value. The interval is a
one-observable sensitivity interval under the frozen uncertainty assumption.

Verdict: `ZERO_EFFECTIVE_RESIDUAL_DOF_NO_GOODNESS_OF_FIT_CLAIM`.
