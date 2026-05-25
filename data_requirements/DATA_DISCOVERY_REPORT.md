# Data Discovery Report

Date: 2026-05-08  
Scope: accessible local storage under `/home/l` with emphasis on research folders.

## 1) Search policy

Search terms:

- BEST, GALLEX, SAGE
- gallium, neutrino, oscillation, anisotropy

File types scanned:

- `csv`, `json`, `txt`, `md`, `ipynb`, `py`

Safety rule:

- no deletion performed,
- report-only indexing.

## 2) Primary datasets (highest value)

1. `data/raw/gallium_core_dataset.json`  
   Source copy from `LSC/datasets/gallium-core/dataset.json`.
2. `LSC/datasets/gallium-core/dataset.json`
3. `LSC/datasets/gallium-core/summary_report.md`
4. `LSC/simulations/legacy/lsc60/lsc60_gallium_response.csv`
5. `archive/theory-legacy/LSC/LSC-6.0/simulations/outputs/lsc60_gallium_response.csv`

## 3) Useful scripts and notebooks discovered

- `loaders/gallium_loader.py` (new production loader)
- `LSC/datasets/gallium-core/loader.py` (legacy source loader)
- `LSC/simulations/legacy/lsc60/lsc60_gallium_response.py`
- `notebooks/gallium_baseline_template.ipynb` (new template)
- `neutrino-oscillations-pbh/src/*.py` (legacy reference branches)

## 4) External duplicate-rich zones (not production)

Large mirrors and historical duplicates were found in:

- `/home/l/github-audit/*`
- `/home/l/the saga continue/*`
- `/home/l/Desktop/prace dark neutrino */*`

These are valuable as provenance snapshots, but should not be runtime sources
for production computations.

## 5) Recommended source-of-truth map

- Production dataset root: `data/raw/`
- Production scripts: `loaders/`, `likelihood/`, `baselines/`, `scripts/framework/`
- Legacy references only: `archive/`, `LSC/simulations/legacy/`, external mirrors.

## 6) Missing artifacts

Still missing for rigorous benchmark reproduction:

- full covariance matrices for all Gallium source runs,
- fully normalized machine-readable BEST/GALLEX/SAGE unified table,
- standardized sterile-baseline L/E mapping inputs per measurement point.

Placeholders and schema are now in place to ingest these once available.
