# Frozen gallium-capture interpolation policy

Status: **FROZEN BEFORE ALPHA0 DETERMINATION**

## Scientific source

The production payload is the best-estimate energy/cross-section table from John N. Bahcall, *Gallium Solar Neutrino Experiments: Absorption Cross Sections, Neutrino Spectra, and Predicted Event Rates*, Phys. Rev. C 56, 3391 (1997), DOI `10.1103/PhysRevC.56.3391`. The source explicitly instructs readers to use a cubic-spline fit to the tabulated cross sections as a function of energy and reports that the table reproduces standard-spectrum best estimates to 1% or better.

The newer calculation by Elliott, Gavrin, and Haxton, Phys. Rev. C 108, 035502 (2023), DOI `10.1103/PhysRevC.108.035502`, supplies the frozen `51Cr` and `37Ar` source-line energies and branchings. It is used as a line-input source and benchmark, not as an undocumented continuous total-cross-section function.

## Frozen numerical representation

- Data scenario: Bahcall 1997 `Best` table only.
- Interpolant: piecewise cubic spline in linear `E` and linear `sigma`.
- Endpoint condition: natural, meaning second derivative zero at 0.240 and 30.000 MeV.
- Interior continuity: `C2`.
- Derivative: analytic first derivative of the frozen cubic polynomial on the containing interval.
- Extrapolation: prohibited.
- Canonical energy unit: MeV.
- Canonical cross-section unit: `10^-46 cm^2`.
- Arithmetic: IEEE-754 binary64.

Bahcall specifies the cubic-spline family but not an endpoint condition. The natural endpoint condition is therefore an explicit `NUMERICAL_REPRESENTATION_CONVENTION`, selected before any LSC parameter fit. It does not use gallium deficit outcomes. On the complete frozen `51Cr`/`37Ar` line hull, natural and not-a-knot splines agree in the calculated logarithmic derivative to numerical precision; PCHIP is retained only as a sensitivity comparison and is not a selectable production model.

## Domain and fail-closed behavior

The payload domain is `[0.240, 30.000] MeV`. Production A2 evaluation is authorized only for source lines in the frozen `51Cr` and `37Ar` payload. A value outside the table domain, a non-finite value, a non-positive interpolated cross section, an unknown isotope, an altered authoritative line set, or any extrapolation request returns `FAIL_CLOSED_UNSUPPORTED_DOMAIN`.

The spline is positive and finite over the complete payload domain under a deterministic dense-grid and interval-extrema audit. This numerical audit is not a new experimental measurement.

## Derivative limitation

The publication validates the spline representation for cross-section/rate reproduction; it does not publish an uncertainty guarantee for `d ln sigma / d ln E`. Consequently, `F_m` is a deterministic derivative of this explicitly frozen representation, not a separately measured observable. Cross-section-model dependence remains a scientific limitation and the production code must report the exact payload hash.

## Linear-response analysis boundary

There is no source-derived strict theory bound for `alpha_0`. Three distinct bounds are preserved:

1. `THEORY_BOUND`: unavailable.
2. `NUMERICAL_STABILITY_BOUND`: the dilated line energies must remain in the cross-section payload and `1 + alpha_0 F_m(E)` must remain positive.
3. `PREREGISTERED_ANALYSIS_BOUND`: for every frozen `51Cr`/`37Ar` line, the relative difference between the linear response and the exact finite dilation of the frozen spline must not exceed 1%. This gives `-0.06137569484389956 <= alpha_0 <= 0.09541395625505644`.

The 1% threshold is a pre-fit analysis convention tied to the source table's stated reproduction scale. It is not presented as a fundamental physical constant. It is frozen before observing the alpha determination outcome and may not be widened after a boundary result.
