# Optional LSC-Research Repository Structure Proposal

## Scope

This is a proposal only. It does not modify any remote repository and does not apply changes automatically.

## Proposed Release Folder

```text
release/pre_best2_freeze/
  README_FREEZE_ARCHIVE.md
  canonical/
  validation/
  implementation/
  audits/
  provenance/
  metadata/
  release_notes/
  checksums/
```

## Proposed Canonical Folders

```text
docs/canonical/
docs/validation/
docs/implementation/
docs/freeze_boundary/
docs/data_requests/
```

## Proposed Archival Folders

```text
archive/historical/
archive/deprecated/
archive/external_audits/
archive/source_snapshots/
```

## Rules

- Keep canonical LSC separate from MHLM, AOIA, MDLH, and AI-safety material.
- Keep deprecated material visible but inactive.
- Do not overwrite historical files silently.
- Use changelog entries for every post-freeze correction.
- Treat all generated release metadata as draft until human-reviewed.

