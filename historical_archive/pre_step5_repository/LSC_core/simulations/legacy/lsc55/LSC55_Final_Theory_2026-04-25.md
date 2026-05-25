---
title: "LSC 5.5: Unified Theory of Gravitationally Modulated Neutrino Propagation and Tensor Energy Reconstruction"
author: "LuciferSun, working redaction"
date: "2026-04-25"
geometry: margin=2.2cm
fontsize: 11pt
lang: en-US
toc: true
toc-depth: 2
---

# Abstract

We present a curated and integrated final working version of the `LSC 5.5`
framework, unifying two previously separate lines of development: `LSC 4.2
ULTRA`, which describes gravitational modulation of neutrino oscillations near
compact environments and effective primordial black hole (PBH) backgrounds, and
`LSC 5.0@`, which interprets part of the neutrino-anomaly landscape as a
consequence of nonlinear energy reconstruction in the detector. In the final
version the central claim is that observed anomalies may arise from the joint
action of curved-spacetime propagation and anisotropic detector response. The
detection effect is parameterized by a tensor `D_{\mu\nu}`, extending the scalar
energy-shift parameter `\delta` into a directional and geometric object. The
model does not require a dark-neutrino sector as the main explanation of the
anomalies; instead, it preserves a falsifiable phenomenological structure with
testable predictions involving energy dependence, anisotropy, and experiment-to-
experiment response differences. This document organizes the formalism, states
its regime of validity, and records the main changes relative to earlier
versions.

# 1. Introduction

Neutrino physics already possesses a strong and experimentally successful
description of flavor oscillations. Nevertheless, several classes of anomalies
have been interpreted either as evidence for beyond-standard-model states or as
manifestations of incompletely modeled measurement effects. Sterile-neutrino
interpretations belong to the first class; imperfect energy reconstruction and
detector response belong to the second.

Within the LSC family of documents, two major tracks emerged:

1. `LSC 4.2 ULTRA`: an additional gravitational modulation of neutrino
   propagation, especially in environments with an effective PBH contribution.
2. `LSC 5.0@`: a nonlinear energy-reconstruction effect capable of producing
   nontrivial deviations in observed event counts.

`LSC 5.5` merges these tracks. The final version no longer relies on the claim
that PBHs are the primary energy source of the signal, nor on the requirement of
introducing a new particle as the central degree of freedom. Its theoretical
backbone is instead the combination

\[
\text{curved-spacetime propagation}
\;+\;
\text{resonant geometric modulation}
\;+\;
\text{nonlinear tensor energy reconstruction}.
\]

# 2. Scope and status of the final version

The final version is an effective and phenomenological theory. This means:

- it is not claimed to be a complete fundamental theory of gravity and
  measurement,
- it uses an effective operator `H_{\mathrm{LSC}}`,
- it treats the tensor `D_{\mu\nu}` as an effective detector-response object
  tied to local geometry and direction dependence,
- it prioritizes a coherent chain from assumption to equation to observable over
  maximal ontological ambition.

Accordingly, the model should be judged primarily by:

- dimensional consistency and sensible limits,
- testable predictions,
- its ability to explain classes of anomalies without unnecessary extra states.

# 3. Effective propagation formalism

We describe flavor evolution with the effective Hamiltonian

\[
H_{\mathrm{eff}} =
H_{\mathrm{vac}} +
H_{\mathrm{matter}} +
H_{\mathrm{grav}} +
H_{\mathrm{LSC}}.
\]

The vacuum term is

\[
H_{\mathrm{vac}} = \frac{1}{2E} U M^2 U^\dagger,
\]

where `U` is the mixing matrix and `M^2` is the diagonal mass-squared matrix.

The matter term is

\[
H_{\mathrm{matter}} = \mathrm{diag}(V_e,0,0),
\qquad
V_e = \sqrt{2} G_F n_e(r).
\]

The minimal gravitational contribution is written as

\[
H_{\mathrm{grav}} = \frac{E}{c^2}\Phi(r),
\qquad
\Phi(r) = -\frac{GM}{r}.
\]

The effective `LSC` operator parameterizes the additional geometric modulation
associated with PBH-like environments:

\[
H_{\mathrm{LSC}} =
\alpha_{\mathrm{LSC}}
\left(\frac{GM}{r c^2}\right)
F(E)\,\Xi.
\]

Here:

- `\alpha_{\mathrm{LSC}}` is a dimensionless coupling,
- `F(E)` sets the energy scaling,
- `\Xi` is a flavor-space operator structure.

For the minimal high-energy version,

\[
F(E)=\frac{E}{E_0},
\qquad
E_0 = 1\,\mathrm{PeV}.
\]

The required limits are:

1. `H_{\mathrm{LSC}} \to 0` as `M \to 0` or `r \to \infty`,
2. the standard oscillation picture is recovered in the flat-space limit,
3. the new term can remain subdominant at low energy.

# 4. Resonance condition and PBH modulation

The resonance branch preserves the MSW-like insight that even a weak additional
potential may strongly alter conversion probabilities if it enters the correct
kinematic regime. In an effective two-state reduction we write

\[
\Delta m^2 \cos(2\theta)
=
2E\left(V_{\mathrm{matter}} + V_{\mathrm{LSC}}\right),
\]

with

\[
V_{\mathrm{LSC}} =
\alpha_{\mathrm{LSC}}
\left(\frac{GM}{r c^2}\right)F(E).
\]

In this form the model does not assert that PBHs inject energy into the
neutrino. They instead act as modulators of phase, mixing, and local resonance
conditions. That interpretive shift is one of the main cleanups relative to more
speculative earlier versions.

The oscillation probability is treated effectively as

\[
P_{\alpha\to\beta}(L,E)
=
\sin^2(2\theta_{\mathrm{eff}})
\sin^2\left(
\frac{\Delta m^2_{\mathrm{eff}}L}{4E}
\right),
\]

where `\theta_{\mathrm{eff}}` and `\Delta m^2_{\mathrm{eff}}` absorb the
corrections induced by `H_{\mathrm{grav}} + H_{\mathrm{LSC}}`.

# 5. Energy-reconstruction model

The second pillar of the theory concerns measurement rather than propagation.
In `LSC 5.0@` the core ansatz was

\[
E_{\mathrm{true}} = E_{\mathrm{obs}}(1+\delta),
\]

with `\delta` a small correction parameter. This is useful as a first-order
approximation but does not encode direction dependence, local geometry, or
tensor structure.

The final version upgrades this to

\[
\Delta_D = D_{\mu\nu} p^\mu p^\nu,
\]

\[
E_{\mathrm{true}} =
E_{\mathrm{obs}}\left(1+\alpha_D \Delta_D\right),
\]

where:

- `p^\mu` is the neutrino four-momentum,
- `D_{\mu\nu}` is a symmetric detector-response tensor,
- `\alpha_D` sets the detector-coupling scale.

The scalar limit is recovered by

\[
D_{\mu\nu} = \delta\,\eta_{\mu\nu}
\quad \Rightarrow \quad
\Delta_D \propto \delta.
\]

This extension is useful because it:

1. admits anisotropy,
2. allows a geometric interpretation of reconstruction bias,
3. reduces to the earlier scalar model when the extra structure is switched off.

# 6. Event rate and amplification of a small bias

The observed event count is written as

\[
N_{\mathrm{obs}} =
\int dE\,
\Phi(E)\,
P_{\alpha\to\beta}(E)\,
\sigma(E)\,
R_{\mathrm{det}}(E),
\]

where `R_{\mathrm{det}}(E)` encodes the detector response.

If the relevant cross section scales approximately as

\[
\sigma(E) \propto E^2,
\]

then a small energy bias can be amplified at the level of event counts. To first
order,

\[
\frac{\Delta N}{N}
\approx
\frac{\partial\ln\Phi}{\partial\ln E}\frac{\Delta E}{E}
+
\frac{\partial\ln P}{\partial\ln E}\frac{\Delta E}{E}
+
\frac{\partial\ln\sigma}{\partial\ln E}\frac{\Delta E}{E}.
\]

Because `\partial \ln \sigma / \partial \ln E \simeq 2`, even a few-percent
energy reconstruction shift may become phenomenologically important after
integration. This is the core mechanism behind the gallium-anomaly part of the
framework.

# 7. Coupling geometry to detector response

The final version assumes that propagation and detection should not be modeled as
completely unrelated sectors. The simplest effective bridge is

\[
D_{\mu\nu} =
a\,\eta_{\mu\nu}
+ b\,h_{\mu\nu}
+ c\,R_{\mu\nu},
\]

where:

- `\eta_{\mu\nu}` is the Minkowski metric,
- `h_{\mu\nu}` is a local geometric perturbation,
- `R_{\mu\nu}` is the Ricci tensor,
- `a`, `b`, `c` are effective coefficients.

This equation is not yet a first-principles derivation. It is, however, a useful
working ansatz because it:

- reduces to the scalar model in the flat limit,
- permits anisotropic detector effects,
- makes later data-driven fitting possible.

# 8. Covariant formulation

An effective covariant Lagrangian density for the integrated model can be
written as

\[
\mathcal{L}_{\mathrm{tot}}
=
\sqrt{-g}
\left[
i\bar{\psi}\gamma^\mu \nabla_\mu \psi
- m_{\mathrm{eff}}\bar{\psi}\psi
- G_D\,\bar{\psi}\gamma^\mu D_{\mu\nu}\gamma^\nu\psi
\right].
\]

The three terms represent:

- neutrino propagation in curved spacetime,
- an effective mass or phase correction,
- coupling to the detector-response tensor.

This formulation remains effective rather than fundamental, but it places the
model into a consistent covariant language while preserving the distinction
between propagation physics and measurement physics.

# 9. Application to two anomaly classes

## 9.1. Gallium-type anomalies

At low energy the reconstruction mechanism may dominate. In this regime the
tensor generalization of `LSC 5.0@` is more central than the PBH resonance
mechanism.

The main statement is:

- a small systematic mapping `E_{\mathrm{obs}} \to E_{\mathrm{true}}` may
  generate a much larger shift in event counts once the cross section and
  detector response are folded into the calculation.

## 9.2. TeV-PeV events

At high energy the gravitational and resonant branches may become more relevant.
In this regime the model predicts:

- energy-dependent modulation,
- possible directional dependence,
- localized enhancement of flavor conversion inside a narrow parameter window.

The `KM3-230213A` event should be treated as a case study rather than as the
single foundation of the theory. The final version deliberately avoids claiming
that the model already explains the entire energy budget of such an event.

# 10. Testable predictions

The framework yields several classes of falsifiable predictions:

1. event-count anomalies should show nonlinear energy dependence,
2. some configurations may generate anisotropy through `D_{\mu\nu}`,
3. different detectors may reconstruct similar neutrino populations with
   systematic offsets,
4. high-energy anomalies may appear as resonance windows rather than smooth
   distortions,
5. the tensor formulation can be falsified if directional correlations are
   absent where the model predicts them.

# 11. Limitations

The main limitations are:

- `H_{\mathrm{LSC}}` is still an effective operator, not a microscopically
  derived fundamental interaction,
- `D_{\mu\nu}` is still an effective parameterization,
- a full global fit across all experiments has not yet been performed,
- the connection to a realistic PBH population remains to be quantitatively
  constrained,
- the dark-neutrino branch is not required for the mainline and is therefore not
  retained as the central mechanism here.

# 12. Changes relative to earlier versions

This section records the main editorial and physical changes.

## 12.1. Relative to `LSC 3.5` and early `darkNeutrino`

- information-theoretic and philosophical language was removed from the
  mainline,
- the dark-neutrino sector is no longer treated as mandatory,
- only those ideas that can be rewritten in terms of effective Hamiltonians and
  observables are retained.

## 12.2. Relative to `PBHRM 3.3`

- the PBH-regulator motif is preserved in weakened and cleaner form,
- strongly speculative environmental claims were removed from the core theory,
- the emphasis shifts from regulatory language to a propagation-and-detection
  framework.

## 12.3. Relative to `LSC 4.2 ULTRA`

- the `H_{\mathrm{eff}}` formalism is preserved,
- PBHs are reframed as resonance and phase modulators rather than direct energy
  sources,
- the `QUE` branch is not retained in the final mainline because it is less
  constrained and less clearly testable.

## 12.4. Relative to `LSC 5.0@`

- the central energy-reconstruction mechanism is preserved,
- the scalar parameter `\delta` is upgraded to the tensor `D_{\mu\nu}`,
- propagation and measurement are explicitly separated before being coupled.

## 12.5. Relative to `LSC 5.5`

- the integrated geometry-plus-detection idea is preserved,
- the formal status is clarified: not every equation is a first-principles
  derivation,
- the discussion of limits, interpretation, and testability is strengthened,
- duplicates and over-strong interpretive claims are removed.

# 13. Minimal next-step program

To move from this working version toward a stronger preprint, the next tasks are:

1. dimensional and scale analysis for `\alpha_{\mathrm{LSC}}` and `\alpha_D`,
2. selection of one explicit flavor-space choice for `\Xi`,
3. order-of-magnitude estimates for `BEST`, `SAGE`, and `GALLEX`,
4. a parameter table summarizing the observationally allowed ranges,
5. a simple scan or fit demonstrating when the effect becomes measurable.

# 14. Conclusion

The final `LSC 5.5` version presents one coherent effective theory in which
neutrino anomalies may arise from the combination of modified propagation in
curved spacetime and nonlinear, direction-dependent energy reconstruction in the
detector. The main advance relative to earlier versions is the cleanup of
unnecessary extra entities and conflicting interpretations, together with a
clearer separation between physical claims and effective parameterizations.

In this form the model is suitable as the core of a working preprint. Its next
stage should focus less on adding new ontological layers and more on parameter
control, scale estimates, and quantitative comparison with data.
