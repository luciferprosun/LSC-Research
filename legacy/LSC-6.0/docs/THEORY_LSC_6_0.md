# LSC 6.0 Theory Note

## Title

**LSC 6.0: A Phenomenological Framework for Neutrino Propagation and Anisotropic Detection**

## Abstract

LSC 6.0 is a phenomenological framework for neutrino physics that combines weak propagation-level modulation with anisotropic detector-level energy reconstruction. It is developed as a conservative continuation of the LSC research line, whose public Zenodo archival sequence begins with LSC 4.2, DOI: `10.5281/zenodo.19602045`.

The model removes earlier unsupported assumptions involving primordial black holes or compact astrophysical objects as necessary ingredients of the Gallium interpretation. Instead, LSC 6.0 expresses the observable effect through an effective propagation factor and a detector response tensor. The core hypothesis is that a coupled propagation-measurement mechanism can reduce the required detector-level energy-scale bias from an implausibly large standalone value near 10% to a testable phenomenological range around 3-6%.

This document should be read as an effective model proposal, not as a confirmed physical theory.

## 1. Physical Context

Standard three-flavor neutrino oscillation physics has strong experimental support. However, source-calibration measurements in gallium experiments have reported deficits that motivate phenomenological alternatives. Sterile-neutrino interpretations are possible but face increasing constraints from precision experiments and global analyses.

LSC 6.0 explores a different possibility: the measured event rate may be affected by a small propagation-level correction and a detector-dependent anisotropic reconstruction term. The framework is designed so that it can be tested against:

- BEST and the Gallium anomaly,
- KATRIN beta-spectrum constraints,
- IceCube anisotropy and Lorentz-violation searches,
- future controlled source experiments with orientation or sidereal analyses.

## 2. Lineage

The LSC framework has been developed over an extended period as an independent theoretical research line. Public archival records begin from LSC 4.2:

- **LSC 4.2** introduced propagation-side language, effective Hamiltonian terms, weak phase modulation, and relativistic energy mapping.
- **LSC 5.5** introduced anisotropic detector response through a tensor-style detector structure.
- **LSC 6.0** unifies propagation and detector response while removing compact-object assumptions from the Gallium interpretation.

## 3. Observable Ansatz

The current clean LSC 6.0 observable equation is best written in first-order form:

```text
E_obs / E_emit = 1 + beta_cal + delta_G(Phi, E)
               + alpha_D A_mu_nu n^mu n^nu
               + O(delta^2)
```

where:

- `E_emit` is the emitted neutrino energy,
- `E_obs` is the reconstructed energy,
- `beta_cal` is an isotropic calibration baseline,
- `delta_G(Phi, E)` is an effective propagation-level correction,
- `A_mu_nu` is the anisotropic detector response tensor,
- `n^mu` is a normalized propagation or arrival-direction vector,
- `alpha_D` controls the detector-response amplitude.

This form separates the isotropic calibration offset from the anisotropic tensor contraction. That separation is important because a term proportional to `eta_mu_nu p^mu p^nu / E^2` would vanish in the massless limit and would not behave like an ordinary calibration baseline.

## 4. Propagation Factor

The propagation factor is defined phenomenologically:

```text
G(Phi, E) = 1 + delta_G(Phi, E) + O(delta_G^2)
```

with the consistency condition:

```text
lim_{Phi -> 0, alpha_LSC -> 0} G(Phi, E) = 1
```

In LSC 6.0, `delta_G` should not be interpreted as a large classical gravitational redshift. Natural solar-system gravitational effects are too small to directly account for percent-level Gallium deficits. The term is instead treated as an effective propagation parameter to be constrained by data.

## 5. Detector Tensor

The anisotropic response is represented by a symmetric detector tensor:

```text
Delta_D(theta, phi, t) = A_mu_nu n^mu n^nu
```

The tensor can encode:

- detector geometry,
- source-detector orientation,
- material response,
- unresolved reconstruction systematics,
- sidereal or angular modulation.

The model does not claim direct Ricci-tensor causation. A curvature-like basis may be useful mathematically, but LSC 6.0 treats the tensor as an effective detector-response object.

## 6. Gallium Event Rate

For gallium source experiments, a discrete source-line expression is more appropriate than a smooth-spectrum integral:

```text
N_obs = sum_i Phi_i P_ee(E_i) sigma(E_i) R_det(E_i)
```

For small reconstructed-energy shifts:

```text
Delta N / N ~= A_eff * Delta E / E
```

where `A_eff` is an experiment-dependent amplification factor. Since gallium capture cross sections rise rapidly with energy near the relevant source lines, a few-percent effective energy-response shift can produce a larger event-rate effect.

A simple phenomenological split is:

```text
Delta N / N ~= A_G * delta_G + A_D * alpha_D * Delta_D
```

The BEST-scale deficit is approximately:

```text
R_BEST ~= 0.79
Delta N / N ~= -0.21
```

The purpose of the LSC 6.0 parameterization is to explore whether a small propagation term plus a detector anisotropy term can reproduce this scale while keeping the detector-level shift in the range:

```text
|Delta E / E|_detector ~= 0.03 - 0.06
```

This is a working parameter range, not a fitted result.

## 7. External Constraints

### KATRIN

KATRIN strongly constrains universal distortions of the tritium beta spectrum. LSC 6.0 remains viable only if its dominant Gallium effect is not a universal emitted-energy shift:

```text
|delta_G + alpha_D Delta_D|_KATRIN << 10^-2
```

### IceCube

IceCube constrains large global modulation and Lorentz-violating signatures. LSC 6.0 therefore requires the direction-averaged anisotropic term to be small:

```text
<A_mu_nu n^mu n^nu>_sky ~= 0
```

while allowing local or angular anisotropy:

```text
A_mu_nu n^mu n^nu != 0
```

for specific directions, detector geometries, or sidereal phases.

## 8. Predictions

1. **Sidereal modulation**: a controlled source experiment should show a small orientation-dependent modulation if the anisotropic tensor term is physical.
2. **Detector dependence**: different detector technologies should reconstruct small but systematic offsets for comparable neutrino populations.
3. **Angular anisotropy**: the response should depend on the incoming direction through a tensor contraction.
4. **No universal KATRIN-scale distortion**: the effect should be suppressed or absent in beta-spectrum observables.

## 9. Limitations

LSC 6.0 is an effective model. It does not yet derive the detector tensor from first principles. The values of `alpha_D`, `delta_G`, tensor components, and amplification coefficients require global fitting.

The correct interpretation is:

```text
phenomenological proposal -> numerical tests -> experimental constraints -> possible model refinement
```

not:

```text
confirmed new physics
```

## 10. Next Research Steps

- Replace toy response parameters with a real likelihood model.
- Fit Gallium source data with discrete line energies and published cross sections.
- Add KATRIN null constraints as priors.
- Add IceCube angular constraints as a direction-averaged suppression condition.
- Prepare a longer arXiv-style manuscript with explicit parameter tables and reproducible notebooks.

