# LSC Archive Structure Plan

Status: Step 3 implementation artifact  
Purpose: local/GitHub/Zenodo freeze package preparation plan only  
Publishing: not performed  

## 1. Local Archive Structure

```text
LSC_FREEZE_PACKAGE/
  README.md
  MANIFEST.csv
  CHECKSUMS.sha256
  canonical/
    LSC_CANONICAL_CORE.md
    LSC_ACTIVE_EQUATION_SET.md
    LSC_FREEZE_BOUNDARY.md
  validation/
    LSC_VALIDATION_PROTOCOL.md
    LSC_M4_DETECTOR_SYSTEMATICS_BASELINE.md
    LSC_COVARIANCE_AND_DATA_POLICY.md
    LSC_EXTERNAL_VETO_CHECKLIST.md
    LSC_PREREGISTRATION_POLICY.md
    LSC_FAILURE_MODES_AND_RISK_MATRIX.md
  implementation/
    LSC_DATA_REQUIREMENT_MATRIX.md
    LSC_M0_M6_SPECIFICATION_TEMPLATES.md
    LSC_M4_IMPLEMENTATION_SCHEMA.md
    LSC_COVARIANCE_PLACEHOLDER_AND_SENSITIVITY_TEMPLATE.md
    LSC_LOO_EXECUTION_PROTOCOL.md
    LSC_CROSS_EXPERIMENT_TRANSFER_PROTOCOL.md
    LSC_EXTERNAL_VETO_DATA_REQUEST_CHECKLIST.md
    LSC_BEST2_PREREGISTRATION_FORM.md
  audits/
    original/
    extracted/
  sources/
    source_inventory.csv
    zenodo_metadata/
  reports/
    PDFs/
  provenance/
    lineage.md
    deprecated_components.md
    source_map.csv
```

## 2. GitHub Release Preparation

Prepare but do not publish:

- freeze tag name proposal;
- release notes;
- changelog;
- checksum manifest;
- source inventory;
- no generated claims beyond frozen documents.

## 3. Zenodo Freeze Package Preparation

Prepare but do not upload:

- archive zip;
- `zenodo.json`;
- DOI relation notes;
- concept DOI continuity statement;
- included files list;
- excluded files list.

## 4. Reproducibility Structure

Required:

- all Markdown source files;
- all generated PDFs;
- source inventory;
- audit inventory;
- checksum manifest;
- scripts used for generation, if any;
- explicit note that placeholders are non-validation-grade.

## 5. Provenance Structure

Must preserve:

- Step 1 canonicalization decisions;
- Step 2 validation rules;
- Step 3 implementation templates;
- original audits;
- extracted audit text;
- Zenodo metadata;
- source repository references.

## 6. Audit Traceability

Every archive must answer:

- what became canonical;
- what became deprecated;
- what validation is required;
- what data are missing;
- what claims are prohibited;
- what negative outcomes mean.

