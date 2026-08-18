# BEST-2 prospective handoff

Status: `FUTURE_ONLY`, `FUTURE_BLIND`

As of the STEP 08 closure:

- observed BEST-2 data accessed: **NO**;
- BEST-2 prediction generated: **NO**;
- prediction authorized: **NO**;
- publication of a prediction: **NO**.

No one may inspect observed BEST-2 outcomes or generate a model prediction
under this handoff. A future prediction requires a separate explicit owner and
prospective-governance authorization after all prerequisites below pass.

## Preconditions for a future freeze

1. Obtain authoritative collaboration-approved as-built geometry, zone
   definitions, source insertion coordinates, isotope and branching data,
   final source assay and covariance, exposure/extraction/counting schedule,
   detector response, and nuisance/covariance policy.
2. Verify and record the frozen LSC model SHA, parameter-bundle SHA,
   scientific-specification SHA, evaluator SHA, cross-section/source-line
   SHAs, every authoritative input SHA, and preregistration SHA.
3. Record a trusted freeze timestamp before outcome access and attest that the
   model parameter will not be refit or tuned to BEST-2.
4. Only after explicit prediction authorization, generate a deterministic
   prediction artifact and record its SHA-256 and timestamp before observed
   outcomes are accessed.
5. Preserve the input, prediction, authorization, and no-refit evidence even
   if the later result is adverse.

The currently discussed 58Co source, source strength, exposure count, and
three-zone geometry are proposal-level descriptions, not authoritative
as-built inputs. No numeric prediction is present in this file.
