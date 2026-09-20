# LSC 6.5.0 owner scientific authorization

Status: **OWNER AUTHORIZATION: APPROVED**

Authorization date: 2026-08-16

Authorized successor: **LSC 6.5.0 Exact Finite Dilation**

The owner understands that LSC 6.5.0 is specified after the preregistered LSC 6.4.0 linear A2 parameter-determination failure. LSC 6.4.0 remains an immutable adverse development result. The exact finite response is a separately versioned, post-6.4 physical successor and is not presented as a recovered 6.3.0 object, a 6.3.1 release, or a 6.4.1 patch.

## Decision 1 - exact finite response: OWNER_AUTHORIZED

The owner authorizes Candidate X: only the energy argument of the frozen gallium capture cross section is dilated.

Exact equations:

`E_sigma_prime = E exp(alpha_0)`

`K_m(E; alpha_0) = sigma_m(E exp(alpha_0)) / sigma_m(E)`

`S_m(E; alpha_0) = K_m(E; alpha_0) - 1`

`N_LSC,a(alpha_0) = integral_Da K_m(E; alpha_0) dnu_a`

`N0_a = integral_Da dnu_a`

`R_pred,a(alpha_0) = N_LSC,a(alpha_0) / N0_a = <K_m(E; alpha_0)>_a`

Null invariant:

`alpha_0 = 0 -> K_m = 1 -> S_m = 0 -> R_pred,a = 1`

`alpha_0` is the universal, signed, dimensionless logarithmic dilation `Delta ln E` of the capture-cross-section energy argument.

The following authoritative inputs are **not** dilated:

- stored source-line energies and source spectrum;
- source activity and decay law;
- conventional survival probability;
- detector response and efficiency;
- geometry, exposure, and time;
- nuisance parameters.

Candidate Y, dilation of the full forward model, is not authorized.

Classification: `NEW_PHYSICAL_HYPOTHESIS_6_5_0`, `NEW_POST_6_4_PHYSICAL_SUCCESSOR`, `POST_6_4_DEVELOPMENT`.

Scientific-specification binding:

- path: `spec/LSC_6_5_0_EXACT_DILATION_SPECIFICATION.yaml`;
- SHA-256: `114e8398a45e6a6c8fb4a105e994ca695805b06b9ed8608b86288ea0791ef948`;
- frozen cross-section scenario: `BAHCALL_1997_BEST_ESTIMATE_NATURAL_CUBIC_SPLINE`;
- cross-section payload SHA-256: `55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`;
- source-line payload SHA-256: `ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`;
- outside payload support: `FAIL_CLOSED_UNSUPPORTED_DOMAIN`.

## Decision 2 - tensor profile: OWNER_AUTHORIZED

Option C is authorized:

- anisotropic sector: `DISABLED`;
- tensor: `DISABLED`;
- preferred physical axis: `NONE`;
- anisotropic amplitude: absent;
- directional claim: absent;
- T12: outside the production LSC 6.5.0 profile.

## Decision 3 - sharing semantics: OWNER_AUTHORIZED

Option A is authorized:

- one universal response equation;
- exactly one physical LSC parameter, `alpha_0`;
- no experiment-, isotope-, zone-, exposure-, or run-specific LSC coefficient;
- experiment differences enter only through authoritative inputs and conventional nuisance parameters;
- after a successful freeze, `alpha_0` may not be refit between experiments.

## Data-exposure and adverse-result acknowledgement

1. BEST inner is permanently `MODEL_EXPOSED`, `POST_6_4_DEVELOPMENT`, `RETROSPECTIVE_NON_BLIND`, and `DEVELOPMENT_DATA` for this parameter determination.
2. BEST outer, GALLEX/GNO, and SAGE are excluded from the determination objective and retain their existing non-blind historical exposure classifications.
3. BEST-2 remains `FUTURE_ONLY` and `FUTURE_BLIND`; observed BEST-2 data are prohibited.
4. The frozen LSC 6.4.0 boundary result is not an initial value, parameter, domain constraint, or successful result for LSC 6.5.0.
5. The response, payload, domain, protocol, and data role must be frozen before the single authorized determination.
6. Any adverse LSC 6.5.0 determination must be preserved without changing this hypothesis after exposure.

OWNER AUTHORIZATION: **APPROVED**

Scientific decisions authorized: **A2-exact / C / A**

Implementation authorized subject to hash-bound gates: **YES**

Single parameter determination authorized subject to a passing pre-fit audit: **YES**

BEST-2 prediction authorized: **NO**

Publication authorized: **NO**
