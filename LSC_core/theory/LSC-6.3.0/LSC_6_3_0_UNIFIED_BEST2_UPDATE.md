# LSC 6.3.0 Unified BEST-2 Continuation

Status: unvalidated phenomenological continuation  
Date: 2026-05-05  
Primary Zenodo concept DOI: `10.5281/zenodo.19780615`  
Current version DOI anchor: `10.5281/zenodo.19878587`  
Scope: LSC 6.0 -> LSC 6.2.0 -> LSC 6.3.0 continuation for BEST-2-style validation

## Abstract

LSC 6.3.0 is a conservative continuation of the LSC 6.2.0 preprint line. It does not introduce a discovery claim. It consolidates the strongest post-6.2.0 corrections into one testable framework for gallium-source experiments, especially BEST/BEST-2-style two-zone and multi-zone tests.

The update keeps LSC as one Zenodo project by using the existing LSC concept DOI, `10.5281/zenodo.19780615`, as the project-level citation target. The LSC v1.2.0 computational record is treated as a supplementary computational release, not as a separate primary theory line.

The scientific change from LSC 6.2.0 is not a stronger claim. It is a stronger validation protocol:

- separate scalar trace response from traceless directional anisotropy;
- freeze the model specification before fitting;
- fit BEST inner/outer zones with nuisance parameters and external comparison models;
- require leave-one-out and cross-experiment validation;
- keep KATRIN, IceCube, solar-neutrino, and standard-oscillation constraints as veto channels;
- archive negative results as valid outcomes.

## 1. Record Unification

The public LSC publication line should be cited as:

```text
LSC concept DOI: https://doi.org/10.5281/zenodo.19780615
Latest LSC version DOI: https://doi.org/10.5281/zenodo.19878587
```

The relevant published records are:

```text
LSC 6.0
Record: https://zenodo.org/records/19780616
Version DOI: 10.5281/zenodo.19780616
Concept DOI: 10.5281/zenodo.19780615

LSC 6.2.0
Record: https://zenodo.org/records/19878587
Version DOI: 10.5281/zenodo.19878587
Concept DOI: 10.5281/zenodo.19780615

LSC v1.2.0 computational release
Record: https://zenodo.org/records/19843361
Version DOI: 10.5281/zenodo.19843361
Concept DOI: 10.5281/zenodo.19843360
Role: supplementary computational/reproducibility release
```

LSC 6.0 and LSC 6.2.0 are already joined by the same Zenodo concept DOI. The practical cleanup is to make all future text point to the concept DOI for the evolving project, while treating the v1.2.0 computational record as a supplement.

## 2. What Is Accepted From The 2026-05-05 Model Iterations

### Accepted into LSC 6.3.0

Codex:

- exact anchor fits are insufficient;
- leave-one-out diagnostics are required;
- negative validation outcomes must be archived.

DeepSeek:

- trace and traceless anisotropy must be separated;
- sidereal tests need a fixed celestial reference frame;
- dimensional and frame consistency must be explicit.

Gemini:

- public language must remain conservative;
- LSC is a testable ansatz, not confirmed physics;
- sterile-neutrino interpretations remain valid comparison models.

GPT:

- detector-response framing is clearer and safer than older PBH-centered language;
- the theory should be presented as reconstruction/response phenomenology.

Kimi:

- BEST-2 needs an explicit likelihood and systematics model;
- sidereal/orientation dependence is the strongest discriminating test;
- prediction templates should be frozen before data fitting.

Manus:

- the public package should read as one continuous LSC line;
- version transitions need to be bridged cleanly.

### Not accepted as current claims

The following are not promoted to current theory claims:

- LSC proves the gallium anomaly;
- LSC excludes sterile neutrinos;
- the tensor is a confirmed physical field;
- AI model agreement validates the physics;
- full EFT, covariant, or PMNS-flavor completion is already established.

Those may remain future research directions only after a stable likelihood and external constraints exist.

## 3. Model Definition

The baseline event expectation is:

```text
N0_a = integral dE dOmega dt [
  Phi(E,t,Omega)
  P_alpha_beta(E,L)
  sigma(E)
  epsilon0_a(E,t,Omega)
  W_a(E,t,Omega)
]
```

where `a` indexes the analysis bin or detector zone. For BEST-style analysis, `a` includes at minimum the inner and outer gallium zones.

LSC 6.3.0 modifies only the detector-response layer unless explicitly stated otherwise:

```text
epsilon_LSC,a(E,t,Omega)
= epsilon0_a(E,t,Omega) *
  [1 + lambda0 * f0_a(E,t) + lambdaA * q_a(t,Omega) * fA_a(E,t)]
```

The anisotropic projection is:

```text
q_a(t,Omega) = n_i^lab(t,Omega) A_a^{ij} n_j^lab(t,Omega)
```

with:

```text
A_a^{ij} = A_a^{ji}
Tr(A_a) = 0
```

The predicted count/rate becomes:

```text
N_LSC,a(theta) =
integral dE dOmega dt [
  Phi P sigma epsilon_LSC,a W_a
]
```

The observed ratio is:

```text
R_a = N_obs,a / N0_a
```

and the first-order LSC residual template is:

```text
Delta R_a^LSC ~= lambda0 * F0_a + lambdaA * FA_a
```

where:

```text
F0_a = <f0_a>_a
FA_a = <q_a fA_a>_a
```

The brackets denote the same flux, cross-section, geometry, and exposure weighting used in `N0_a`.

## 4. BEST/BEST-2 Validation Layer

For BEST, the minimum binned vector is:

```text
R_BEST = (R_inner, R_outer, R_outer / R_inner)
```

The 6.2.1 Codex package gives an important warning: a model can fit anchor ratios exactly and still fail leave-one-out validation. Therefore LSC 6.3.0 must treat exact reproduction of BEST inner/outer values as insufficient.

The validation target is:

```text
chi2(theta, eta) =
  [R_obs - R_pred(theta, eta)]^T
  C^{-1}
  [R_obs - R_pred(theta, eta)]
  + penalty(eta)
```

where:

- `theta = {lambda0, lambdaA, A^{ij}, f0, fA}` are LSC parameters;
- `eta` are nuisance parameters for source strength, cross-section, geometry, extraction efficiency, and normalization;
- `C` is the statistical and systematic covariance matrix.

Minimum comparison models:

```text
M0: null / published baseline
M1: scalar normalization only
M2: cross-section nuisance only
M3: sterile-neutrino benchmark
M4: detector-systematics benchmark
M5: LSC trace-only
M6: LSC trace + traceless anisotropy
```

LSC can only be preferred if `M6` improves predictive performance after parameter penalties relative to simpler models.

## 5. Frozen Prediction Protocol

Before any new BEST-2 fitting, create a locked model specification with:

- equations;
- parameter list;
- priors or bounds;
- datasets;
- comparison models;
- success criteria;
- failure criteria.

Any equation change after seeing fit output must increment the version number.

Minimum validation tests:

```text
T1: fit BEST inner, predict BEST outer
T2: fit BEST outer, predict BEST inner
T3: fit BEST, predict GALLEX/SAGE
T4: fit GALLEX/SAGE, predict BEST
T5: fit all gallium source data, test KATRIN/IceCube veto region
T6: test sidereal/orientation template if timestamps and geometry exist
```

## 6. Sidereal And Orientation Test

The anisotropic component must be evaluated in a fixed celestial frame, then transformed to the lab frame:

```text
n_lab(t) = R_lab<-ICRS(t, latitude, longitude, detector_orientation) * n_ICRS
```

The sidereal template is:

```text
S_a(t) = n_lab,i(t) A^{ij} n_lab,j(t)
```

Falsification conditions:

- no stable sidereal phase after environmental correction;
- phase or amplitude changes randomly across datasets;
- anisotropy collapses into scalar normalization under covariance propagation;
- each experiment requires unrelated tensor parameters with no shared rule.

## 7. External Vetoes

Any parameter region that improves gallium residuals must be checked against:

- KATRIN beta-spectrum constraints;
- IceCube anisotropy/systematics constraints;
- solar-neutrino consistency;
- standard three-flavor oscillation fits;
- detector calibration and source cross-section uncertainties.

If an LSC parameter region improves BEST but violates these checks, it is not a viable physical explanation.

## 8. BEST-2 Experimental Recommendation

For a future BEST-2-style test, the most useful additions are:

- time-stamped extraction and exposure data;
- source-position and source-extension model;
- zone-by-zone covariance matrix;
- detector orientation metadata;
- environmental/systematic monitoring;
- public baseline prediction files;
- pre-registered LSC and sterile-neutrino comparison templates.

The central discriminant is not only the mean deficit. It is whether a frozen trace-plus-anisotropy template predicts stable zone, orientation, or sidereal structure better than scalar/nuisance alternatives.

## 9. Public Claim Boundary

Allowed statement:

```text
LSC 6.3.0 consolidates the LSC 6.2.x line into a single falsifiable BEST-2 validation framework. It tests whether a trace-plus-traceless detector-response template can structure gallium-source residuals better than simpler normalization, cross-section, sterile-neutrino, or detector-systematics alternatives.
```

Disallowed statement:

```text
LSC 6.3.0 explains the gallium anomaly or proves new physics.
```

## 10. Zenodo Update Recommendation

Do not create a detached Zenodo project.

Use:

```text
Primary project citation:
https://doi.org/10.5281/zenodo.19780615

Latest version page:
https://zenodo.org/records/19878587
```

If only metadata is edited, Zenodo does not require a new DOI. If files are replaced or a new package is uploaded as a new version, Zenodo will assign a new version DOI but keep the same concept DOI. For user-facing continuity, cite the concept DOI and describe the update as part of the same LSC project.

