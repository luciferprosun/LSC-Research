---
title: "Kodeks STEP 5 - GitHub Freeze Engineering"
subtitle: "LSC Pre-BEST-2 Repository Closure and Release Preparation"
date: "2026-05-25"
---

# 1. Executive Summary

STEP 5 reorganized the local `LSC-Research` repository into a clean pre-BEST-2 freeze-stage structure.

This was repository engineering only. No new physics, equations, tensor structures, particle claims, or LSC 6.4 material were introduced. No GitHub push and no Zenodo upload were performed.

The repository now separates active canonical material, validation infrastructure, implementation templates, release-preparation files, audits, provenance, data requirements, and historical/noncanonical material.

# 2. Repository Before/After Structure

## Before

The pre-STEP5 repository root contained mixed active, framework, legacy, archive, and report paths:

```text
LSC_core/
framework/
legacy/
archive/
docs/
reports/
README.md
LICENSE
CITATION.cff
AUTHORITY_SCOPE.md
COMPUTE_LIMITATIONS.md
DATA_DISCOVERY_REPORT.md
ROADMAP.md
```

The full pre-migration tree is preserved in `provenance/PRE_STEP5_TREE.txt`.

## After

The freeze-stage root now follows the target structure:

```text
README.md
LICENSE
CITATION.cff
CHANGELOG.md
MANIFEST.csv
CHECKSUMS.sha256
canonical/
validation/
implementation/
freeze_release/
audits/
provenance/
docs/
data_requirements/
historical_archive/
tools/
```

# 3. Migration Decisions

| Decision | Result |
|---|---|
| Preserve old mixed repository content. | Moved to `historical_archive/pre_step5_repository/`. |
| Use STEP 1 as active canonical source. | Copied into `canonical/`; deprecated components placed in `historical_archive/`. |
| Use STEP 2 as validation source. | Copied into `validation/`. |
| Use STEP 3 as implementation source. | Copied into `implementation/`. |
| Use STEP 4 as release-prep source. | Copied into `freeze_release/`, `data_requirements/`, and `provenance/`. |
| Preserve external audits. | Copied into `audits/original/` and `audits/extracted/`. |
| Preserve old authority reports. | Moved to `docs/repository_authority/` and `data_requirements/`. |

# 4. Duplicate Detection Results

Duplicate detection used filename repetition and SHA-256 grouping.

Detailed outputs:

- `provenance/STEP5_DUPLICATE_GROUPS.txt`
- `provenance/STEP5_DUPLICATE_FILENAMES.tsv`
- `provenance/STEP5_DUPLICATE_REPORT.md`

Confirmed duplicate classes included:

- duplicated PBH legacy source files;
- duplicated LSC 6.0 simulation outputs;
- duplicated Gallium dataset/summary files;
- duplicated LSC 6.3.0 PDF copies;
- audit originals and extracted text that intentionally preserve the same source content in different forms.

No scientific content was deleted. Redundant active paths were removed from the root by moving the old mixed structures into the historical archive.

# 5. Files Moved

Major moved paths:

| Source | Target |
|---|---|
| `LSC_core/` | `historical_archive/pre_step5_repository/LSC_core/` |
| `framework/` | `historical_archive/pre_step5_repository/framework/` |
| `legacy/` | `historical_archive/pre_step5_repository/legacy/` |
| `archive/` | `historical_archive/pre_step5_repository/archive/` |
| `reports/` | `historical_archive/pre_step5_repository/reports/` |
| old `docs/` | `historical_archive/pre_step5_repository/docs_pre_step5/` |
| `AUTHORITY_SCOPE.md` | `docs/repository_authority/AUTHORITY_SCOPE.md` |
| `COMPUTE_LIMITATIONS.md` | `docs/repository_authority/COMPUTE_LIMITATIONS.md` |
| `ROADMAP.md` | `docs/repository_authority/ROADMAP.md` |
| `DATA_DISCOVERY_REPORT.md` | `data_requirements/DATA_DISCOVERY_REPORT.md` |

# 6. Files Removed or Archived

No files were intentionally deleted.

Archived/preserved:

- old mixed repository tree;
- legacy PBH/curvature material;
- old speculative material;
- old framework code and notebooks;
- historical release packages;
- old generated reports;
- root README pre-STEP5 snapshot.

# 7. Final Folder Roles

| Folder | Role |
|---|---|
| `canonical/` | Active frozen LSC core and freeze-boundary documents. |
| `validation/` | M0-M6 validation infrastructure and risk controls. |
| `implementation/` | Dataset, model, M4, covariance, LOO, transfer, and preregistration templates. |
| `freeze_release/` | Release notes draft, Zenodo draft, freeze checklists, pre-BEST-2 statement. |
| `audits/` | External audits and Codex STEP reports. |
| `provenance/` | Migration plan, duplicate report, manifests, hashes, source inventory. |
| `docs/` | Repository guides and authority documents. |
| `data_requirements/` | Missing-data and access-request documents. |
| `historical_archive/` | Pre-STEP5 repository and deprecated/historical material. |
| `tools/` | Reserved for maintenance scripts. |

# 8. README Summary

`README.md` now states:

- LSC is an unvalidated constrained phenomenological validation framework;
- LSC is not confirmed physics;
- no discovery claim is made;
- no sterile-neutrino exclusion claim is made;
- repository state is frozen before BEST-2-era analysis;
- missing data block full likelihood validation;
- M4 detector/systematics remains a primary competitor;
- negative outcomes are valid outcomes;
- AI model agreement is not scientific evidence.

# 9. Manifest Summary

`MANIFEST.csv` was generated with:

- path;
- file type;
- role;
- canonical status;
- checksum;
- source step;
- notes.

The manifest had 256 lines during verification before this report was added; it is regenerated after report creation.

# 10. Checksum Summary

`CHECKSUMS.sha256` was generated for repository files excluding `.git`. It is regenerated after final report generation.

# 11. Git Status

The working tree contains a large local restructuring with renames and new files. No local commit was created because the instruction allowed commit preparation only with user approval.

Latest observed commits before STEP 5 work:

```text
4e4c492 Migrate LSC data block from legacy mixed root
a095631 Tighten authority boundary wording
e22c7fc Authority purity boundary fix
```

# 12. Publication Status

GitHub publication status: not pushed.

No `git push` was executed.

# 13. Zenodo Status

Zenodo status: not uploaded.

`freeze_release/ZENODO_NEXT_STEP_NOTICE.md` documents that Zenodo archival must be a later immutable snapshot after human review.

# 14. Remaining Human Review Tasks

- Review final claim language.
- Confirm license.
- Confirm authorship and affiliation metadata.
- Review `CITATION.cff`.
- Review `LSC_ZENODO_METADATA_DRAFT.json`.
- Verify `MANIFEST.csv` and `CHECKSUMS.sha256`.
- Review external-source references.
- Decide whether to commit locally.
- Decide whether to push to GitHub.
- Decide whether a later Zenodo archival snapshot is appropriate.

# 15. Final Recommendation

Treat this repository as locally GitHub-freeze-ready after human review. The next step is not theory development. The next step should be a human release gate: review claim language, citation metadata, license, provenance, manifest, and checksums, then decide whether to commit and push.

