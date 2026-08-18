# Phase-2 validation handoff

## Frozen identity

- Scientific model: LSC `6.5.0`, profile `EXACT_FINITE_A2/C/A`
- Model SHA-256:
  `c063aae4877159aa1ff2d0df4a8694988f587bc0cf68671357e711a136f7aab8`
- `alpha_0`: `-0.14388795521516184`
- Parameter-bundle SHA-256:
  `617d72a303a947e8e7467efb3c745f7e44dc1c07eab7d830a90dbfd179da5c18`
- Production-evaluator SHA-256:
  `ab195449e68da7d4b19e5dbd45079add4fee0e154666d63e30d9381a59dccd8f`
- Scientific-specification SHA-256:
  `114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948`
- Cross-section payload SHA-256:
  `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`
- Source-line payload SHA-256:
  `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`
- Parameter protocol SHA-256:
  `bf05812385439b0c82a53ed9bf52a26b65b6b8925903fab4f04e6d4d5a67a56c`

Every Phase-2 execution must verify these bindings before loading outcomes.
Any mismatch stops execution. `alpha_0` is universal and `no_refit=true`; no
experiment-, isotope-, zone-, run-, or exposure-specific fit is allowed. A
scientific response, payload, interpolation, domain, covariance, nuisance, or
parameter change requires a new model-development version and new freeze.

## Validation protocol

The preregistered primary fixed sequence remains:

`T11 -> T7 -> T3 -> T1 -> T10`

Family-wise alpha is `0.05`; stop at the first non-rejection, blocker, invalid
endpoint, or missing prerequisite. T2/T4/T6 are secondary descriptive tests;
T5/T8/T9 are sensitivity-only. STEP 08 executed none of these tests.

The available development covariance is `COV_DIAGONAL` with no profiled
nuisance parameter and classification `ASSUMPTION_BASED_SENSITIVITY_ONLY`.
Collaboration covariance/likelihood is unavailable. Phase 2 must not promote
this approximation to collaboration-equivalent inference.

## Exposure and validation roles

- BEST inner: `MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`,
  `RETROSPECTIVE_NON_BLIND`, `DEVELOPMENT_DATA`.
- BEST outer, GALLEX/GNO, SAGE 51Cr, SAGE 37Ar: absent from the 6.5.0 alpha
  objective, but historically model-exposed and not strict blind holdouts.
- BEST-2: `FUTURE_ONLY`, `FUTURE_BLIND`; observed data accessed **NO**;
  prediction generated **NO**.

## Known blocked mappings

The KATRIN and IceCube native data products do not have an independently
justified LSC mapping. They cannot confirm or exclude LSC until a mapping is
specified and frozen without outcome-driven selection. T12 remains outside
the production profile because LSC 6.5.0 disables anisotropy, tensor, and a
preferred axis; it must not be executed as a directional test.

## Execution authorization

This handoff states readiness only. A separate explicit Phase-2 authorization
is required before any observed holdout is loaded or any primary statistic is
computed. Preserve all input hashes, execution timestamps, blocker decisions,
and results whether favorable or adverse.
