# Zenodo Unification Plan For LSC

Date: 2026-05-05

## Decision

Use the LSC concept DOI as the single project-level publication identity:

```text
https://doi.org/10.5281/zenodo.19780615
```

This concept DOI already links:

- LSC 6.0: `10.5281/zenodo.19780616`
- LSC 6.2.0: `10.5281/zenodo.19878587`

The LSC v1.2.0 computational release:

```text
10.5281/zenodo.19843361
```

has a different concept DOI and cannot be physically merged into the existing LSC concept DOI after publication. It should be treated as a supplementary computational/reproducibility record and linked from the main LSC record.

## Why It Looks Like Two Projects

The confusion comes from two separate mechanisms:

1. LSC 6.0 and LSC 6.2.0 are true Zenodo versions under one concept DOI.
2. LSC v1.2.0 was published as its own record with its own concept DOI.

The correct public interpretation:

```text
LSC 6.0 -> LSC 6.2.0 is the main theory line.
LSC v1.2.0 is a supplementary computational extension.
```

## Metadata-Only Update Strategy

If we must avoid any new version DOI, edit only metadata on the current latest LSC record:

```text
Record: https://zenodo.org/records/19878587
Version DOI: 10.5281/zenodo.19878587
Concept DOI: 10.5281/zenodo.19780615
```

Recommended metadata edits:

- description: add LSC 6.3.0 continuation note and BEST-2 validation framing;
- version: keep `6.2.0-preprint` or use a metadata note such as `6.2.0-preprint; 6.3.0 continuation metadata note`;
- related identifiers: add GitHub link to the LSC 6.3.0 update file;
- related identifiers: keep `19843361` as `isSupplementedBy`;
- notes: state that LSC 6.3.0 is a metadata-linked continuation, not a file replacement.

This preserves the existing version DOI.

## New-Version Strategy

If we need to upload a new PDF/ZIP package, use Zenodo's "New version" on record `19878587`.

Expected result:

- a new version DOI will be created;
- the project-level concept DOI remains `10.5281/zenodo.19780615`;
- the public project is still one LSC publication line.

This is the cleaner archival method if files change.

## Recommended Public Wording

```text
LSC is now cited as one evolving Zenodo project under concept DOI 10.5281/zenodo.19780615. LSC 6.2.0 is the latest published version record, while the LSC 6.3.0 continuation is a GitHub-linked theory and validation update. The earlier LSC Framework v1.2.0 record is retained as a supplementary computational release, not as a separate primary theory line.
```

## Published Result

LSC 6.3.0 was published as a new Zenodo version under the same LSC concept DOI:

```text
Record: https://zenodo.org/records/20037838
Version DOI: https://doi.org/10.5281/zenodo.20037838
Concept DOI: https://doi.org/10.5281/zenodo.19780615
```
