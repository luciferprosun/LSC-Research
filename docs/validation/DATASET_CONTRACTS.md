# Dataset contracts

## Authority

`ValidationDatasetRegistry` in `src/lsc_kernel/validation/datasets.py` is the sole executable source of truth. Its deterministic serialization is `preregistration/validation_datasets.json`; `preregistration/datasets.json` is only a checksum-bound reference to it.

Every record fixes source identity, repository-relative path, SHA-256, version, quality grade, observable scope, uncertainty boundary, readiness role, data-exposure class, blindness level, allowed tests and prohibited tests. Every `DatasetContract` also freezes row selection, exclusions, transformations, units, missing-value policy, derived-field policy and provenance fields. Raw source files are read-only.

## Registered datasets

| ID | Objects | Grade | Role | Critical boundary |
|---|---:|:---:|---|---|
| `BEST` | 20 | B | primary gallium validation | 10 exposures x 2 zones; full covariance unavailable |
| `GALLEX_GNO` | 83 | B | gallium transfer | 65 solar + 18 Cr rows; Cr1/Cr2 preserved |
| `SAGE_CR51` | 12 | B | gallium transfer | 8 primary + 4 controls; isotope kept separate |
| `SAGE_AR37` | 11 | B | gallium transfer | 10 primary + Ar3-2 control |
| `GALLIUM_CROSS_SECTIONS` | 15 | B | model sensitivity | no model is designated correct/default |
| `KATRIN` | 2,500 | A | external constraint | 50x50 absolute chi-square grid; mapping missing |
| `ICECUBE` | 52 file records | C | external constraint | release-native confidence construction required |
| `BOREXINO` | 6 resource groups | B | `METHODOLOGY_CONTROL` | not direct gallium evidence |
| `DAYA_BAY` | 213 archive members | A | external conventional control | no direct LSC inference |
| `PROSPECT` | 76 ancillary files | A | external sterile control | preserve CLs construction |
| `STEREO` | 6 core tables | A | external sterile control | no Gaussian reinterpretation |
| `MICROBOONE` | 4 core products | A | external sterile control | preserve Combined Neyman-Pearson treatment |
| `BEST2_FUTURE` | 0 observations | E | future blind target | proposal only; no prediction values |

## BEST discrepancy policy

The outer-zone candidate rows sum to 1070 while the combined-source row reports 1069. The contract applies `PRESERVE_SOURCE_DISCREPANCY`: both source statements remain intact, neither replaces the other, and the discrepancy must be reported whenever candidate totals are used.

## Exposure and blindness

BEST, GALLEX/GNO, SAGE and other historical data are `MODEL_EXPOSED` and `NON_BLIND_HISTORICAL` relative to the recovered LSC 6.3.0 freeze. They are not represented as clean hold-outs. BEST-2 is `MODEL_PREEXISTING` and `FUTURE_BLIND`; its observed data remain absent.

## Integrity

The dry-run harness validates all 13 pinned files against their registry hashes before producing a plan. A missing or changed source becomes an explicit plan blocker. No loader may edit a raw source or silently impute `NOT_PUBLIC`, `UNRESOLVED` or missing fields.
