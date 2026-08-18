# LSC 6.3.1 Genesis Contract

## Definition

> LSC 6.3.1 is a reproducibility and executable-specification successor to LSC 6.3.0. It may preserve the symbolic E1-E12 framework where explicitly unchanged, but every numerical parameter, unit, frame, tensor component, initialization rule, and executable convention must be explicitly versioned and provenance-labelled. It must not be presented as a recovered numerical copy of LSC 6.3.0 unless direct evidence establishes identity.

STEP 06 authorizes this contract, not the creation of numerical values. STEP 07 may define an explicit successor under these rules.

## Version identity

`6.3.1` is the approved successor candidate only when:

- E1-E12 remain symbolically and physically unchanged;
- the model class and observable semantics remain unchanged;
- work is limited to explicit numerical specification, executable formalization, provenance, methodology, and reproducibility;
- all new content is labelled as new successor content.

If STEP 07 changes an equation, physical interpretation, tensor semantics, observable mapping, or model class, the release must be renamed before freeze:

- `6.4.0` for a compatible but scientifically substantive model extension;
- `7.0` for an incompatible model-class or conceptual change.

## Exactly one classification per element

Every file, equation descriptor, parameter, convention, transformation, and algorithm entering the successor must have exactly one class:

| Class | Meaning | Executable admission |
|---|---|---|
| `UNCHANGED_FROM_6_3_0_AUTHENTIC` | Directly recovered, hash-bound historical content used without semantic change. | Allowed with exact source identity. |
| `FORMALIZED_FROM_6_3_0` | Historical symbolic content encoded formally without changing meaning. | Allowed with source-to-code mapping and equivalence tests. |
| `NEW_NUMERICAL_SPECIFICATION_6_3_1` | Newly declared value, ordering, unit, frame, tensor component, bound, default, or numerical convention. | Allowed only as 6.3.1 content with a complete decision log. |
| `NEW_METHOD_6_3_1` | New evaluator, schema, provenance, validation, or release infrastructure. | Allowed when it does not silently change model physics. |
| `HISTORICAL_REFERENCE_ONLY` | Legacy or contextual material retained but inactive. | Never active by inheritance. |
| `UNRESOLVED` | Meaning, value, source, or role remains undecided. | Prohibited from an executable release. |

## No silent inheritance

No numerical value from 4.x, 5.5, 6.0, 6.2, 6.2.1, toy tables, illustrative examples, or historical fits becomes active merely because it exists. To enter 6.3.1 it must be newly and explicitly selected, versioned, justified, exposure-labelled, and classified. It then remains new 6.3.1 content, not recovered 6.3.0 content.

## Parameter decision log

Every numerical parameter requires all of:

- parameter ID and canonical name;
- value and uncertainty;
- units, dimensions, frame, and ordering;
- origin and exact source;
- reason for selection;
- introduced version;
- data-exposure status;
- inherited/newly specified/fit-derived flags;
- training data when fit-derived;
- frozen status and content classification;
- source and artifact SHA-256.

Missing metadata makes the parameter `UNRESOLVED`. No default may fill the gap.

## Data-exposure consequence

BEST, GALLEX/GNO, SAGE 51Cr, and SAGE 37Ar were available before this successor specification. They are therefore `MODEL_EXPOSED`, `NON_BLIND_HISTORICAL`, and usable only under `RETROSPECTIVE_NON_BLIND` reporting for 6.3.1 if the new numerical decisions were made with knowledge of them.

Permitted historical-data roles are model development, compatibility assessment, retrospective benchmark, parameter illustration, and baseline comparison. Strict blind confirmation is prohibited.

## Two validation tracks

### Track A - retrospective

- label: `RETROSPECTIVE_NON_BLIND`;
- scope: historical BEST, GALLEX/GNO, SAGE, and other previously exposed datasets;
- all fits, parameter choices, and exposure must be disclosed;
- results may assess compatibility or benchmark predictive structure but may not be presented as blind confirmation.

### Track B - prospective

- label: `PROSPECTIVE_BLIND`;
- scope: genuinely future outcomes not accessed before model and prediction freeze;
- requires complete model, method, data-input, and prediction artifacts to be hash-frozen and timestamped before unblinding;
- BEST-2 remains `FUTURE_BLIND` and has no prediction value in STEP 06.

## Hard development sequence

1. Specification.
2. Parameter determination.
3. Freeze.
4. Retrospective evaluation.
5. Prospective prediction.
6. Future unblinding.

Steps 2 and 5 may not be merged. A value selected using historical observations cannot later be described as a pre-data prediction for those observations.

## Freeze protocol for the successor

Before any prospective prediction:

1. finalize equations and version classification;
2. finalize the complete parameter bundle;
3. finalize evaluator, input schema, transformations, and numerical tolerances;
4. generate experiment-independent golden reference vectors;
5. hash all model, environment, schema, and test artifacts;
6. commit the complete object;
7. create a release manifest and timestamp;
8. create a release tag only after all gates pass;
9. prohibit parameter or semantic changes after freeze;
10. generate a separately hashed prediction artifact only afterward.

STEP 06 does not execute this protocol and creates no release tag.

## BEST-2 prospective protocol

A future `PROSPECTIVE_BLIND_PREDICTION` requires:

- final authoritative as-built geometry and source insertion coordinates;
- final isotope, branching, source assay, and covariance;
- actual exposure/extraction/counting design;
- a completely frozen successor model and prediction function;
- a frozen data, cross-section, covariance, nuisance, and reporting policy;
- proof that observed BEST-2 results were not accessed;
- a hashed, timestamped prediction artifact created before unblinding.

Until every condition holds, BEST-2 remains `FUTURE_ONLY`, `FUTURE_BLIND`, and `prediction_authorized=false`.

## Scientific interpretation boundary

The successor may establish reproducibility of its own explicitly versioned object. It cannot retroactively establish numerical reproducibility or independent validation of historical 6.3.0. Claims about physical performance require separately authorized evaluation after freeze.
