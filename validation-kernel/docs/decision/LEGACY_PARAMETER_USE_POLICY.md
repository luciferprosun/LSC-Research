# Legacy Parameter Use Policy

## Rule

Legacy numerical values are preserved as evidence, not inherited as active parameters. No value from an earlier LSC epoch may enter 6.3.1 without an explicit new-version decision, source, reason, exposure disclosure, and content classification.

## Epoch policy

| Source epoch | Historical reference | Exploratory initialization | Active 6.3.1 use | Required classification |
|---|---|---|---|---|
| 4.x deprecated PBH-era configuration | Allowed with deprecation label. | Conditional, isolated, and never reported as a prediction. | Not by inheritance. A deliberate new selection requires full review and may trigger a larger version bump if semantics differ. | `HISTORICAL_REFERENCE_ONLY` or, after a new justified decision, `NEW_NUMERICAL_SPECIFICATION_6_3_1` |
| 5.5 tensor `D` and optimized alpha | Allowed with post-data and version labels. | Conditional software exploration only; never an active frozen fixture. | Cannot be mapped automatically to active `A_a^{ij}`. A new tensor choice is 6.3.1 content and requires complete frame/orientation semantics. | `HISTORICAL_REFERENCE_ONLY`; automatic mapping remains prohibited |
| 6.0 toy amplification/scenarios | Allowed as toy history. | Allowed only in explicitly non-physical or exploratory work outside release artifacts. | Not admissible as an active release value without a new scientific decision. | `HISTORICAL_REFERENCE_ONLY` or new specification after adjudication |
| 6.2 illustrative `delta` | Allowed with the source's illustrative label. | Conditional for non-reportable exploration. | Never promoted as measured, fitted, or frozen. | `HISTORICAL_REFERENCE_ONLY` |
| 6.2.1 five-anchor coefficients | Allowed with fit provenance and adverse leave-one-out results. | Conditional development seed with full training-data disclosure. | May not become a clean predictor for its fit datasets; cannot be called 6.3.0. | `HISTORICAL_REFERENCE_ONLY` or `NEW_NUMERICAL_SPECIFICATION_6_3_1` with `fit_derived=true` |
| Toy `c0=0.808281`, `c1=0.012500` | Allowed as a preserved post-data fitted toy table. | Conditional non-physical/software exploration only. | No automatic `c0/c1 -> lambda0/lambdaA` mapping; prohibited as frozen 6.3.0. | `HISTORICAL_REFERENCE_ONLY` |

## Admission requirements for any legacy-derived successor decision

If STEP 07 deliberately selects or transforms a legacy value, the record must state:

1. exact source path, commit/version, and SHA-256;
2. original symbol, units, frame, semantics, and exposure status;
3. transformation equation, if any;
4. reason for reintroduction;
5. datasets known and datasets used for fitting;
6. new 6.3.1 parameter ID and content class;
7. uncertainty and domain;
8. whether the decision changes E1-E12 or the model class;
9. retrospective-only consequence for exposed data;
10. tests demonstrating that no historical label is silently inherited.

Failure of any item leaves the candidate `UNRESOLVED` and inactive.

## Explicitly prohibited mappings

- toy `c0/c1` to historical frozen `lambda0/lambdaA`;
- LSC 5.5 `D` to historical active 6.3.0 `A_a^{ij}`;
- 6.2/6.2.1 coefficients plus 6.3 equations as a purported recovered bundle;
- exposure midpoint to event timestamp for T12;
- average path length to exact volume-integrated sterile prediction;
- marginal uncertainty to a fabricated collaboration covariance.

The historical quarantine remains active. This policy does not change any quarantined object's provenance class.
