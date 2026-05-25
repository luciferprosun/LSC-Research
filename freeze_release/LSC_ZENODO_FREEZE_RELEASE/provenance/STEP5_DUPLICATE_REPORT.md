# STEP 5 Duplicate Report

## Method

Duplicate detection was performed before and after migration using:

- filename repetition;
- SHA-256 exact-content grouping;
- review of repeated generated folders and PDFs.

Generated details:

- `provenance/STEP5_DUPLICATE_GROUPS.txt`
- `provenance/STEP5_DUPLICATE_FILENAMES.tsv`

## Summary

Exact duplicates were confirmed in the pre-STEP5 mixed layout. They were concentrated in:

- duplicated PBH-era legacy source files under both `LSC_core/simulations/legacy/neutrino-oscillations-pbh/` and `legacy/neutrino-oscillations-pbh/`;
- duplicated LSC 6.0 simulation files under `LSC_core/simulations/legacy/lsc60/` and `legacy/LSC-6.0/simulations/`;
- duplicated dataset and summary files under `LSC_core/datasets/`, `framework/data/raw/`, and `reports/`;
- duplicated LSC 6.3.0 PDF copies under `LSC_core/theory/` and `framework/papers/`;
- audit originals and extracted text that intentionally preserve equivalent content in separate audit forms.

## Action Taken

No scientific content was deleted.

The mixed pre-STEP5 folders were moved under:

`historical_archive/pre_step5_repository/`

This removes duplicate active paths from the repository root while preserving old content for lineage review.

## Representative Exact Duplicates

| SHA-256 class | Representative paths | Action |
|---|---|---|
| PBH legacy source duplicate | `LSC_core/simulations/legacy/neutrino-oscillations-pbh/src/analysis.py`; `legacy/neutrino-oscillations-pbh/src/analysis.py` | Preserved in historical archive. |
| LSC 6.3.0 PDF duplicate | `LSC_core/theory/LSC-6.3.0/LSC_6_3_0_UNIFIED_BEST2_UPDATE.pdf`; `framework/papers/LSC_6_3_0_UNIFIED_BEST2_UPDATE.pdf` | Preserved in historical archive. |
| Gallium dataset duplicate | `LSC_core/datasets/gallium-core/dataset.json`; `framework/data/raw/gallium_core_dataset.json` | Preserved in historical archive. |
| Gallium summary duplicate | `LSC_core/datasets/gallium-core/summary_report.md`; `reports/GALLIUM_SOURCE_SUMMARY.md` | Preserved in historical archive. |
| LSC 6.0 simulation duplicate | `LSC_core/simulations/legacy/lsc60/lsc60_gallium_response.py`; `legacy/LSC-6.0/simulations/lsc60_gallium_response.py` | Preserved in historical archive. |

## Remaining Intentional Duplicates

Some audit materials exist both as original files and extracted text. This is intentional:

- originals preserve source form;
- extracted text supports review and search.

These are classified as audit-format duplicates, not active scientific duplicates.

## Removal Status

No files were removed during STEP 5. Redundant active paths were collapsed by moving old mixed structures into the historical archive.

