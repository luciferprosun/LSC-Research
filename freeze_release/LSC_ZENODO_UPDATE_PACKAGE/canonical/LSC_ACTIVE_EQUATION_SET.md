# LSC Active Equation Set

Status: Step 1 canonicalization output  
Rule: no new equations are introduced. The active set is restricted to equations already present in the LSC 6.3.0 / master package sources or directly classified in the external audits as freeze-core candidates.  

## 1. Classification Key

- canonical: active in the pre-BEST-2 freeze framework.
- dimensional review needed: active only with explicit caveat; cannot support strong claims until reviewed.
- exploratory: useful for model-building but not frozen as validation core.
- deprecated: excluded from active core.
- historical only: retained for lineage.

## 2. Canonical Equations

### E1. Baseline event expectation

```text
N0_a = integral dE dOmega dt [
  Phi(E,t,Omega)
  P_alpha_beta(E,L)
  sigma(E)
  epsilon0_a(E,t,Omega)
  W_a(E,t,Omega)
]
```

Classification: canonical  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `a`: analysis bin or detector zone;
- `Phi`: source flux;
- `P_alpha_beta`: oscillation probability or survival/transition factor;
- `sigma`: capture cross section;
- `epsilon0_a`: baseline detector efficiency;
- `W_a`: geometry/exposure weighting.

Physical meaning:

- defines the non-LSC baseline expectation.

Validation relevance:

- required to compare LSC to null and baseline models.

Dataset tie:

- BEST/GALLEX/SAGE rate predictions; needs source lines, geometry, efficiencies and covariance.

### E2. LSC detector-efficiency response

```text
epsilon_LSC,a(E,t,Omega)
= epsilon0_a(E,t,Omega) *
  [1 + lambda0 * f0_a(E,t) + lambdaA * q_a(t,Omega) * fA_a(E,t)]
```

Classification: canonical with functional-form freeze required  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `lambda0`: scalar trace-response amplitude;
- `lambdaA`: anisotropic response amplitude;
- `f0_a`: scalar response template;
- `fA_a`: anisotropic response template;
- `q_a`: anisotropic projection.

Physical meaning:

- active detector-response ansatz.

Validation relevance:

- separates trace-only and trace-plus-anisotropy models.

Dataset tie:

- BEST/BEST-2 zone data; GALLEX/SAGE transfer only if geometry and metadata are available.

Audit caveat:

- `f0_a` and `fA_a` must be explicitly frozen before fitting.

### E3. Anisotropic projection

```text
q_a(t,Omega) = n_i^lab(t,Omega) A_a^{ij} n_j^lab(t,Omega)
```

Classification: canonical with identifiability caveat  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `n_i^lab`: lab-frame direction vector;
- `A_a^{ij}`: anisotropy tensor for bin/zone `a`.

Physical meaning:

- projects directional response into the detector/lab frame.

Validation relevance:

- needed for traceless anisotropy and sidereal/orientation tests.

Dataset tie:

- requires orientation/timestamp metadata; currently underconstrained.

Audit caveat:

- a freely fitted tensor is overparameterized with current public data.

### E4. Tensor symmetry and tracelessness

```text
A_a^{ij} = A_a^{ji}
Tr(A_a) = 0
```

Classification: canonical  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `A_a^{ij}`: symmetric traceless response tensor.

Physical meaning:

- removes scalar normalization from directional component.

Validation relevance:

- prevents trace response and anisotropy from being collapsed into one undifferentiated fit term.

Dataset tie:

- only testable with enough directional/orientation information.

### E5. LSC event expectation

```text
N_LSC,a(theta) =
integral dE dOmega dt [
  Phi P sigma epsilon_LSC,a W_a
]
```

Classification: canonical  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `theta`: LSC parameters and nuisance parameters as specified in the frozen model.

Physical meaning:

- event expectation after applying the LSC detector-response template.

Validation relevance:

- direct model-comparison object.

Dataset tie:

- requires same source/geometry/covariance inputs as E1.

### E6. Observed ratio

```text
R_a = N_obs,a / N0_a
```

Classification: canonical  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `N_obs,a`: observed count/rate;
- `N0_a`: baseline expected count/rate.

Physical meaning:

- rate-ratio residual target.

Validation relevance:

- basic input to BEST/GALLEX/SAGE comparison.

Dataset tie:

- available in summary form; full likelihood requires missing details.

### E7. First-order LSC residual template

```text
Delta R_a^LSC ~= lambda0 * F0_a + lambdaA * FA_a
```

Classification: canonical as first-order template  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `F0_a`: scalar weighted response;
- `FA_a`: anisotropic weighted response.

Physical meaning:

- linearized residual decomposition.

Validation relevance:

- supports M5 trace-only and M6 trace-plus-anisotropy comparison.

Dataset tie:

- requires weighting definitions and covariance.

### E8. Weighted scalar and anisotropic factors

```text
F0_a = <f0_a>_a
FA_a = <q_a fA_a>_a
```

Classification: canonical with weighting-definition caveat  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- brackets denote the same flux, cross-section, geometry and exposure weighting used in `N0_a`.

Physical meaning:

- converts functional templates into bin-level residual factors.

Validation relevance:

- required to avoid free post-hoc fitting of bin coefficients.

Dataset tie:

- needs explicit weights from experiment geometry and exposure.

### E9. BEST binned target

```text
R_BEST = (R_inner, R_outer, R_outer / R_inner)
```

Classification: canonical  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `R_inner`: inner-zone BEST ratio;
- `R_outer`: outer-zone BEST ratio.

Physical meaning:

- minimum BEST vector for two-zone tests.

Validation relevance:

- necessary but insufficient; cannot validate anisotropy alone.

Dataset tie:

- BEST summary data; full covariance still missing.

### E10. Covariance-aware validation statistic

```text
chi2(theta, eta) =
  [R_obs - R_pred(theta, eta)]^T
  C^{-1}
  [R_obs - R_pred(theta, eta)]
  + penalty(eta)
```

Classification: canonical with missing-covariance caveat  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `theta`: LSC parameters;
- `eta`: nuisance parameters;
- `C`: statistical and systematic covariance matrix;
- `penalty(eta)`: model/nuisance penalty.

Physical meaning:

- formal comparison statistic.

Validation relevance:

- mandatory for meaningful model comparison.

Dataset tie:

- currently blocked by missing full covariance matrices.

### E11. Frame transformation for sidereal/orientation tests

```text
n_lab(t) = R_lab<-ICRS(t, latitude, longitude, detector_orientation) * n_ICRS
```

Classification: canonical for future BEST-2 tests; currently metadata-blocked  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `n_ICRS`: fixed celestial-frame direction;
- `R_lab<-ICRS`: time-dependent transform to lab frame.

Physical meaning:

- distinguishes lab-fixed detector artifacts from celestial-frame anisotropy.

Validation relevance:

- essential for sidereal claims.

Dataset tie:

- requires timestamp, latitude/longitude and detector orientation metadata.

### E12. Sidereal template

```text
S_a(t) = n_lab,i(t) A^{ij} n_lab,j(t)
```

Classification: canonical for future test; speculative until metadata exists  
Source: LSC 6.3.0 Unified BEST-2 Continuation  

Variables:

- `S_a(t)`: time-dependent anisotropy signal;
- `A^{ij}`: traceless anisotropy tensor.

Physical meaning:

- predicted sidereal/orientation modulation template.

Validation relevance:

- strongest proposed discriminator, but not currently testable with public data.

Dataset tie:

- BEST-2 metadata required.

## 3. Active But Dimensional Review Needed

### DR1. Detector-frame energy reconstruction form

```text
E_rec = E_true * [1 + alpha_D * D_ij * p_hat^i * p_hat^j]
```

Classification: dimensional review needed  
Source: LSC 6.2.0 and historical 6.2.x line  

Reason:

- audits flag tensor dimensions, identifiability and possible Lorentz-violation implications.
- current 6.3.0 operational core can be expressed through detector efficiency response instead.

Validation relevance:

- not sufficient as a validation equation unless mapped to E2/E5 and external vetoes.

Dataset tie:

- indirect only.

### DR2. Effective propagation factor

```text
G(Phi,E) = 1 + delta_G(Phi,E) + O(delta_G^2)
```

Classification: dimensional review needed / effective-only  
Source: LSC 6.0 / 6.2.0 lineage  

Reason:

- `delta_G` has no accepted microscopic derivation in the current freeze.
- curvature/gravitational labels must be removed from active claims.

Validation relevance:

- can remain as effective nuisance/response language only.

Dataset tie:

- not directly identifiable with current Gallium summary data.

## 4. Deprecated Equation Families

### DEP1. PBH/curvature Hamiltonian family

Classification: deprecated / historical only  

Includes:

- explicit PBH/curvature `H_LSC`;
- explicit gravitational Hamiltonian terms as current Gallium mechanism;
- PBH resonance equations.

Reason:

- removed from current Gallium core;
- no direct validation path in BEST/GALLEX/SAGE.

### DEP2. Schwarzschild energy-map family

Classification: deprecated / historical only  

Includes:

- old `E_obs` / `E_emit` Schwarzschild-style mapping used as standalone explanation.

Reason:

- replaced by effective detector-response framing.

### DEP3. Covariant Lagrangian from LSC 5.5

Classification: deprecated / historical only  

Reason:

- Lorentz-violation and SME implications are unresolved;
- not used in current BEST-2 validation protocol.

### DEP4. Redundant tensor parameterizations

Classification: deprecated unless reduced to the single 6.3.0 trace/traceless structure  

Reason:

- multiple equivalent tensor forms create ambiguity and overfitting risk.

## 5. Equation Freeze Decision

Frozen as active:

- E1-E12 above.

Active only with caveats:

- DR1 and DR2.

Archived:

- DEP1-DEP4 and all historical equation clutter not needed by the 6.3.0 validation protocol.

