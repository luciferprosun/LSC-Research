# LSC Data Report

## Public data retrieved
- arXiv PDFs downloaded for BEST, gallium anomaly review papers, and related source-experiment papers.
- InspireHEP query results saved and normalized in `experimental/inspire_literature_links.json`.
- Zenodo query results saved and filtered in `experimental/zenodo_related_records.json`.
- NNDC public pages and PDFs saved in `public_sources/nndc/`.

## Structured outputs created
- `experimental/best_results_summary.json`
- `experimental/gallium_source_experiments.csv`
- `experimental/inspire_literature_links.json`
- `experimental/zenodo_related_records.json`
- `theoretical/ga71_cross_sections.csv`
- `theoretical/nndc_ga71_notes.json`
- `geometry/best_geometry.json`
- `contacts/contact_targets.csv`
- `contacts/lsc_data_request_template.txt`
- `contacts/sent_requests_log.csv`

## What was successfully extracted
- BEST inner and outer measured-to-predicted ratios: `Rin = 0.79 +/- 0.05`, `Rout = 0.77 +/- 0.05`.
- BEST measured production rates, predicted rates, Cr-51 source activity, and detector geometry.
- Historical source-calibration summary for SAGE, GALLEX, and BEST from the 2023 gallium anomaly review.
- Multiple published Ga-71 cross-section estimates for Cr-51 and Ar-37 source analyses.
- Public institutional / author contact emails with source URLs.

## What still requires manual contact
- Full numeric covariance matrices for BEST were not found as a public numeric table in the downloaded papers; the public paper gives the covariance formula and uncertainty components instead.
- Zone-by-zone raw event-count tables were not located as a clean public machine-readable table.
- Any internal calibration spreadsheets or unpublished detector bookkeeping still require collaboration response.

## Missing or incomplete items
- Public numeric covariance matrix: missing from current public extraction set.
- Confirmed public machine-readable BEST event-count tables: not found in the downloaded sources.
- Direct NNDC `71Ga(nu,e)` tabulation via Sigma endpoint: not found; ENSDF references were saved instead.

## Verification checklist
- [x] BEST inner/outer ratio `R` available
- [ ] Full numeric covariance matrix available publicly
- [x] Cr-51 source activity available
- [x] Ga-71 cross-section estimates available
- [x] Detector geometry available
- [x] Email send confirmations available

## Notes on Zenodo
- The public Zenodo query returned one directly relevant record, `The Gallium Anomaly` (`10.5281/zenodo.17647685`).
- No relevant `.csv`, `.txt`, or `.dat` payloads were exposed in the filtered BEST/gallium-anomaly records returned by the public query used here.
