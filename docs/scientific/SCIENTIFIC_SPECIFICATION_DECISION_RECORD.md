# STEP 07A Scientific Specification Decision Record

## Decision summary

The 17 STEP 07 unresolved objects separate into three groups:

1. representational issues that STEP 07A resolves by gauge, normalization, coordinate, or algebraic choices;
2. empirical validation objects that do not define the LSC physical model;
3. response-function and tensor choices that remain new physical content.

Because a complete model necessarily requires group 3, the successor must be versioned as 6.4.0 under the user-supplied version rule.

## Blocker-by-blocker adjudication

| Blocker | Evidence and derivation | Classification | Resolved? | Resolution | Physical consequence | Version consequence |
|---|---|---|---:|---|---|---|
| `theta` | Original source separates LSC `theta` from nuisance `eta`; E10 does the same | `COORDINATE_CONVENTION` | PARTIAL | `theta` is only the ordered physical successor vector; `eta` remains external | avoids double-counting nuisances | no escalation by itself |
| parameter ordering | ordering has no effect if names and hashes bind values | `COORDINATE_CONVENTION` | PARTIAL | order invariant fields before model-specific coefficients; final list waits for owner choices | serialization only | no escalation |
| `lambda0` | only `lambda0*f0_a` occurs | `PURE_GAUGE_CHOICE` | YES | replace with `S_a=lambda0*f0_a` | removes scale/sign redundancy | 6.3.1-capable formalization |
| `lambdaA` | only the product with `fA_a*A_a` occurs | `PURE_GAUGE_CHOICE` | YES | replace with `B_a=lambdaA*fA_a*A_a` | removes scale/sign redundancy | 6.3.1-capable formalization |
| `f0_a` | exact form explicitly not frozen; E8 sees only a weighted functional | `UNRESOLVED_PHYSICAL_CHOICE` | NO | owner must supply a transferable physical form or choose a restricted moment model | determines energy/time and transfer predictions | new form requires 6.4.0 |
| `fA_a` | exact form explicitly not frozen; E8 sees only a `q`-weighted functional | `UNRESOLVED_PHYSICAL_CHOICE` | NO | owner must supply a transferable physical form or choose a restricted moment model | determines directional energy/time response | new form requires 6.4.0 |
| active tensor components | E4 fixes STF structure but no component values/eigenvalue shape | `UNRESOLVED_PHYSICAL_CHOICE` | NO | choose uniaxial, general STF, or anisotropy-off option | changes anisotropic prediction space | requires 6.4.0 |
| tensor orientation | physical orientation explicitly not frozen | `UNRESOLVED_PHYSICAL_CHOICE` | NO | supply an a-priori ICRS orientation from a physical hypothesis | sets directional phase and transfer prediction | requires 6.4.0 |
| complete reference frame | ICRS/lab roles are known, physical axis and full transforms are not | `COORDINATE_CONVENTION` | PARTIAL | standardize coordinate chain; owner supplies physical tensor direction; experiment supplies surveyed orientation/time inputs | separates coordinate choice from physical alignment | physical direction requires 6.4.0 |
| complete units | E2 fixes only multiplicative product dimensions | `NORMALIZATION_CONVENTION` | YES AT INVARIANT LEVEL | `S_a` and `B_a` are dimensionless; model inputs must be explicitly converted to canonical units | removes unit gauge without choosing response shape | no escalation by itself |
| `eta` | original source defines source/cross-section/geometry/extraction/normalization nuisances | `EMPIRICAL_PARAMETER` | OUTSIDE MODEL | retain in likelihood registry and dataset execution manifest | affects inference, not model identity | no model-version escalation |
| covariance | E10 requires empirical ratio-space covariance | `EMPIRICAL_PARAMETER` | OUTSIDE MODEL | authoritative dataset object; sensitivity scenarios remain labelled | blocks strong inference but not model definition | no model-version escalation |
| numerical configuration | binding and normalization can be formalized; physical fields cannot | `COORDINATE_CONVENTION` | PARTIAL | use exact ratio binding and normalized measure; wait for owner model choices | prevents hidden defaults | no escalation for technical fields |
| parameter bounds | no final bounds exist and phenomenological coefficients may require development | `EMPIRICAL_PARAMETER` | NO | preregister theory/calibration bounds or a historical development protocol | defines admissible parameter region | tied to 6.4.0 parameterization |
| numerical defaults | quadrature/tolerance follow only after measure/domain are fixed | `NORMALIZATION_CONVENTION` | PARTIAL | one normalized denominator; implementation tolerances deferred | numerical only after scientific contract | no escalation by itself |
| frozen prediction table | derived output, not an independent physical parameter | `ALGEBRAICALLY_IMPLIED` | NOT APPLICABLE NOW | generate only after a complete frozen model and authorized inputs exist | cannot repair missing model semantics | no independent version effect |
| executable evaluator inputs | geometry, exposure, timing, source and detector metadata are experiment objects | `EMPIRICAL_PARAMETER` | OUTSIDE MODEL | bind through immutable dataset contracts | controls which components can execute | no model-version escalation |

## Additional scientific adjudications

| Issue | Evidence and derivation | Classification | Resolved? | Resolution | Version consequence |
|---|---|---|---:|---|---|
| tensor dimension | five independent STF components imply `d(d+1)/2-1=5` | `ALGEBRAICALLY_IMPLIED` | YES | `d=3` | no escalation |
| tensor scale | exact degeneracy with anisotropic amplitude/function | `NORMALIZATION_CONVENTION` | YES | Frobenius norm one on the nonzero branch | no escalation |
| tensor sign | exact discrete degeneracy after factorization | `PURE_GAUGE_CHOICE` | YES | canonical component sign with compensation in signed response | no escalation |
| tensor sharing | E3 uses `A_a`; E12 omits the index | `UNRESOLVED_PHYSICAL_CHOICE` | NO | owner chooses shared, geometry-derived, or independent tensors | 6.4.0 |
| E8 denominator | E6 ratio plus E1/E5 algebra require baseline normalization | `ALGEBRAICALLY_IMPLIED` | YES | divide by `N0_a` | no escalation |
| E5/E7 to E10 binding | exact E5/E1 ratio equals `1+` E7 residual under normalized E8 | `ALGEBRAICALLY_IMPLIED` | YES | Binding A: `Rpred=NLSC/N0`; E7 is residual diagnostic | no escalation |
| integration domain and weights | factor roles are source-defined but exact experiment objects are external | `EMPIRICAL_PARAMETER` | PARTIAL | one baseline measure; authoritative dataset supplies domains and factors | no model escalation |
| response functional reduction | exact only for a fixed measure, not across new measures | `PHYSICALLY_EQUIVALENT_REPARAMETERIZATION` | LIMITED | permitted for fixed-design diagnostics only | full replacement changes prediction space and requires 6.4.0 |
| frame basis | passive orthogonal basis changes leave `n^T A n` invariant | `COORDINATE_CONVENTION` | YES IN PRINCIPLE | freeze one ICRS to Earth-fixed to lab chain | no escalation |
| physical preferred direction | rotating tensor relative to ICRS changes predictions | `NEW_PHYSICAL_ASSUMPTION` | NO | owner must state the physical hypothesis before validation | 6.4.0 |

## Alternative observable bindings

| Binding | Definition | Equivalent to preserved equations? | Additional assumption | Required version |
|---|---|---:|---|---|
| `BINDING_A` | `Rpred=NLSC/N0` | YES | normalized E1 measure and positive denominator | preserved formalization; selected |
| `BINDING_B` | `Rpred=1+DeltaR` | YES only when E7 is derived from E2/E5/E8 | explicit approximation/equality policy | same as A only under proved equivalence |
| `BINDING_C` | count-space likelihood using `NLSC` | NO | new observable and covariance law | at least 6.4.0 |

`BINDING_A` is selected without fit quality. It is the unique binding that makes E10's prediction coordinate match E6's observed ratio while preserving E1-E5.

## Option-space recommendation

| Option | Minimal assumptions | Effective parameter count | Identifiability | Falsifiability | Equations changed? | Prediction space changed? | Version |
|---|---|---:|---|---|---:|---|
| O1: trace-only fixed template | one physically justified normalized scalar shape | 1 amplitude | conditional; aliases normalization if shape is constant | moderate with transfer data | active subset only | YES, anisotropy removed | 6.4.0 restricted M5 |
| O2: fixed scalar plus shared uniaxial anisotropy | two fixed response shapes and one a-priori physical axis | 2 amplitudes if axis is fixed | best available full trace/traceless option | strongest among finite options | symbolic E1-E12 retained with specified subfamily | YES, unrestricted family reduced | 6.4.0 |
| O3: general/flexible tensor-function family | arbitrary functions and general shared or per-zone STF tensors | at least 6 plus function-shape degrees; potentially infinite | poor with current aggregate data | weak without strong external structure | symbolic form retained | explicitly enlarged/selected | 6.4.0 and not recommended |

O2 is recommended on structural criteria if the project owner can supply a defensible, pre-data axis and response mechanism. O1 is the fallback when no anisotropic physical hypothesis exists. O3 is not recommended.

## Version decision

The gauge, units, dimension, normalized integration, and observable binding are representational or algebraic. They could have remained a patch-level formalization.

The missing response forms and tensor physical hypothesis cannot. Completing them changes the transferable prediction space and meets the explicit STEP 07A triggers for a new functional form, tensor semantics, and preferred-direction assumption.

**Verdict: `VERSION_ESCALATION_REQUIRED_6_4_0`.**

There is no evidence that the detector-response model class itself must be replaced, so 7.0 is not warranted.
