# STEP 07B.1 RESULT

Project: **LSC Validation Kernel**

Status: **PASS**

Response-closure verdict: **`RESPONSE_A_NEW_PHYSICAL_HYPOTHESIS_OPTIONS_READY`**

## Executive result

The preserved E1-E12 backbone determines where a scalar response enters and how it is averaged, but it does not determine its functional form. The active 6.3.0 sources explicitly leave `f0_a(E,t)` physically unfixed. Historical 5.x material supplies an energy-reconstruction motivation and a logarithmic-sensitivity expansion, but canonical lineage retains only detector-response language and removes the old standalone energy-map mechanism. Therefore no response can honestly be classified as uniquely physically derived from the frozen model.

STEP 07B.1 closes this gap without fitting by defining three finite, transferable and falsifiable 6.4.0 candidates. The recommended owner choice is `RESPONSE_A2_CAPTURE_ENERGY_DILATION`, a one-parameter universal logarithmic energy-dilation response using a versioned conventional gallium capture cross section. It is a new 6.4.0 physical hypothesis, not recovered 6.3.0 content. Owner selection remains mandatory.

No fit, prediction, T1-T12 execution, BEST-2 observation access, publication or push occurred.

## A. Response physical meaning

The preserved trace-only response is

\[
\epsilon_{\mathrm{LSC},a}(E,t,\Omega)
=\epsilon_{0,a}(E,t,\Omega)\,[1+S_a(E,t)].
\]

Here:

- `a` is an analysis bin or detector zone established by an authoritative dataset contract;
- `E` is incident neutrino energy;
- `t` is physical exposure time;
- `S_a` is a dimensionless local multiplicative response;
- the inactive anisotropic branch carries all directional dependence, so active scalar `S_a` has no `Omega` argument.

The conventional measure is

\[
d\nu_a=\Phi P_{\alpha\beta}\sigma\epsilon_{0,a}W_a\,dE\,d\Omega\,dt,
\qquad
N_{0,a}=\int_{D_a}d\nu_a.
\]

With the STEP 07A binding,

\[
R_{\mathrm{pred},a}=\frac{N_{\mathrm{LSC},a}}{N_{0,a}}
=1+\langle S_a\rangle_a,
\qquad
\langle g\rangle_a=\frac{\int_{D_a}g\,d\nu_a}{N_{0,a}}.
\]

This establishes local versus integrated semantics: `S_a` is local, while only its normalized E1-weighted moment reaches the final rate ratio.

## B. Equation-first derivation

### What follows algebraically

1. Setting the anisotropic response to zero reduces E2 to `epsilon_LSC=epsilon0(1+S)`.
2. Substituting this into E5 gives `N_LSC=N0+integral(S dnu)`.
3. Dividing by `N0` gives `Rpred=1+<S>`.
4. The old `lambda0*f0_a` factorization has an exact scale and sign gauge, so the observable object is `S_a` itself.
5. Dimensional consistency requires `S_a` dimensionless.

### What does not follow

No E1-E12 equation selects whether `S_a` is constant, energy-dependent, time-dependent, cross-section-derived or detector-response-derived. Normalization removes only a scale redundancy; it cannot choose a shape. The null space of the weighted integral also means infinitely many distinct local functions have the same observed moment on one dataset contract.

**Equation-first verdict:** the backbone supplies the response slot and observable map, not an exact Response-A equation.

## C. Physics-first derivation

The active canonical core frames LSC as detector-response phenomenology and explicitly keeps detector systematics as a competitor. It contains no microphysical scalar source. Historical material offers two relevant ideas:

1. a universal multiplicative or effective normalization shift;
2. a small energy-reconstruction shift whose rate effect is the logarithmic derivative of a conventional response kernel.

Neither survives as a complete active physical mechanism. A constant response is indistinguishable from the M1 normalization baseline. An energy-dilation response is more transferable and discriminating, but selecting which conventional function receives the dilation is itself new physical content. The three candidates below make those choices explicit rather than hiding them in implementation.

**Physics-first verdict:** a complete response requires a new explicit 6.4.0 hypothesis.

### Conventional physics separation

| Object | Role in the recommended A2 closure |
|---|---|
| source activity and radioactive decay | conventional `Phi` input; never part of LSC response |
| neutrino line energies and branching fractions | authoritative source-spectrum input |
| oscillation/survival factor | conventional `P_alpha_beta` input |
| `71Ga` capture cross section `sigma_m(E)` | versioned conventional external physics whose logarithmic sensitivity is evaluated |
| baseline detector efficiency `epsilon0_a` | conventional detector input; not dilated in A2 |
| geometry, volume and exposure weighting `W_a` | conventional experiment input |
| extraction, counting and calibration uncertainty | nuisance policy, not LSC physics |
| `alpha_0` and the declaration that it dilates the cross-section energy argument | the new LSC 6.4.0 physical hypothesis |

This separation prevents Response A from silently duplicating source activity, standard decay, line weights, detector efficiency or geometry.

## D. Historical candidates

| Source | Candidate content | Exposure/provenance | Compatibility | Adjudication |
|---|---|---|---|---|
| Active E1-E12 (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_ACTIVE_EQUATION_SET.md`; archival evidence path, not redistributed) | `lambda0 f0_a`, E1 weighting, E7/E8 moments | authentic frozen symbolic source | defines the slot, not the function | reusable backbone only |
| Canonical core (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_CANONICAL_CORE.md`; archival evidence path, not redistributed) | `f0_a(E,t)` explicitly not physically fixed | authentic frozen negative evidence | proves non-uniqueness | blocker, not equation |
| Historical lineage (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_HISTORICAL_LINEAGE.md`; archival evidence path, not redistributed) | 5.x energy reconstruction as historical bridge | canonical source | old standalone energy map removed | historical reference only |
| LSC 5.5 hard mathematics (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/historical_archive/pre_step5_repository/LSC_core/simulations/legacy/lsc55/LSC55_Hard_Mathematics_2026-04-25.md`; archival evidence path, not redistributed) | `Delta N/N` from a logarithmic rate-kernel slope | historical, not active 6.3.0; no unique scalar mechanism | motivates A2/A3 algebra | historical reference only |
| LSC 6.0 theory (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/historical_archive/pre_step5_repository/legacy/LSC-6.0/docs/THEORY_LSC_6_0.md`; archival evidence path, not redistributed) | effective `delta_G` / scalar response | historical and phenomenological | no physical generator | not promotable |
| LSC 6.0 toy (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/historical_archive/pre_step5_repository/legacy/LSC-6.0/simulations/lsc60_gallium_response.py`; archival evidence path, not redistributed) | fixed amplification and BEST-scale scenarios | post-data toy | violates no-fit closure | quarantined |
| LSC 6.2 preprint (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/historical_archive/pre_step5_repository/legacy/LSC-6.0/releases/LSC_6.2.0_preprint/source/main.tex`; archival evidence path, not redistributed) | illustrative `delta` magnitude | historical illustrative value | not a physical function | quarantined |
| Hostile physics audit (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/audits/extracted/LSC_Physics_Audit_2026-05-25.md`; archival evidence path, not redistributed) | requires explicit `f0`; rejects naive `sigma proportional E^2` | independent freeze-era audit | supports fail-closed closure | methodological evidence |
| Elliott-Gavrin-Haxton 2023 source (`../../LSC_6_3_0_VALIDATION/05_GALLIUM_CROSS_SECTIONS/Papers/source_2303.13623/CS_paper_v10.tex`; archival evidence path, not redistributed) | line energies and an explicit conventional gallium cross-section construction | external conventional physics; DOI `10.1103/PhysRevC.108.035502` | can supply a versioned `sigma_m`, not an LSC mechanism | candidate external input |

No historical fit coefficient, toy amplification or illustrative value was promoted.

## E. Candidate equations

Machine-readable definitions: [LSC_6_4_0_RESPONSE_A_CANDIDATES.json](../../spec/LSC_6_4_0_RESPONSE_A_CANDIDATES.json).

Because no unique backbone-derived equation exists, `spec/LSC_6_4_0_RESPONSE_A.yaml` was intentionally **not** created. The candidate-set artifact is the fail-closed alternative required by the task.

### A1: universal fractional response scale

\[
F_{A1,a}(E,t)=1,
\qquad
S_a(E,t)=\alpha_0,
\qquad
R_{\mathrm{pred},a}=1+\alpha_0.
\]

This is complete and maximally transferable. It is also prediction-equivalent to the M1 constant-normalization model and can be degenerate with common normalization nuisances. It is retained as an explicit nested control, not recommended as a scientifically distinct LSC closure.

### A2: universal gallium-capture energy dilation

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

`sigma_m` is a positive, differentiable, versioned conventional `71Ga` capture cross-section function. The source spectrum, decay, geometry and detector efficiency are not shifted. The equation is the exact linear-response coefficient for an infinitesimal logarithmic energy dilation; it is not a claim that finite nonlinear remapping has been derived.

**Recommendation:** A2, subject to owner selection and freezing a differentiable cross-section implementation before parameter determination.

### A3: universal detector-response energy dilation

\[
F_{A3,a}(E,t)
=\left.\frac{\partial}{\partial\xi}\ln\epsilon_{0,a}(Ee^\xi,t)\right|_{\xi=0}
=\frac{\partial\ln\epsilon_{0,a}(E,t)}{\partial\ln E},
\]

\[
S_a(E,t)=\alpha_0F_{A3,a}(E,t),
\qquad
R_{\mathrm{pred},a}=1+\alpha_0\langle F_{A3,a}\rangle_a.
\]

This is closest to detector-response language, but it requires positive differentiable energy-resolved efficiency curves that are absent for the archived radiochemical datasets. It is also at risk of observational equivalence with M4 detector systematics.

### Comparison without fit quality

| Criterion | A1 | A2 | A3 |
|---|---|---|---|
| New physical amplitudes | 1 | 1 | 1 |
| Additional shape coefficient | 0 | 0 | 0 |
| Identifiable after nuisance freeze | weak; M1-degenerate | conditional, one-dimensional | conditional; M4-degenerate |
| Cross-zone transfer | exact | exact | through authoritative `epsilon0_a` |
| Cross-isotope discrimination | none | yes, through source energies and `sigma_m` | only through detector input |
| Required missing external input | none | differentiable versioned `sigma_m` | energy-resolved `epsilon0_a` |
| Distinctive falsifiability | low | highest | conditional |
| BEST-2 schema | capable | capable after cross-section/input freeze | capable only with response curve |
| Recommendation | nested control | **recommended** | retained alternative |

No candidate was compared against an observed residual or chi-square.

## F. Normalization

The old `lambda0*f0` scale/sign freedom is removed by giving `alpha_0` a direct physical meaning:

- A1: fractional response change, with `F=1`;
- A2: logarithmic incident-energy dilation `d(ln E)`;
- A3: logarithmic detector energy-axis dilation `d(ln E)`.

For A2 and A3, the logarithmic derivative fixes the template scale. A transformation `F -> cF`, `alpha_0 -> alpha_0/c` would change the stated meaning of `alpha_0` and is prohibited after owner selection. Normalization never uses an observed rate.

## G. Domain

All candidates require a finite positive `N0_a`. Candidate-specific rules are machine-readable in the candidate set.

- A1 supports positive-energy inputs in any authoritative dataset domain.
- A2 supports `51Cr` and `37Ar` gallium-capture lines only where the frozen `sigma_m(E)` is positive and differentiable in a neighborhood of each line.
- A3 supports only domains with a positive, differentiable, versioned `epsilon0_a(E,t)`.
- No candidate adds intrinsic scalar time dependence. Source decay and exposure weighting stay in the conventional E1 measure.
- An unsupported isotope, missing function, nonpositive baseline, nondifferentiable evaluation point or violation of positivity/linear-response conditions returns `FAIL_CLOSED_UNSUPPORTED_DOMAIN`.

## H. Units and constants

- energy: MeV at interfaces;
- exposure intervals: seconds;
- `S_a`, `F_a`, `alpha_0`, `Rpred_a`: dimensionless;
- logarithmic derivatives: unit-invariant;
- A1 constant: exact `1`;
- A2 conventional constants: owned by the versioned cross-section model and not copied into LSC as free constants;
- A3 has no LSC constant but requires a versioned detector-response function.

The current cross-section registry contains model totals and uncertainties but not a differentiable function for every model. STEP 07C must package or implement a selected authoritative function with source/version/hash; it may not infer slopes from the two isotope totals.

## I. Provenance

| Component | Class |
|---|---|
| E1 measure, E2 response slot, E5 integral, E8 normalized average | `PRESERVED_FROM_LSC_BACKBONE` |
| `Rpred=NLSC/N0=1+<S>` | `ALGEBRAICALLY_DERIVED` |
| source line data, `sigma_m`, `epsilon0_a` | `CONVENTIONAL_EXTERNAL_PHYSICS` / authoritative experiment input |
| direct physical meaning of `alpha_0` and the resulting template scale | `NORMALIZATION_CONVENTION` within a selected mechanism |
| A1, A2 or A3 mechanism selection | `NEW_PHYSICAL_HYPOTHESIS_6_4_0` |
| Tensor C and Sharing A | `NEW_PHYSICAL_ASSUMPTION_6_4_0` |

The 2023 cross-section paper is an authoritative conventional source for gallium capture calculations and source-line treatment; it does not validate or derive the LSC energy-dilation hypothesis. [APS record](https://doi.org/10.1103/PhysRevC.108.035502).

## J. Remaining new assumptions

The owner must still select one A1/A2/A3 mechanism under canonical Response Option A. For the recommended A2, the owner accepts that:

1. one universal scalar acts as a logarithmic incident-energy dilation;
2. only the conventional gallium capture cross-section argument is dilated;
3. the theory is linear response around `alpha_0=0`;
4. a versioned cross-section scenario is frozen before determination;
5. the same `alpha_0` transfers without refit.

These are not gauge, coding defaults or recovered 6.3.0 statements.

## K. `alpha_0` definition

Each candidate has exactly one physical amplitude. Under recommended A2:

- meaning: signed logarithmic incident-energy dilation;
- units: dimensionless;
- sign: positive samples `sigma_m` at higher energy;
- value: not selected;
- uncertainty: not selected;
- numerical bounds: not selected;
- determination preference: independent theory or calibration, otherwise one preregistered retrospective development objective;
- historical-data label if used: `RETROSPECTIVE_NON_BLIND_MODEL_EXPOSED`;
- refit between experiments: prohibited;
- BEST-2 observed data: prohibited.

Future determination contract: [LSC_6_4_0_ALPHA0_DETERMINATION_CONTRACT.json](../../LSC_6_4_0_ALPHA0_DETERMINATION_CONTRACT.json).

No determination may begin before owner selection, response/domain/normalization hashes, numerical bounds, objective, development-data manifest and statistical policy are frozen.

## L. Tensor decision

**Option C: anisotropic sector disabled.**

`B_a(E,t)=0`; no active tensor, anisotropic amplitude, preferred axis or directional claim exists in the production branch. Historical tensor equations remain unchanged in provenance. T12 is not a claim of this trace-only 6.4.0 profile.

## M. Sharing decision

**Option A: universal cross-experiment law.**

The selected equation and frozen `alpha_0` apply to all zones, exposures, experiments and supported isotopes without physical refit. Differences enter through authoritative E1 inputs and nuisance parameters only. No observation-, zone- or experiment-specific LSC coefficient exists.

## N. BEST-2 prospective compatibility

- status: `FUTURE_ONLY`;
- blindness: `FUTURE_BLIND`;
- observed BEST-2 data accessed: **NO**;
- prediction generated: **NO**;
- candidate-set schema: `PROSPECTIVE_SCHEMA_CAPABLE`;
- recommended A2: conditional on a frozen differentiable `sigma_m`, authoritative as-built source/geometry/exposure/detector inputs, a frozen `alpha_0`, and a prediction artifact created before observed data access.

No BEST-2 value or residual informed the recommendation.

## O. Owner authorization document

[OWNER_AUTHORIZATION_6_4_0.md](../../OWNER_AUTHORIZATION_6_4_0.md) contains exactly the three decisions:

1. Response Option A refined to an owner selection among A1/A2/A3, with A2 recommended;
2. Tensor Option C;
3. Sharing Option A.

`OWNER AUTHORIZATION: PENDING`.

## P. Implementation contract status

- `owner_authorized=false`;
- `ready_for_implementation=false`;
- candidate equation package present: **YES**;
- unique owner-selected equation present: **NO**;
- parameter determination authorized: **NO**;
- model execution authorized: **NO**.

The implementation contract is hash-bound to the candidate set and alpha determination contract. STEP 07C remains closed until the owner records all three selections and the selected A2 external-function payload and parameter bounds are frozen.

## Q. Tests

Final receipts are recorded after validation:

- STEP 07B.1 response tests: **15/15 PASS**, plus **3/3 parameterized subtests**;
- STEP 07B + STEP 07B.1 combined regression: **31/31 PASS**, plus **3/3 parameterized subtests**;
- full software suite: **207/207 PASS**, plus **21/21 parameterized subtests**;
- candidate equation AST parsing: **PASS**;
- dimensional and deterministic normalization checks: **PASS**;
- analytical nonphysical log-derivative controls (`E^2 -> 2`, `E^3 -> 3`): **PASS**;
- finite one-parameter count: **PASS**;
- universal-sharing/no per-experiment coefficient guard: **PASS**;
- tensor-disabled/no-axis guard: **PASS**;
- unsupported-domain fail-closed guard: **PASS**;
- no-fit/no-prediction/BEST-2 untouched guard: **PASS**;
- implementation-contract response hash bindings: **PASS**;
- preserved archive SHA-256: **1,882/1,882 PASS**;
- nested repositories: **4/4 clean**, expected HEADs, `git fsck` **PASS**;
- outer `git diff --check`: **PASS**;
- publication-path scan: **PASS, 0 findings**;
- historical 6.3.0 HEAD/tree/equation hash: **PASS**.

## R. Git state

- input branch: `main`;
- input HEAD: `8e5162ab398cd5b5b12b85569daa75b857d39a89`;
- intended commit: `Step 07B.1: close LSC 6.4.0 scalar response specification`;
- push: **NO**;
- tag: **NO**;
- publication: **NO**;
- final commit and clean-worktree receipt: reported after commit.

## S. Next readiness

**READY FOR OWNER AUTHORIZATION: YES**

**READY FOR STEP 07C AFTER OWNER AUTHORIZATION: YES**

Conditions:

1. owner chooses A1, A2 or A3 under Decision 1 and accepts Decisions 2 and 3;
2. STEP 07C begins by freezing the selected external function, candidate-specific bounds and linear-response tolerance before any parameter determination;
3. the pre-fit determination contract is completed before any fit;
4. the implementation contract is regenerated with `owner_authorized=true` only after those receipts exist.

The remaining ambiguity is physical, not representational: E1-E12 do not select which conventional response receives the universal scalar dilation.
