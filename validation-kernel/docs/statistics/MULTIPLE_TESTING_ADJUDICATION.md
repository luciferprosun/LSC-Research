# Multiple-testing adjudication

## Verdict

`MULTIPLE_TESTING_POLICY_FROZEN`

This decision was made in Step 04 before any numerical LSC prediction, fit, validation statistic, or hold-out result was available. No LSC result information was used.

## Dependency map

T1-T12 are not twelve independent endpoints. BEST is reused by T1, T2, T3, T4, T6, T7, T8, T9, T10, and T11; the legacy gallium experiments are reused across transfer, cross-section, systematics, sterile, and null comparisons. T12 lacks the data needed even to characterize its dependence. The full machine-readable map is `preregistration/multiple_testing_dependency_map.json`.

## Selected strategy

Primary family ID: `LSC_PRIMARY_FIXED_SEQUENCE_V1`

Fixed order:

1. T11, simpler null/baseline comparison;
2. T7, leave-one-experiment-out generalization;
3. T3, BEST-to-GALLEX transfer;
4. T1, BEST inner-to-outer zone transfer;
5. T10, sterile 3+1 comparison.

The family-wise alpha is 0.05. Each endpoint is tested at 0.05 in this fixed order. Confirmatory testing stops at the first non-rejection, unavailable prerequisite, blocker, or invalid endpoint. Every later output is descriptive and cannot reopen the gate. Fixed-sequence gatekeeping controls family-wise type-I error without assuming independence, provided each reached endpoint has a valid preregistered test calibration.

T2, T4, and T6 are secondary descriptive diagnostics. T5, T8, and T9 are sensitivity-only. T12 remains blocked. BEST-2 remains outside T1-T12 and `FUTURE_ONLY`.

## Alternatives considered

- Holm family-wise control is valid under arbitrary dependence when all primary p-values are simultaneously valid, but it does not encode the scientific prerequisite order.
- Benjamini-Hochberg controls false discovery rate under an appropriate dependence contract, but is weaker than the family-wise protection chosen for a confirmatory claim.
- One prespecified primary endpoint with descriptive secondaries would be valid, but would discard several already-required ordered generalization gates.

No strategy may be changed after LSC outcomes. The frozen policy does not itself authorize a global claim: the numerical bundle and every reached primary prerequisite must first be valid.
