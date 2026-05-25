# Roadmap

## Phase A — Reproducibility Baseline (highest priority)

- [x] Create production computational layout (`data/loaders/likelihood/baselines/tests`)
- [x] Add lightweight null vs sterile baseline runner
- [ ] Finalize canonical Gallium dataset schema and validation checks
- [ ] Freeze benchmark input snapshots in `data/raw` with version tags

## Phase B — Statistical Validation

- [ ] Add covariance-aware chi2 implementation
- [ ] Add leave-one-out runner for all measurement points
- [ ] Add null-hypothesis and sterile-baseline comparison reports
- [ ] Add reproducible plot scripts for baseline residuals

## Phase C — Infrastructure Hardening

- [ ] Add CI workflow for baseline smoke test and schema checks
- [ ] Block accidental imports from `archive/` and `legacy/` paths
- [ ] Add deterministic environment bootstrap (minimal dependencies)

## Phase D — Exploratory Models (only after A+B)

- [ ] Connect exploratory LSC correction modules behind explicit feature flags
- [ ] Keep exploratory outputs segregated from validated baseline outputs
- [ ] Require baseline deltas and LOO checks in every exploratory report
