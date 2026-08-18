# STEP 07A RESULT

Project: **LSC Validation Kernel**

Status: **PASS**

Scientific-adjudication verdict: **`VERSION_ESCALATION_REQUIRED_6_4_0`**

## Technical summary

The equation-first and observable-first audits independently produce the same minimal invariant response:

\[
\epsilon_{\mathrm{LSC},a}
=\epsilon_{0,a}\left[1+S_a(E,t)+n^TB_a(E,t)n\right],
\]

with `S_a=lambda0*f0_a` and `B_a=lambdaA*fA_a*A_a`. This exactly removes the amplitude/function/tensor scale and sign gauges. Three spatial dimensions, normalized E8 weighting, and the E5/E1 ratio binding to E10 can also be adjudicated without new physics.

The remaining ambiguity is not representational. The source explicitly lacks the physical forms of both response functions, and it does not select tensor eigenvalue shape, sharing semantics, or absolute physical orientation. Any complete transferable successor must add at least a new functional form and, for M6, a new tensor hypothesis. The explicit STEP 07A version rule assigns those changes to 6.4.0. No fundamental model-class change requires 7.0.

No fit, prediction, T1-T12 execution, BEST-2 access, publication, push, or E1-E12 change occurred.

## A. Gauge degeneracies

For nonzero scale factors, E2-E8 are invariant under

\[
(\lambda_0,f_{0,a})\mapsto(c_0\lambda_0,f_{0,a}/c_0)
\]

and

\[
(\lambda_A,f_{A,a},A_a)
\mapsto(c_A\lambda_A,d_af_{A,a},A_a/(c_Ad_a)).
\]

Negative factors prove sign degeneracy. Passive orthogonal frame changes `n->Qn`, `A->QAQ^T` also preserve `n^TAn`. Scale, sign, and passive coordinates are gauge; physical rotation relative to ICRS is not.

Full derivation: [GAUGE_IDENTIFIABILITY_ANALYSIS.md](GAUGE_IDENTIFIABILITY_ANALYSIS.md).

## B. Canonical parameterization

Selected invariant objects:

- `S_a(E,t)=lambda0*f0_a(E,t)`;
- `B_a(E,t)=lambdaA*fA_a(E,t)A_a`;
- `rho_a=S_a+n^T B_a n`;
- normalized baseline measure `dnu_a/N0_a`.

For a factorized anisotropic representation, `B_a=h_A,a*T_a`, with `T_a` independent of energy and time. Historical `lambda` and unnormalized function/tensor factors are aliases, not independently physical parameters.

Classification: `PHYSICALLY_EQUIVALENT_REPARAMETERIZATION`.

## C. `f0_a`

- Index `a`: analysis bin or detector zone.
- Domain: `(E,t)`.
- Codomain: scalar response factor; individual units are gauge-dependent.
- Source status: exact form and normalization not frozen.
- Observable content for one design: only the weighted functional `<S_a>_a`.
- Full function: not identifiable from aggregate rates.

Replacing the function by one fixed-design moment is exact only for that design and loses cross-experiment transfer. A new transferable form is a `NEW_PHYSICAL_ASSUMPTION` and requires 6.4.0.

## D. `fA_a`

- Index and domain: zone/bin `a`, `(E,t)`.
- Directional dependence is separated into `q_a=n^TA_an`.
- Observable content for one design: only `<n^T B_a n>_a`.
- Any perturbation in the `q`-weighted functional null space is invisible to that aggregate.

No source determines energy/time shape, normalization, transfer rule, or relation to geometry. A constant or fitted form is not a neutral convention.

## E. Tensor dimension

E3-E4 give a rank-two, square, symmetric, traceless spatial tensor. The canonical core's five-parameter warning supplies

\[
d(d+1)/2-1=5,
\]

whose positive solution is `d=3`. ICRS/laboratory directions support the same result.

Decision: **3-by-3**, classification `ALGEBRAICALLY_IMPLIED`.

Before scale fixing: 5 continuous STF components. After scale gauge: 4 generic continuous shape/orientation degrees per active tensor.

## F. Tensor normalization

Frobenius norm is selected as a gauge representative on the nonzero branch:

\[
\|T_a\|_F=1.
\]

It is rotation invariant, component-symmetric, and smoother than spectral or maximum-eigenvalue normalization. A deterministic coordinate sign representative carries the compensating sign in `h_A,a`. The zero tensor is a separate anisotropy-off branch.

This fixes only redundancy. It does not select eigenvalue ratios or physical orientation.

## G. Tensor orientation

Coordinate orientation is conventional; physical orientation relative to ICRS changes predictions. The source does not provide a preferred axis.

Status: **`UNRESOLVED_PHYSICAL_CHOICE`**.

General STF, uniaxial, shared, zone-derived, and independent-zone tensors are not equivalent. Choosing a tensor family or physical axis is new physics and requires 6.4.0.

## H. Frames and time

The draft distinguishes:

- ICRS storage basis;
- Earth-fixed intermediate transform;
- right-handed local laboratory basis;
- surveyed detector geometry frame;
- physical tensor orientation;
- versioned UTC/UT1/earth-orientation inputs.

The coordinate chain is a `COORDINATE_CONVENTION`. The physical ICRS direction is not. Exposure midpoint fallback remains prohibited.

## I. Units

E2 fixes only

\[
[\lambda_0][f_0]=1,
\qquad
[\lambda_A][A][f_A]=1.
\]

After gauge reduction, `S_a`, `B_a`, `T_a`, ratios, residuals, and direction vectors are dimensionless. Ratio-space covariance is dimensionless squared and chi-square is dimensionless. Energy, time, and angle units are explicit coordinate conventions; each dataset must declare whether `N` is a count or rate.

## J. Observable binding

Selected `BINDING_A`:

\[
R_{\mathrm{pred},a}=N_{\mathrm{LSC},a}/N_{0,a}.
\]

Under E2 and normalized E8,

\[
R_{\mathrm{pred},a}=1+\langle S_a\rangle_a+\langle n^TB_an\rangle_a.
\]

E7 is the derived residual diagnostic. `theta` contains physical LSC parameters; `eta` contains nuisances. Count-space `BINDING_C` would change E10 and requires at least 6.4.0.

BEST's double ratio is derived from inner and outer ratios and must not be counted as a third independent datum.

## K. Integration normalization

The E8 bracket is adjudicated as

\[
\langle g\rangle_a=
\frac{\int_{D_a}g\,\Phi P\sigma\epsilon_{0,a}W_a\,dE\,d\Omega\,dt}
{N_{0,a}},
\qquad N_{0,a}>0.
\]

Source-line/isotope, geometry/volume, time/exposure, and detector factors enter once through the baseline measure. A zero or non-finite denominator blocks execution. Exact domains and factors are authoritative dataset inputs; quadrature is a later implementation convention.

## L. Minimal physical parameter set

The active gauge-invariant objects are `S_a`, `h_A,a`, normalized `T_a`, and the tensor sharing rule. Their values are not known.

- Current unrestricted form: infinite-dimensional because response families are absent.
- Fixed scalar shape: one scalar amplitude.
- Fixed scalar and anisotropic shapes plus fixed tensor: two amplitudes.
- Shared general STF tensor with fixed functions: one scalar plus five effective anisotropic components before scale redistribution.
- Zone-specific general STF tensors: at least `1+5m` effective components for `m` zones.

Machine-readable table: [MINIMAL_PHYSICAL_PARAMETER_SET.csv](MINIMAL_PHYSICAL_PARAMETER_SET.csv).

## M. Parameters requiring empirical determination

No parameter was fitted. If theory does not provide amplitudes or coefficients, a future 6.4.0 development step must freeze one objective, development dataset rows and hashes, covariance scenario, bounds, optimizer, identifiability check, and exposure labels before fitting.

Any historical gallium data used become `MODEL_EXPOSED` / `RETROSPECTIVE_NON_BLIND`. BEST-2 observations remain prohibited.

Protocol: [PARAMETER_DETERMINATION_REQUIREMENTS.md](PARAMETER_DETERMINATION_REQUIREMENTS.md).

## N. Version decision

- Gauge fixing, normalized integration, coordinate conventions, unit conventions, three-dimensional adjudication, and Binding A could remain patch-level formalization.
- New `f0_a/fA_a` forms, tensor family/sharing, and preferred physical direction change the transferable prediction space.
- The user-supplied rule assigns those changes to 6.4.0.
- The detector-response model class remains intact, so 7.0 is not required.

Decision: **`VERSION_ESCALATION_REQUIRED_6_4_0`**.

Non-executable draft: [LSC_6_4_0_SCIENTIFIC_SPECIFICATION_DRAFT.yaml](../../spec/LSC_6_4_0_SCIENTIFIC_SPECIFICATION_DRAFT.yaml).

## O. Option space

| Option | Parameters after fixed shapes | Identifiability | Falsifiability | Prediction-space change | Version | Recommendation |
|---|---:|---|---|---:|---|---|
| trace-only fixed template | 1 amplitude | conditional; constant shape aliases normalization | moderate with transfer tests | yes | 6.4.0 restricted M5 | fallback |
| shared uniaxial tensor with predeclared physical axis | 2 amplitudes | best finite full-M6 option | strongest finite option | yes | 6.4.0 | **recommended if a physical axis exists** |
| general/flexible tensor-function family | at least 6 plus function-shape degrees; potentially infinite | poor | weak without external structure | yes | 6.4.0 | not recommended |

No option was selected using fit quality.

## P. Owner decisions required

Exactly three scientific decisions remain:

1. response-function hypothesis;
2. anisotropic tensor family and physical-axis hypothesis;
3. cross-zone and cross-experiment sharing semantics.

Each is presented as A/B/C with consequences in [OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md](OWNER_SCIENTIFIC_DECISIONS_REQUIRED.md).

## Q. Symbolic tests

- gauge scale/sign equivalence: PASS;
- tensor symmetry/tracelessness and component count: PASS;
- Frobenius normalization: PASS;
- passive-frame covariance: PASS;
- normalized integration and weight-rescaling invariance: PASS;
- fixed-design functional null-space/non-transferability: PASS;
- exact E5/E8 ratio binding: PASS;
- zero, scalar-off, and anisotropic-off limits: PASS;
- BEST coordinate-rank check: PASS;
- STEP 07A artifact/authorization checks: PASS.

Targeted STEP 07A suite: **17/17 PASS**.

Full suite: **176/176 PASS**, plus **18/18 parameterized subtests**.

## R. Historical integrity

- historical 6.3.0 HEAD: `6ffa07bdde533fcc2a550e36c762b8edd9236c47`;
- E1-E12 changed: **NO**;
- historical tree changed: **NO**;
- archive hash verification: **1,882/1,882 PASS**;
- nested repository integrity: **4/4 clean at expected HEADs; `git fsck` PASS**;
- fit/prediction/validation/BEST-2 execution: **NONE**.

The new 3-by-3 adjudication and all 6.4.0 draft content are successor decisions. They do not rewrite what was historically recoverable in 6.3.0.

## S. Git state

- input branch: `main`;
- input HEAD: `7a8a281da6e3ace333ae1d2cac91a1cece570459`;
- intended commit: `Step 07A: adjudicate scientific specification and version`;
- final commit: recorded in the final Git receipt because a commit cannot embed its own hash;
- push: **NO**;
- release/tag: **NO**;
- final worktree: **CLEAN after the STEP 07A commit**.

## T. Next authorized path

**PATH D — OWNER SCIENTIFIC DECISION REQUIRED**

Reason: STEP 07A has removed the algebraic and coordinate ambiguity, but software cannot choose the response mechanism, tensor physical hypothesis, or sharing semantics. After the owner records the three decisions, the expected subsequent engineering path is PATH C: design and implement LSC 6.4.0 under a new freeze contract.

## Final scientific answer

**The remaining ambiguity is only partly representational. Gauge, normalization, units, coordinates, integration, and observable binding can be resolved without new physics; completing LSC requires new response-function and tensor-orientation assumptions.**
