# LSC Canonical Core

Status: Step 1 canonicalization for the Pre-BEST-2 freeze program  
Scope: LSC / SC neutrino phenomenology only  
Current active reference state: LSC 6.3.0 Unified BEST-2 Continuation  
Primary identity: Zenodo concept DOI `10.5281/zenodo.19780615`  

## 1. Canonical Status

LSC is frozen as a constrained phenomenological validation framework.

It is not frozen as:

- confirmed physics,
- a discovery claim,
- a sterile-neutrino exclusion,
- a PBH/curvature theory,
- a new particle model,
- an AI/meta-analysis framework.

The active scientific question is:

Can a pre-registered detector-response model with scalar trace plus traceless anisotropic components structure gallium-source residuals better than null, normalization-only, cross-section/systematics, sterile-neutrino, and detector-systematics alternatives, while surviving external vetoes?

## 2. Active Canonical Concepts

### 2.1 Gallium-source residual analysis

The active domain is BEST/Gallium source-experiment residual analysis, including BEST, GALLEX and SAGE where data are available.

Canonical role:

- define rate-ratio residuals;
- compare against required baselines;
- avoid claiming new physics before validation;
- preserve missing-data limits.

### 2.2 Detector-response framing

The active LSC object is a detector-response template, not a fundamental field.

Canonical role:

- separate detector response from propagation speculation;
- express residual templates in terms of analysis bins or detector zones;
- treat detector systematics as an active competing explanation.

### 2.3 Trace / traceless split

The scalar trace response and traceless directional anisotropy split is active and canonical because it reduces ambiguity between:

- global normalization shifts;
- cross-section/source-strength shifts;
- detector-zone effects;
- directional or orientation-dependent structure.

Audit consolidation:

- Kimi: freeze trace/traceless formalism as the cleanest structural element.
- Gemini: freeze with downgraded claims because directional tensor components are currently underconstrained.
- DeepSeek: detector/systematics can mimic trace and traceless components unless explicitly broken by metadata and calibration.
- Claude/physics audit: trace/traceless separation is salvageable only if anisotropy is pre-defined rather than freely fitted.

### 2.4 Frozen prediction protocol

Before BEST-2-style fitting, the following must be frozen:

- equations used;
- parameter list;
- priors or bounds;
- datasets;
- baseline models;
- success criteria;
- failure criteria;
- treatment of missing covariance;
- external veto rules.

Any change after seeing fit output requires a new version and cannot be treated as the same freeze.

### 2.5 Required baseline hierarchy

The active canonical baseline hierarchy is:

- M0: null / published baseline;
- M1: scalar normalization only;
- M2: cross-section/systematics only;
- M3: sterile-neutrino benchmark;
- M4: detector-systematics benchmark;
- M5: LSC trace-only;
- M6: LSC trace plus traceless anisotropy.

LSC can only claim relative support if M5/M6 improve predictive performance after model-complexity penalties and after comparison to M0-M4.

### 2.6 Leave-one-out and cross-experiment validation

Anchor fits are not validation.

Active validation requires:

- leave-one-out stability;
- BEST inner-to-outer and outer-to-inner prediction;
- BEST-to-GALLEX/SAGE transfer;
- GALLEX/SAGE-to-BEST transfer;
- no post-hoc tuning after seeing target data.

### 2.7 External vetoes

The active framework must survive quantitative veto checks:

- KATRIN energy-response constraints;
- IceCube / SME-style anisotropy or Lorentz-violation constraints where relevant;
- solar-neutrino consistency;
- standard three-flavor oscillation fits;
- detector calibration and source cross-section constraints.

These are constraints, not optional discussion points.

## 3. Active Canonical Dataset Scope

### BEST

Active role:

- primary two-zone gallium source target;
- inner and outer zone ratio structure;
- future BEST-2 freeze target.

Current limitation:

- public data are insufficient for full likelihood-level validation without covariance, extraction-level data and metadata.

### GALLEX

Active role:

- cross-experiment validation target;
- source-calibration comparison.

Current limitation:

- exact source coordinates, exposure-level tables and full response covariance are missing from current local package.

### SAGE

Active role:

- cross-experiment validation target;
- isotope comparison using 51Cr and 37Ar source calibrations.

Current limitation:

- run-by-run exposure, impurity and counter-level likelihood data are missing.

### BEST-2

Active role:

- future discriminating validation environment.

Required metadata:

- time-stamped extraction and exposure data;
- source-position and source-extension model;
- zone-by-zone covariance matrix;
- detector orientation metadata;
- environmental/systematic monitoring;
- public baseline prediction files.

## 4. Active Parameter Structures

The active parameter structures are limited to those needed by the 6.3.0 validation template:

- `lambda0`: scalar trace response amplitude;
- `lambdaA`: anisotropic response amplitude;
- `A_a^{ij}`: symmetric traceless anisotropy tensor for analysis bin or detector zone `a`;
- `f0_a(E,t)`: scalar response template, not yet physically fixed;
- `fA_a(E,t)`: anisotropic response template, not yet physically fixed;
- `eta`: nuisance parameters for source strength, cross-section, geometry, extraction efficiency and normalization;
- `C`: statistical and systematic covariance matrix.

Audit restriction:

- `A_a^{ij}` must not remain an unconstrained five-parameter fit if the available data cannot identify it.
- Tensor orientation must be pre-specified for sidereal claims.
- `f0_a` and `fA_a` require explicit functional forms before any fit can be called frozen.

## 5. Active Claim Boundary

Allowed claims:

- LSC is an unvalidated phenomenological framework.
- LSC 6.3.0 defines a conservative pre-BEST-2 validation protocol.
- Trace/traceless separation is a useful way to separate normalization-like and directional-like residual templates.
- Sterile-neutrino explanations remain viable comparison baselines.
- Detector systematics remain active competitors.
- BEST-2 requires preregistered templates and metadata.

Not allowed:

- LSC proves the gallium anomaly.
- LSC excludes sterile neutrinos.
- LSC tensor structures are confirmed physical fields.
- PBH/curvature mechanisms are part of the current Gallium core.
- Anchor fits validate LSC.
- Detector systematics can be dismissed without a quantitative M4 baseline.

## 6. Canonicalization Decision

The canonical core is the LSC 6.3.0 validation framework after audit constraints:

- keep trace/traceless response separation;
- keep M0-M6 baseline hierarchy;
- keep frozen prediction protocol;
- keep leave-one-out and cross-experiment validation requirements;
- keep external veto requirements;
- downgrade all physical interpretation stronger than detector-response phenomenology;
- archive PBH/curvature-heavy and redundant historical material.

