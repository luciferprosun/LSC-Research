# LSC 6.3.1 Decision Matrix

| Decision | Answer | Reason | Evidence | Consequence |
|---|---|---|---|---|
| Preserve 6.3.0 unchanged? | YES | Identity and symbolic provenance are recoverable; numerical incompleteness is part of the historical truth. | STEP 01 and STEP 05 | Historical commit, files, version DOI, and limitations remain immutable. |
| Is a new version required for numerical completion? | YES | New values or conventions cannot be authenticated as recovered 6.3.0 without direct evidence. | Frozen parameter adjudication | Any complete executable object receives a distinct successor identity. |
| Use version 6.3.1? | CONDITIONAL | Appropriate for explicit numerical specification and reproducibility with unchanged E1-E12/model class. | Genesis contract | Reserve 6.3.1 for this scope; escalate if physics changes. |
| Use 6.4.0 or 7.0? | CONDITIONAL | Required if equations, physical semantics, or model class change. | Version-bump policy | Rename before freeze and do not present the result as a patch-level successor. |
| Use the same concept DOI lineage for the model successor? | CONDITIONAL | Zenodo versioning links a new record/version while keeping historical versions distinct. | Official Zenodo versioning documentation | Create a new version through the historical record only after release readiness; obtain a new version DOI. |
| Reuse version DOI `10.5281/zenodo.20377427`? | NO | It identifies the immutable historical 6.3.0 record. | Historical identity and DOI policy | The successor must have a new version DOI. |
| Publish a separate Validation Kernel companion? | YES, WHEN READY | Methodology/software is a distinct citable object from the model release. | STEP 01-06 architecture | Separate DOI and explicit bidirectional relation to the model release. |
| Treat historical gallium data as retrospective? | YES | The model and successor decisions are exposed to these data. | Data-exposure audit | Label analyses `RETROSPECTIVE_NON_BLIND`. |
| Call historical gallium tests strict blind? | NO | `MODEL_EXPOSED` is incompatible with strict blindness. | Dataset registry and Step 06 guard | Such language is rejected in code and publication policy. |
| Preserve BEST-2 as prospective? | YES, CONDITIONAL | It remains future blind only if model and prediction are frozen before observed results are accessed. | BEST-2 future contract | No prediction now; future artifact must be hashed and timestamped pre-unblinding. |
| Permit new parameter specification? | YES, IN STEP 07 | A successor must explicitly define what 6.3.0 does not recover. | Genesis contract | Values are labelled `NEW_NUMERICAL_SPECIFICATION_6_3_1`, never recovered 6.3.0. |
| Automatically inherit old values? | NO | Legacy objects are version-conflicted, toy, illustrative, fitted, or post-data. | STEP 01/05 adjudication | Every proposed reuse requires a new decision log and exposure disclosure. |
| Permit numerical validation before the new freeze? | NO | Development choices and evaluation must remain separated. | Genesis and freeze protocol | Prediction, validation, and publication gates remain false. |
| Permit KATRIN/IceCube claims now? | NO | Native releases exist, but LSC-specific mappings are not justified. | STEP 05 mapping assessments | No external veto or likelihood combination. |
| Mark 6.3.1 executable now? | NO | No successor bundle, evaluator, vectors, or release manifest exists. | Executable release requirements | Current maximum readiness is `P1_SPECIFICATION_BOUNDARY_READY`. |

## Version decision

The authorized next design identity is **LSC 6.3.1 Explicit Numerical Specification + Executable Successor**, conditional on preserving E1-E12 and the model class. This is a prospective project identity, not a release declaration. No tag, DOI, numerical bundle, or prediction is created in STEP 06.

## Zenodo recommendation

Recommended strategy: **OPTION C**.

1. When and only when the executable model passes release gates, create the model release as a new Zenodo version linked to the historical lineage. This yields a distinct version record and persistent identifier while preserving prior versions.
2. Publish the LSC Validation Kernel as a separate reproducibility companion with its own DOI and explicit relation to the model release.

Zenodo's official documentation states that a new version is a new record with separate metadata, files, and persistent identifier, linked to prior and future versions: [Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/). It also states that published record files and persistent identifiers are immutable: [About records](https://help.zenodo.org/docs/deposit/about-records/).

No Zenodo deposit, DOI reservation, release, or metadata edit is performed in STEP 06.
