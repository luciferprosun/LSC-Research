# LSC Zenodo Upload Structure

## Upload Status

Prepared locally only. No upload has been performed.

## Recommended Upload Contents

| Path | Include | Purpose |
|---|---|---|
| `README.md` | yes | Package overview and claim boundary. |
| `metadata/LSC_ZENODO_METADATA_FINAL.json` | yes | Zenodo metadata draft. |
| `metadata/CITATION.cff` | yes | Citation metadata. |
| `canonical/` | yes | Frozen canonical core and equations. |
| `validation/` | yes | Validation infrastructure. |
| `implementation/` | yes | Future validation templates. |
| `provenance/` | yes | Source inventory, claim classification, migration and duplicate reports. |
| `data_requirements/` | yes | Missing-data and request-for-data materials. |
| `release/` | yes | Final abstract, release notes, keywords, upload structure, checklists. |
| `pdfs/` | yes | PDF renderings of frozen documents. |
| `audits/codex_reports/` | yes | Step reports and re-audit trail. |
| `audits/extracted/` | optional | Searchable external audit extracts. |
| `PACKAGE_MANIFEST.csv` | yes | Package-level manifest. |
| `PACKAGE_CHECKSUMS.sha256` | yes | Package-level checksums. |

## Not Recommended For Zenodo Upload Without Review

- Full `historical_archive/` tree, unless a larger historical-preservation deposit is explicitly desired.
- Recursive ZIP files from old releases.
- Any unrelated MHLM/AOIA/MDLH material.

## Human Gate Before Upload

Before upload, confirm:

- final authorship and affiliations;
- license;
- DOI relationship to existing records;
- whether this is uploaded as a new version of record `20037838`;
- final file set;
- checksum verification;
- claim language.

