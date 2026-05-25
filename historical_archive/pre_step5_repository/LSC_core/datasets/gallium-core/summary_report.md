# Codex Data Report: BEST, GALLEX, SAGE

Generated: 2026-04-29

## Scope

This package is a structured starter dataset for gallium neutrino source-experiment modeling. It covers:

- BEST with a 51Cr source and two nested gallium zones.
- GALLEX with two 51Cr source calibrations.
- SAGE with 51Cr and 37Ar source calibrations.

The main machine-readable file is `dataset.json`. Missing values are represented as `null` or listed in each experiment's `extraction_status.missing`.

## Files

- `dataset.json` - structured dataset with geometry, source lines, measured ratios, cross sections and references.
- `loader.py` - small Python helper with `load_dataset()` and `get_experiment("BEST")`.
- `summary_report.md` - this report.
- `codex data.pdf` - PDF rendering of this report.

## Extracted Numerical Values

### Common Source Lines and Cross Sections

The line data are normalized to MeV and cm^2.

| Isotope | Energy MeV | Intensity | Cross section cm^2 |
|---|---:|---:|---:|
| 51Cr | 0.7473 | 0.8163 | 6.08e-45 |
| 51Cr | 0.7521 | 0.0849 | 6.15e-45 |
| 51Cr | 0.4272 | 0.0895 | 2.67e-45 |
| 51Cr | 0.4320 | 0.0093 | 2.71e-45 |
| 37Ar | 0.8110 | 0.9020 | 7.01e-45 |
| 37Ar | 0.8130 | 0.0980 | 7.03e-45 |

These values come from sterile-neutrino review tables that cite Bahcall-interpolated gallium capture cross sections.

### BEST

Geometry extracted:

- Inner gallium zone: sphere, diameter 1.335 m, radius 0.6675 m, 7.4691 +/- 0.0631 metric tons of Ga.
- Outer gallium zone: cylinder, diameter 2.18 m, height 2.345 m, 39.9593 +/- 0.0024 metric tons of Ga.
- Approximate average baselines used in review literature: inner about 0.5 m, outer about 1.1 m.

Source extracted:

- 51Cr source activity: 3.414 +/- 0.008 MCi at 2019-07-05 14:02 Moscow time.
- Active core: 26 irradiated Cr disks in a stainless-steel cylinder, radius 0.043 m and height 0.108 m, with about 0.03 m tungsten-alloy shielding.

Measured results extracted:

| Zone | Production rate atoms/day | R |
|---|---:|---:|
| Inner | 54.9 +2.5/-2.4 stat +/- 1.4 syst | 0.79 +/- 0.05 |
| Outer | 55.6 +2.7/-2.6 stat +/- 1.4 syst | 0.77 +/- 0.05 |
| Outer/inner | null | 0.97 +/- 0.07 |

Completeness:

- Complete enough for first-pass two-zone rate modeling.
- Missing full exposure-by-exposure extraction table, counter efficiencies and covariance matrix.
- No figure digitization was performed.

### GALLEX

Geometry extracted:

- Cylindrical tank, approximately 8.0 m high and 3.8 m diameter.
- 53.5 m^3 GaCl3-HCl solution, containing 30.3 metric tons of gallium.
- Source position is described as a reentrant tube in the center of Tank A; exact coordinates are not yet extracted.

Source extracted:

- 51Cr Cr1: 1.714 +/- 0.036 MCi.
- 51Cr Cr2: 1.868 +/- 0.073 MCi.

Measured results extracted:

| Result convention | R |
|---|---:|
| Cr1 final 1998 | 1.01 +0.12/-0.11 |
| Cr2 final 1998 | 0.84 +0.12/-0.11 |
| Combined final 1998 | 0.93 +/- 0.08 |
| Cr1 common gallium-anomaly table | 0.953 +/- 0.11 |
| Cr2 common gallium-anomaly table | 0.812 +/- 0.10 |
| Combined GALLEX reanalysis 2010 | 0.882 +/- 0.078 |

Cross-section value extracted:

- Integrated 51Cr gallium capture cross section reported in the GALLEX final-results discussion: 5.81e-45 cm^2 with +2.1e-46/-1.6e-46 cm^2 uncertainty.

Completeness:

- Good for calibration-ratio comparisons.
- Missing exact source coordinates, exposure-level event table and detector response covariance.
- The dataset intentionally preserves both final-paper and later/reanalysis conventions because they are not numerically identical.

### SAGE

Geometry extracted:

- Source-exposure detector approximation: cylinder radius 0.7 m, height 1.47 m.
- Source height above base: 0.72 m.
- Source exposure gallium mass: 13.1 metric tons.

Source extracted:

- 51Cr source: 0.517 +/- 0.006 MCi.
- 37Ar source: 0.409 +/- 0.002 MCi.

Measured results extracted:

| Source | Production rate atoms/day | R |
|---|---:|---:|
| 51Cr | 14.0 +/- 1.7 | 0.95 +/- 0.12 |
| 37Ar | 11.0 +/- 1.5 | 0.79 +/- 0.10 |

An alternate commonly reported 37Ar value is also stored: 0.791 +/- 0.084.

Completeness:

- Good for first-pass single-zone calibration modeling.
- Missing full run-by-run source exposure table, 37Ar impurity table and counter-level likelihood inputs.
- No figure digitization was performed.

## References Used

- BEST PRL: `10.1103/PhysRevLett.128.232501`
- BEST detailed PRC / arXiv: `10.1103/PhysRevC.105.065502`, arXiv `2109.11482`
- GALLEX first source result: `10.1016/0370-2693(94)01586-2`
- GALLEX final source results: `10.1016/S0370-2693(97)01562-1`
- GALLEX reanalysis: `10.1016/j.physletb.2010.01.030`
- SAGE 51Cr: `10.1103/PhysRevLett.77.4708`
- SAGE 37Ar: `10.1103/PhysRevC.73.045805`
- Sterile-neutrino white paper / CERN copy: arXiv `2203.07323`
- Gallium anomaly review: `10.1016/j.ppnp.2023.104082`

## What Is Complete vs Missing

Complete enough for:

- Loading source lines and cross sections in normalized units.
- Building simple rate-ratio comparisons for BEST, GALLEX and SAGE.
- Initial sterile-neutrino oscillation toy modeling using reported `R` values.

Not complete enough for:

- Reproducing official likelihoods.
- Reproducing extraction-by-extraction GALLEX/SAGE/BEST analyses.
- Fitting detector systematics with covariance matrices.
- Plot digitization from figures.

Next data work:

- Pull the full PDFs into a `sources/` subfolder.
- Extract exposure tables with `pdftotext` or `tabula/camelot` where possible.
- Add covariance/systematics tables as separate JSON objects.
- Add figure-digitized points only with explicit provenance and digitization uncertainty.
