# Baseline model registry

The registry preserves the historical model labels from the frozen protocol:

| Frozen ID | Model | Fit boundary |
|---|---|---|
| M0 | null / published baseline | no fitted model parameter |
| M1 | scalar normalization | calibration subset only |
| M2 | cross-section/source systematics | registered model/prior only |
| M3 | sterile-neutrino 3+1 | calibration subset or external published surface |
| M4 | detector/systematic benchmark | calibration subset only |
| M5 | frozen LSC trace-only | no fit or refit |
| M6 | frozen full trace + traceless LSC | no fit or refit |

Modern stable aliases map without renumbering: `M_NULL` to M0, `M_CONSTANT_DEFICIT` to M1, `M_CROSS_SECTION_VARIANT` to M2, `M_STERILE_3P1` to M3, and experiment-normalization, detector-systematic and hierarchical variants to named M4 submodels.

Each record freezes hypothesis, equations, parameters, free/fixed status, training/evaluation boundary, complexity count, likelihood prerequisites, comparison metrics and provenance. M5/M6 appear to preserve the historical hierarchy; they are not fit-capable baseline targets.

The `NoRefitPolicy` permits preregistered baseline fitting and nuisance profiling while raising `FrozenModelRefitForbidden` for every attempt to fit, refit, optimize or calibrate frozen LSC parameters.
