# LSC 6.2.1 Codex Workspace

Working package for the LSC 6.2.1 continuation.

This folder is intentionally separate from the 6.2.0 base theory. It contains:

- a small, reproducible data model for BEST, GALLEX and SAGE;
- a first-pass phenomenological fit to the extracted ratios;
- diagnostic simulations for geometry, source cross sections and zone splitting;
- unit tests;
- a generated PDF report.

## Build

```bash
cd "/home/l/the saga continue/6.2.1/codex"
python3 build.py
```

Outputs are written to `out/`.

## Model Status

This is an exploratory calibration layer, not a claim of confirmed new physics.
It uses published gallium source-experiment values as anchor points and reports
where the fit is stable and where it is not.

