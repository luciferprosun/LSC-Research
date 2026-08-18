# LSC 6.5.0 parameter-freeze, exposure, and no-refit audit

Status: **PASS**

## Frozen result

- `alpha_0 = -0.14388795521516184`;
- profile-`Delta chi2 = 1` interval:
  `[-0.19024973740805776, -0.10233891434687088]`;
- objective: `2.169792942258529e-20`;
- classification: `RETROSPECTIVE_NON_BLIND_PARAMETER_DETERMINATION`;
- inference: `ASSUMPTION_BASED_SENSITIVITY_ONLY`;
- parameter-bundle SHA-256:
  `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18`;
- bundle policy: `no_refit = true`.

Independent reproduction recovered the same optimizer estimate and interval
within the frozen `5e-12` tolerance. A third, Decimal/bisection path recovered
the scalar root within `6.5e-12` and the endpoints within `3.4e-16`.

## Dataset forensics

The development-manifest SHA-256 is
`2ccccde98363954b9167263cd54c20a9dd9068686ad382ed8388560559dfc87b`.
The sole objective row is
`BEST:zone=inner:published_aggregate_ratio`, value `0.791`, standard
uncertainty `0.05`, with source bindings:

- published BEST source transcription SHA-256
  `c9805ff757eb1c6f832b104f1eb043bb7e51b2c1a6711c0e1aa3737feed8f592`;
- prior public-result transcription SHA-256
  `7d49ab5f93e2d53b85755a602e21fe3a0a76ff3221c380549dba3a6e4de662ce`;
- excluded run-level file SHA-256
  `9bc2607b18aad11f5cd602cd547c3fe0f2052181386385247d819469c2fb3832`.

BEST outer, GALLEX/GNO, SAGE Cr51, SAGE Ar37, and BEST-2 are declared
holdouts and have `holdout_use_in_alpha_objective = false`. The objective uses
the frozen one-by-one `COV_DIAGONAL` matrix, no profiled nuisance parameter,
the bounded scalar optimizer, source-support-derived bounds, required
convergence/interiority/identifiability, and the frozen two-sided
`Delta chi2 = 1` interval construction. No post-fit scientific choice changed.

## Exposure classifications

- BEST inner: `MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`,
  `RETROSPECTIVE_NON_BLIND`, `DEVELOPMENT_DATA`;
- BEST outer, GALLEX/GNO, and SAGE: not used in the 6.5.0 objective, but
  historically exposed and not strict blind tests;
- BEST-2: `FUTURE_ONLY`, `FUTURE_BLIND`; observed data accessed **NO**;
  prediction generated **NO**.

## Permanent no-refit controls

The production evaluator contains no optimizer and takes one scalar
`alpha_0`. `PredictionInput.parse` requires the exact model profile, response,
cross-section scenario, source-line hash, and complete strict schema. For
`FROZEN_PARAMETER_BUNDLE`, it verifies the bundle file hash, exact frozen
value, and `no_refit=true`; a silent override fails closed.

Authorized source inputs must exactly match all canonical source-line IDs,
energies, and branching fractions. Tensor, axis, anisotropic amplitude,
directional, `beta_0`, quadratic, and second-coefficient keys are explicitly
forbidden. There is no experiment-, isotope-, zone-, run-, or exposure-level
parameter slot.

`execute_once` refuses to write if the result already exists. The pure
recalculation function and public reproduction tool can verify the frozen
result, but cannot replace it or authorize a second determination. Explicit
`PREFIT_AUTHORIZED_DEVELOPMENT` and `NON_PHYSICAL_TEST_FIXTURE` kinds are
limited to disclosed development/test contexts and cannot impersonate a
frozen bundle because they must carry a null bundle hash.

Searches found no alternate payload, spline, production response, parameter
sharing policy, or hidden tensor/axis activation path. Critical findings: **0**.

Verdict: `FROZEN_UNIVERSAL_ALPHA_NO_REFIT_FAIL_CLOSED`.
