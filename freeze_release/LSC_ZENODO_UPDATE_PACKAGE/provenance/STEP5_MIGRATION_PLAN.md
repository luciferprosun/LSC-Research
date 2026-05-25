# STEP 5 Migration Plan - LSC Pre-BEST-2 GitHub Freeze Engineering

## Scope

Repository: `LSC-Research`

This migration is repository engineering only. It does not extend LSC, introduce new equations, create LSC 6.4, upload to Zenodo, push to GitHub, or modify any other project.

## Current State Before Migration

The pre-migration repository tree is recorded in:

- `provenance/PRE_STEP5_TREE.txt`
- `provenance/PRE_STEP5_FILE_HASHES.sha256`

The current repository contains a mixed historical layout:

- `LSC_core/`
- `framework/`
- `legacy/`
- `archive/`
- `docs/`
- `reports/`
- root authority/report files

Several exact duplicate files exist across `LSC_core/`, `framework/`, `legacy/`, and `reports/`. These are not deleted silently.

## Target Structure

The final freeze-stage structure will use:

```text
LSC-Research/
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── MANIFEST.csv
├── CHECKSUMS.sha256
├── canonical/
├── validation/
├── implementation/
├── freeze_release/
├── audits/
├── provenance/
├── docs/
├── data_requirements/
├── historical_archive/
└── tools/
```

## Migration Decisions

| Source | Target | Role | Reason |
|---|---|---|---|
| STEP 1 canonicalization outputs | `canonical/` | canonical | Authoritative pre-BEST-2 canonical core, active equation set, freeze boundary, lineage, deprecated component registry. |
| STEP 2 validation infrastructure outputs | `validation/` | validation | Authoritative validation protocol, M0-M6 hierarchy, M4 competitor, covariance policy, external veto checklist, preregistration policy, risk matrix. |
| STEP 3 implementation outputs | `implementation/` | implementation | Authoritative templates and procedures for data requirements, model specifications, M4 schema, covariance placeholders, LOO, transfer, BEST-2 preregistration. |
| STEP 4 release-prep outputs | `freeze_release/` | release | Local release-candidate materials, release notes draft, Zenodo metadata draft, request-for-data, final review checklist. |
| External audits original/extracted | `audits/` | audit | Preserves Claude/Gemini/DeepSeek/Kimi/reconnaissance critique layers. |
| Source inventory, manifest, checksums, migration logs | `provenance/` | provenance | Reproducibility and lineage tracking. |
| Data request and public-data reconnaissance materials | `data_requirements/` | data requirement | Centralizes missing-data requests and validation blockers. |
| Existing pre-STEP5 mixed folders (`LSC_core/`, `framework/`, `legacy/`, `archive/`, old `reports/`) | `historical_archive/pre_step5_repository/` | historical | Preserves old content without leaving active duplicate paths in the freeze-stage root. |
| Existing root authority files (`AUTHORITY_SCOPE.md`, `COMPUTE_LIMITATIONS.md`, `DATA_DISCOVERY_REPORT.md`, `ROADMAP.md`) | `docs/repository_authority/` or `data_requirements/` | documentation/data | Keeps legacy authority and limitation reports accessible without cluttering root. |
| Duplicate copies identified by checksum | `historical_archive/duplicates_removed/` report only; no silent deletion | redundant/historical | Exact duplicates are documented. Content is preserved unless a future human review approves removal. |

## Duplicate Handling Policy

Confirmed duplicates are not silently deleted in this step. One active copy is kept in the relevant final folder where appropriate. Redundant old copies remain only inside `historical_archive/pre_step5_repository/` and are listed in `provenance/STEP5_DUPLICATE_REPORT.md`.

## Forbidden Actions

This migration will not:

- publish to GitHub or Zenodo;
- create a new repository;
- alter MHLM, AOIA, MDLH, or other projects;
- introduce new scientific claims;
- introduce new equations;
- remove scientific content without a provenance record.

