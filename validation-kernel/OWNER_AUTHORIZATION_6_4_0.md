# LSC 6.4.0 Owner Authorization Package

Status: **OWNER AUTHORIZED ON 2026-08-16**

This package preserves the three scientific decisions established in STEP 07B and records the owner's explicit STEP 07C authorization. The Response-A candidates refined Decision 1; they were not a fourth hidden decision. This authorization is a new project decision and does not rewrite the earlier pending decision records.

## Decision 1

### Response

Canonical STEP 07B option: **Option A, physically derived transferable functions**.

Evidence result: E1-E12 do not uniquely derive a response function. Canonical 6.3.0 explicitly leaves `f0_a(E,t)` unfixed and preserves only the response slot and its normalized observable. A concrete 6.4.0 equation is therefore a `NEW_PHYSICAL_HYPOTHESIS_6_4_0`, not recovered 6.3.0 physics.

Authorized refinement: **`RESPONSE_A2_CAPTURE_ENERGY_DILATION`**.

Exact equation:

\[
F_{A2,m}(E)
=\left.\frac{\partial}{\partial\xi}\ln\sigma_m(Ee^\xi)\right|_{\xi=0}
=\frac{d\ln\sigma_m(E)}{d\ln E},
\]

\[
S_a(E,t)=\alpha_0F_{A2,m}(E),
\qquad
R_{\mathrm{pred},a}=1+\alpha_0\langle F_{A2,m}\rangle_a.
\]

Physical meaning: `alpha_0` is one universal signed logarithmic dilation of the incident-neutrino-energy argument of the conventional gallium capture cross section. Source activity, decay, line weights, geometry and detector efficiency remain conventional inputs and are not shifted.

Normalization: the logarithmic derivative fixes the scale. `alpha_0=d(ln E)` is dimensionless; arbitrary rescaling of `F_A2` is forbidden.

Domain:

- `E > 0`;
- the selected, versioned `sigma_m(E)` is positive and differentiable on an open neighborhood of every evaluated source line;
- currently supported isotope contracts are `51Cr` and `37Ar` on `71Ga`;
- `N0_a` is finite and strictly positive;
- `1 + alpha_0 F_A2,m(E) > 0` at every integration point;
- the preregistered linear-response tolerance is satisfied;
- all other cases fail closed as `FAIL_CLOSED_UNSUPPORTED_DOMAIN`.

Constants and external inputs: no numerical LSC constant is inserted. The cross-section function, all of its conventional constants, source-line data, version and SHA-256 must be frozen before parameter determination. Cross-section alternatives are preregistered scenarios; none may be chosen after observing an outcome.

Provenance classification:

- E1 measure and `Rpred=1+<S>`: `PRESERVED_FROM_LSC_BACKBONE` / `ALGEBRAICALLY_DERIVED`;
- gallium cross-section function: `CONVENTIONAL_EXTERNAL_PHYSICS`;
- logarithmic-derivative normalization: `NORMALIZATION_CONVENTION` tied to the physical definition of `alpha_0`;
- universal energy-dilation mechanism: `NEW_PHYSICAL_HYPOTHESIS_6_4_0`.

Alternatives retained for owner choice:

- `RESPONSE_A1_UNIVERSAL_SCALE`: `S_a=alpha_0`; executable and minimal, but prediction-equivalent to M1 constant normalization;
- `RESPONSE_A3_DETECTOR_ENERGY_DILATION`: `S_a=alpha_0 partial(ln epsilon0_a)/partial(ln E)`; detector-response aligned, but current radiochemical energy-response curves are absent and the effect can be degenerate with M4 systematics.

Full candidate definitions: [LSC_6_4_0_RESPONSE_A_CANDIDATES.json](spec/LSC_6_4_0_RESPONSE_A_CANDIDATES.json).

Owner selection required: **SATISFIED**

Owner selected candidate: **A2, capture-energy dilation, OWNER_AUTHORIZED**

## Decision 2

### Tensor

Authorized selection: **Option C, anisotropic sector disabled**.

Exact branch rule:

\[
B_a(E,t)=0.
\]

Consequences:

- no active anisotropic amplitude;
- no active physical tensor or preferred axis;
- no directional or sidereal claim;
- historical E3/E4/E11/E12 remain preserved as provenance but inactive in the 6.4.0 trace-only profile;
- T12 is not a claim of this profile.

Classification: `NEW_PHYSICAL_ASSUMPTION_6_4_0`.

Owner authorization required: **SATISFIED**

Owner selection: **C, OWNER_AUTHORIZED**

## Decision 3

### Sharing

Authorized selection: **Option A, universal cross-experiment sharing**.

Rule:

- one selected response equation;
- one `alpha_0` after its future freeze;
- zero experiment-specific or zone-specific LSC physical coefficients;
- experiment differences enter only through authoritative source, isotope, geometry, exposure and detector inputs;
- detector calibration and other experiment-specific effects remain nuisance parameters;
- no physical refit between experiments.

Classification: `NEW_PHYSICAL_ASSUMPTION_6_4_0`.

Owner authorization required: **SATISFIED**

Owner selection: **A, OWNER_AUTHORIZED**

## Authorization boundary

- model version: **LSC 6.4.0**;
- planned executable LSC 6.3.1: **`ABANDONED_BEFORE_RELEASE`**;
- owner authorization recorded: **YES, A2/C/A**;
- implementation authorized: **YES, subject to the cross-section and pre-fit gates**;
- parameter determination authorized: **CONDITIONAL ON ALL PRE-FIT GATES**;
- model execution authorized: **YES FOR HASH-VERIFIED SUPPORTED OR EXPLICIT NON-PHYSICAL INPUTS**;
- scientific validation authorized: **NO**;
- BEST-2 observed data accessed: **NO**;
- BEST-2 prediction generated: **NO**.

## Owner authorization

On 2026-08-16 the owner explicitly authorized the combined configuration **A2/C/A** and accepted A2 as `NEW_PHYSICAL_HYPOTHESIS_6_4_0`: universal logarithmic incident-energy dilation of the gallium capture-cross-section argument, first-order response about `alpha_0=0`, one frozen cross-section scenario, and transfer of one signed dimensionless `alpha_0` between supported experiments and isotopes without refit. The owner also authorized the tensor-off trace-only profile and universal sharing with no experiment- or zone-specific LSC physical coefficient.

This authorization does not claim that A2 was uniquely derived from LSC 6.3.0, does not authorize outcome-dependent changes, does not authorize a BEST-2 prediction, and does not authorize publication.

**OWNER AUTHORIZATION: OWNER_AUTHORIZED (A2/C/A)**
