# LSC Equation Integrity Review

Status: final re-audit and Zenodo update preparation  
Scope: active equation set in `canonical/LSC_ACTIVE_EQUATION_SET.md`

## Active Equation Boundary

The active equation set is restricted to the frozen STEP 1 classification. No new equation is added in this review.

Active canonical equations remain:

| ID | Equation object | Status |
|---|---|---|
| E1 | Baseline event expectation | canonical |
| E2 | LSC detector-efficiency response | canonical with functional-form freeze required |
| E3 | Anisotropic projection | canonical with identifiability caveat |
| E4 | Tensor symmetry and tracelessness | canonical |
| E5 | LSC event expectation | canonical |
| E6 | Observed ratio | canonical |

## Tensor Drift Review

No new tensor structures are introduced in active documents. Existing tensor language remains limited to detector-response phenomenology and is constrained by:

- symmetric traceless requirement;
- identifiability caveat;
- orientation/timestamp metadata requirement;
- M4 detector/systematics competition;
- external veto checks.

## Hidden Drift Review

The active folders reviewed were:

- `canonical/`
- `validation/`
- `implementation/`
- `freeze_release/`

No LSC 6.4 material or new active equations were identified in active folders.

## Historical Equation Handling

PBH-heavy, curvature-heavy, and old speculative equations remain in `historical_archive/` as historical material only. They are not active freeze-stage equations.

## Review Conclusion

Equation integrity is preserved for local Zenodo preparation. Publication must still state that functional forms, covariance, and metadata requirements block full likelihood validation.

