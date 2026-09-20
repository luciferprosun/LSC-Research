# LSC STEP 07A Gauge and Identifiability Analysis

## Technical result

The amplitude symbols in E2 are not separately physical. The exact equation-preserving objects are

\[
S_a(E,t)=\lambda_0 f_{0,a}(E,t),
\qquad
B_a(E,t)=\lambda_A f_{A,a}(E,t)A_a,
\]

so that

\[
\epsilon_{\mathrm{LSC},a}
=\epsilon_{0,a}\left[1+S_a+n^{T}B_an\right].
\]

Replacing the factorized aliases by `S_a` and `B_a` is a
`PHYSICALLY_EQUIVALENT_REPARAMETERIZATION`: it removes scale and sign gauges and does not change a prediction. It does **not** determine either response field. Their functional shapes, tensor sharing rule, tensor eigenvalue shape, and physical orientation remain genuine scientific choices.

Consequently, the remaining ambiguity is not merely representational. Gauge reduction is possible, but a complete transferable LSC model still requires new physical assumptions.

## Evidence boundary

This adjudication uses the preserved sources below. No experimental result is used to select a model choice.

| Source | Relevant content |
|---|---|
| Active E1-E12 equation set (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_ACTIVE_EQUATION_SET.md`; archival evidence path, not redistributed) | E1-E12, variable roles, source classifications |
| Canonical core (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_CANONICAL_CORE.md`; archival evidence path, not redistributed) | detector-response scope, five-parameter tensor warning, validation intent |
| Freeze boundary (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/canonical/LSC_FREEZE_BOUNDARY.md`; archival evidence path, not redistributed) | functions, orientation, bounds, covariance and predictions explicitly not frozen |
| Original unified 6.3.0 source (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/historical_archive/pre_step5_repository/LSC_core/theory/LSC-6.3.0/LSC_6_3_0_UNIFIED_BEST2_UPDATE.md`; archival evidence path, not redistributed) | original model and `theta`/`eta` definitions |
| Physics audit (`../../LSC_6_3_0_VALIDATION/01_LSC_FROZEN_REFERENCE/LSC-Research/audits/extracted/LSC_Physics_Audit_2026-05-25.md`; archival evidence path, not redistributed) | underidentification and requirement for a-priori functions/orientation |
| [Recovered dependency graph](../../frozen_core/equations/equation_dependency_graph.json) | E5/E7 to E10 were previously unverified |

## Independent double adjudication

### Path 1: equation-first

Starting with E1-E5, define

\[
d\nu_a(x)=
\Phi P_{\alpha\beta}\sigma\epsilon_{0,a}W_a
\,dE\,d\Omega\,dt,
\qquad
N_{0,a}=\int_{D_a}d\nu_a.
\]

Direct substitution of E2 and E3 into E5 gives

\[
N_{\mathrm{LSC},a}
=N_{0,a}+\int_{D_a}
\left[S_a(E,t)+n^TB_a(E,t)n\right]d\nu_a.
\]

Only `S_a`, `B_a`, the baseline measure, and the integration domain enter. The separate amplitudes, functions, and tensor scale do not.

### Path 2: observable-first

E10 requires `R_pred` in the same coordinates as E6's dimensionless observed ratio. Working backward therefore gives

\[
R_{\mathrm{pred},a}=\frac{N_{\mathrm{LSC},a}}{N_{0,a}}
=1+\langle S_a\rangle_a+\langle n^TB_an\rangle_a,
\]

where

\[
\langle g\rangle_a=
\frac{\int_{D_a}g\,d\nu_a}{\int_{D_a}d\nu_a}.
\]

The observable therefore contains only weighted functionals and tensor contractions. It cannot identify pointwise response functions or tensor components outside the experimental design span.

### Reconciliation

Both paths produce the same minimal invariant model: `S_a`, `B_a`, `dnu_a`, and the normalized ratio. They also produce the same null spaces and parameter-count conclusion. The independent-double-adjudication result is **PASS**.

## Exact scale, sign, and coordinate gauges

Let there be `m` zones and take E3 literally as zone-indexed. On the generic nonzero stratum, the scale gauge is

\[
G_{\mathrm{scale}}\cong(\mathbb{R}^{\times})^{m+2}.
\]

For nonzero `c0`, `cA`, and `d_a`, its action is

\[
\lambda'_0=c_0\lambda_0,
\qquad
f'_{0,a}=c_0^{-1}f_{0,a},
\]

\[
\lambda'_A=c_A\lambda_A,
\qquad
f'_{A,a}=d_af_{A,a},
\qquad
A'_a=(c_Ad_a)^{-1}A_a.
\]

Negative factors prove the corresponding sign degeneracies. At a zero amplitude, function, or tensor, the stabilizer is larger and identifiability is weaker.

For one globally shared tensor, the independent zone factors `d_a` are no longer available; two global anisotropic scale factors remain. Choosing global versus zone-indexed tensors is not a gauge choice because it changes cross-zone predictions.

There is also a passive coordinate gauge. For any orthogonal change of basis `Q`,

\[
n'=Qn,
\qquad
A'_a=QA_aQ^T,
\qquad
n'^TA'_an'=n^TA_an.
\]

This permits a coordinate convention but cannot select a physical preferred orientation relative to ICRS or the detector.

## Canonical gauge-free parameterization

The recommended scientific notation is:

- `S_a(E,t)`: dimensionless scalar response field;
- `B_a(E,t)`: dimensionless symmetric traceless 3-by-3 tensor-response field;
- `dnu_a`: baseline experiment measure;
- `rho_a(E,t,Omega) = S_a + n^T B_a n`: total fractional detector response.

To preserve the factorization of E2-E3, write

\[
B_a(E,t)=h_{A,a}(E,t)T_a,
\]

where `T_a` is independent of energy and time. On the nonzero anisotropic branch, a convenient representative is

\[
\|T_a\|_F=1,
\qquad
h_{A,a}=\lambda_A f_{A,a}\|A_a\|_F.
\]

The invariant `B_a` remains primary. `lambda0`, `lambdaA`, `f0_a`, `fA_a`, and the unnormalized `A_a` may remain only as historical aliases until an explicit factorization is scientifically specified.

## `f0_a` and `fA_a` semantics

### Source-derived content

- `a` is an analysis bin or detector zone.
- Both functions have domain `(E,t)` and no explicit angular argument.
- `f0_a` contributes to the scalar detector response.
- `fA_a` multiplies the directional contraction `q_a`.
- Their codomain is scalar, but their individual units are gauge-dependent.
- Their exact form, normalization, parameter count, and physical derivation are not frozen.

### What a fixed observation can identify

For one fixed normalized measure `mu_a`, E8 sees only

\[
L_{0,a}[S]=\int S_a\,d\mu_a,
\qquad
L_{A,a}[B]=\int n^TB_an\,d\mu_a.
\]

The scalar null space is

\[
\ker L_{0,a}=\{h:\int h\,d\mu_a=0\}.
\]

For a fixed factorized tensor, the anisotropic functional null space contains every `h` satisfying

\[
\int q_a h\,d\mu_a=0.
\]

Thus a fixed aggregate rate does not identify either full function.

### Functional reduction is only design-local

Replacing a function by its weighted moment is exactly prediction-equivalent for one fixed measure. It is not equivalent for the transferable model required by the canonical core. If two experiment measures `mu` and `nu` differ, a function can satisfy

\[
\int h\,d\mu=0
\quad\text{but}\quad
\int h\,d\nu\ne0.
\]

Consequently, an `F0_a/FA_a`-only model changes the prediction space for a new spectrum, geometry, or exposure. It is a restricted observation-design profile, not a complete transferable reparameterization.

## Tensor dimension and degrees of freedom

E3-E4 establish rank two, square structure, symmetry, and zero trace. The canonical core additionally warns against an unconstrained **five-parameter** tensor. For a real symmetric traceless `d`-by-`d` tensor,

\[
k(d)=\frac{d(d+1)}{2}-1.
\]

The positive solution of `k(d)=5` is `d=3`. ICRS and laboratory direction vectors independently support the same spatial interpretation. STEP 07A therefore classifies `dimension = 3` as `ALGEBRAICALLY_IMPLIED`. This is a successor scientific adjudication; it does not rewrite the historical machine contract that correctly recorded the dimension as unrecovered.

A general 3-by-3 symmetric traceless tensor has five continuous components. Removing scale by a norm constraint leaves four generic continuous shape-and-orientation degrees of freedom. A uniaxial restriction would reduce this further, but uniaxiality is a `NEW_PHYSICAL_ASSUMPTION`.

For the experimental design tensor

\[
M_{a,ij}=\langle f_{A,a}n_in_j\rangle_a,
\]

the aggregate anisotropic factor is

\[
F_{A,a}=A_a:\operatorname{STF}(M_a).
\]

One aggregate constrains at most one combination of the five tensor components. With two independent BEST zone aggregates and one shared tensor, the unobserved tensor subspace has dimension at least three. Zone-specific tensors are still less identifiable.

## Tensor normalization comparison

| Candidate | Rotation invariant | Numerical behavior | Scientific effect | Decision |
|---|---:|---|---|---|
| Frobenius norm `sqrt(Tr(A^T A))` | Yes | Smooth, component-symmetric, stable sum of squares | Removes scale only | **Selected gauge representative** |
| Spectral norm | Yes | Nondifferentiable at eigenvalue crossings | Removes scale but privileges an extremal eigenvalue | Not selected |
| Largest absolute eigenvalue | Yes | Tie and ordering discontinuities | Removes scale but privileges an extremal eigenvalue | Not selected |
| Reference component | No | Singular when the component vanishes | Introduces frame/component preference | Rejected |

For nonzero `A`, Frobenius normalization is a `NORMALIZATION_CONVENTION`. A deterministic sign representative may be obtained, after a coordinate frame is fixed, by requiring the first nonzero entry of the canonical independent-component tuple to be positive and carrying the compensating sign in `hA`. This removes a discrete representation ambiguity only. It does not select eigenvalue ratios or physical orientation. The zero tensor is a separate anisotropy-off branch and is never normalized.

## Dimensional audit

| Symbol | Equation constraint | Uniquely determined? | Gauge-dependent? | Canonical status after reduction |
|---|---|---:|---:|---|
| `epsilon0`, `epsilonLSC` | efficiencies | Yes | No | dimensionless |
| `n` | unit direction | Yes | No | dimensionless, Euclidean norm 1 |
| `lambda0 f0_a` | additive E2 response | Product only | Yes | `S_a`, dimensionless |
| `lambdaA A_a fA_a` | additive E2 response | Product only | Yes | `B_a`, dimensionless |
| `q_a=n^T A_a n` | E3 | Same units as `A_a` | Yes | absorbed into `B_a` |
| `F0_a` | E8 | Same units as `f0_a` | Yes | use `<S_a>`, dimensionless |
| `FA_a` | E8 | Same units as `A_a fA_a` | Yes | use `<n^T B_a n>`, dimensionless |
| `N0_a`, `NLSC_a` | E1/E5 | Same count-or-rate units | No | dataset contract must declare count or rate |
| `R_a`, `Rpred_a`, `Delta R_a` | E6/E7/E10 | Yes | No | dimensionless |
| `C` in ratio space | E10 | Yes | No | dimensionless squared |
| `chi2` | E10 | Yes | No | dimensionless |

Energy, time, and angle unit choices are coordinate conventions. The future specification should require explicit conversion into one canonical unit set before evaluating a response function. Choosing those units does not determine the missing response shape.

## Frames and time

The following separation is sufficient and does not manufacture a preferred direction:

| Frame or object | Role | Classification | State |
|---|---|---|---|
| ICRS Cartesian basis | storage frame for a physical tensor/direction | `COORDINATE_CONVENTION` | may be standardized |
| Earth-fixed intermediate | Earth rotation and site location | `COORDINATE_CONVENTION` | required for implementation |
| right-handed local laboratory basis | local direction and surveyed detector rotation | `COORDINATE_CONVENTION` | axes must be frozen |
| detector geometry frame | experiment-provided geometry | `EMPIRICAL_PARAMETER` | dataset input |
| physical tensor direction in ICRS | model prediction phase/orientation | `UNRESOLVED_PHYSICAL_CHOICE` | owner decision required |
| UTC/UT1/earth-orientation inputs | reproducible time transform | mixed coordinate/data contract | versioned external input required |

No separate model-internal preferred frame is needed: the tensor can be represented directly in ICRS. The coordinate transform is representational. The numerical tensor orientation relative to ICRS is physical.

## Integration normalization

The normalized bracket consistent with E1, E5, E6, E7, and E8 is

\[
\langle g\rangle_a=
\frac{1}{N_{0,a}}
\int_{D_a}g\,
\Phi P\sigma\epsilon_{0,a}W_a
\,dE\,d\Omega\,dt,
\qquad N_{0,a}>0.
\]

This is `ALGEBRAICALLY_IMPLIED` once the observable is the E6 ratio. It also makes a constant-one response average to one and is invariant to a common rescaling of the baseline weight.

- Source and isotope-line weights belong in `Phi` and `sigma`.
- Volume and geometry weights belong in `W_a`.
- Exposure and time dependence belong in the time-dependent factors and domain.
- Detector response belongs in `epsilon0_a` and the invariant LSC response.
- The denominator is the single baseline integral `N0_a`; factors are not separately renormalized unless an authoritative dataset contract requires it.
- A zero or non-finite denominator blocks evaluation.
- Quadrature, summation, and numerical tolerance are implementation conventions after the domain and measure are fixed.

Exact experiment domains, source-line tables, geometry, exposure intervals, and timing distributions remain empirical inputs. They are not model parameters.

## E5/E7 to E10 observable binding

### Binding A: exact ratio, selected

\[
R_{\mathrm{pred},a}=N_{\mathrm{LSC},a}/N_{0,a}.
\]

Under the normalized E8 bracket and literal linear E2 response,

\[
R_{\mathrm{pred},a}=1+\lambda_0F_{0,a}+\lambda_AF_{A,a}.
\]

E7 is therefore the residual `Rpred-1`; it remains labelled first-order because that is its historical source classification. Production semantics come from the exact E5/E1 ratio. This binding is `ALGEBRAICALLY_IMPLIED` and does not add physics.

### Binding B: residual-native

`Rpred = 1 + DeltaR` is physically equivalent to Binding A only when E8 uses the same normalized baseline measure and E7 is evaluated from E2. If E7 is supplied independently or with a different approximation, predictions are not guaranteed equivalent.

### Binding C: count-space likelihood

Using `NLSC` directly against observed counts would replace the ratio-space observable in E10. It changes the observable law and requires at least version 6.4.0.

For E10, `theta` contains LSC physical parameters and `eta` contains nuisance parameters, following the original unified source and E10 itself. E5's broader prose description of `theta` is treated as an imprecise shorthand.

E9's double ratio is a deterministic function of the inner and outer ratios. E10 must use two independent BEST coordinates or an explicitly rank-aware covariance policy; it must not count the double ratio as an independent third datum.

## Parameter-count hypotheses

| Hypothesis | Required prior specification | Effective LSC degrees of freedom | Adjudication |
|---|---|---:|---|
| No LSC response | `S=0`, `B=0` | 0 | Null model, not implied by LSC |
| Scalar with fixed normalized shape | fixed `S` shape | 1 amplitude | Possible restricted M5 model; shape still needs new physics |
| Scalar plus fixed anisotropic shape/orientation | fixed scalar and anisotropic templates plus fixed normalized tensor | 2 amplitudes | Minimal full trace/traceless option; all fixed objects need new physics |
| Scalar plus unknown shared general STF tensor | fixed response templates | 1 scalar plus 5 effective anisotropic components | Underidentified by BEST summaries |
| Zone-specific general STF tensors | fixed response templates | at least `1+5m` | Literal E3 reading; undermines transferability |
| Unrestricted response functions | none | infinite-dimensional | Current unresolved model class |

There is no evidence for a parameter-free non-null model. A one- or two-amplitude model exists only after its response shapes and tensor hypothesis are fixed independently of validation results.

## Version implication

Gauge fixing, Frobenius normalization, dimension adjudication, coordinate conventions, normalized E8, and Binding A could individually be formalized without changing E1-E12.

However, a complete executable model necessarily requires at least one new functional form and, for the anisotropic sector, a new physical tensor-sharing/orientation hypothesis. The STEP 07A version rule assigns either change to version 6.4.0. No fundamental model-class replacement is required, so 7.0 is not justified.

**Scientific verdict: `VERSION_ESCALATION_REQUIRED_6_4_0`.**
