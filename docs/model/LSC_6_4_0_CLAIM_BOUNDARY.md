# LSC 6.4.0 STEP 07C claim boundary

Final development status: **`DEVELOPMENT_PARAMETER_DETERMINATION_FAILED`**.

The canonical claim-by-claim record is [LSC_6_4_0_CLAIMS_MATRIX.csv](../scientific/LSC_6_4_0_CLAIMS_MATRIX.csv). STEP 07D makes the scientific attempt immutable; it does not alter the STEP 07C result.

## Allowed

- A2/C/A is explicitly owner-authorized as a new LSC 6.4.0 physical hypothesis.
- The Bahcall-table natural-spline cross-section representation is versioned and executable.
- The one-parameter trace-only evaluator is deterministic and fail-closed for explicit in-domain `alpha_0`.
- Fifteen golden vectors and an independent reference implementation pass.
- One preregistered retrospective, non-blind parameter determination was executed.
- That determination failed because the requested optimum was outside the frozen first-order domain and the bounded result was boundary dominated.
- No parameter was frozen and no validation was subsequently performed.
- The adverse result is preserved as a development artifact rather than repaired.

## Prohibited

- “LSC 6.4.0 is validated” or “confirmed.”
- “A frozen alpha_0 was obtained.”
- “LSC 6.4.0 RC1 is ready.”
- Any BEST-2 prediction or confirmation claim.
- Any anisotropic, directional, or T12 claim.
- Any KATRIN or IceCube confirmation/exclusion claim.
- Collaboration-level significance from `COV_DIAGONAL`.
- Any claim that A2 was uniquely recovered from LSC 6.3.0.
- “The boundary value is the LSC 6.4.0 parameter.”
- “LSC 6.4.0 was falsified.” The failed development determination is not a model-validation test.
- Any claim that a proposed exact finite-dilation successor is part of LSC 6.4.0.

The parameter-determination failure is not hidden and is not repaired. Any finite or nonlinear closure requires a separately authorized model version and new preregistration.
