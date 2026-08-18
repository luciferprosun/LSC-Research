# Validation Unlock Matrix

## Decision summary

The complete frozen numerical bundle is a universal prerequisite for T1-T11. Recovering it would permit only the test-specific scope shown below; it would not automatically supply collaboration covariance, external mappings, M3 geometry, or directional inputs.

| Test | Current status | Minimum blocker set | Optional improvements | Executable immediately if bundle recovered? | Collaboration covariance required? | Sensitivity-only without it? |
|---|---|---|---|---|---|---|
| T1 | PARTIAL | bundle; BEST transfer input map | exact joint likelihood | YES, diagnostic only | YES for inferential PASS | YES |
| T2 | PARTIAL | bundle; reverse-mapping identifiability; BEST covariance | exact joint likelihood | NO | YES | Only after identifiability |
| T3 | PARTIAL | bundle; frozen cross-experiment mapping; dataset contracts | joint cross-experiment covariance | NO unless mapping is inside recovered bundle | YES for inference | YES after mapping |
| T4 | PARTIAL | bundle; frozen reverse cross-experiment mapping | joint covariance | NO unless mapping is inside recovered bundle | YES for inference | YES after mapping |
| T5 | SENSITIVITY_ONLY | bundle; frozen isotope/energy map | authoritative cross-isotope nuclear covariance | NO unless energy map is inside recovered bundle | YES for inference | YES |
| T6 | PARTIAL | bundle; run prediction map | full run covariance/likelihood | YES, diagnostic folds only | YES for inferential aggregate | YES |
| T7 | PARTIAL | bundle; experiment prediction mapping | authoritative cross-experiment covariance | YES only if mapping is bundle-complete | YES for inference | YES |
| T8 | SENSITIVITY_ONLY | bundle; cross-section registry | joint nuclear covariance | YES | Needed to leave sensitivity scope | YES by definition |
| T9 | SENSITIVITY_ONLY | bundle; frozen nuisance applicability map | collaboration covariance | YES | Needed to leave sensitivity scope | YES by definition |
| T10 | PARTIAL | bundle; production M3 geometry; explicit external mapping where veto used | exact geometry and native external likelihood mappings | NO | Dataset-native covariance required | Only restricted gallium comparison after geometry |
| T11 | PARTIAL | bundle; executable held-out prediction map | full dataset-native covariance | YES, first controlled sensitivity execution | YES for confirmatory PASS | YES |
| T12 | BLOCKED | bundle; active tensor; precise timing; surveyed orientation; Earth-fixed geometry; frames; units; frozen statistic | event-resolved likelihood and power study | NO | Directional likelihood/covariance required | NO; remains blocked |

## Minimum validation unlock set

**MINIMUM_VALIDATION_UNLOCK_SET**

This set permits the first controlled preregistered scalar numerical execution, expected to be a T11 diagnostic/sensitivity run under the already frozen policy:

1. A complete authentic frozen bundle with parameter ordering.
2. Target-dataset exposure classification retained; a non-clean historical test is never relabelled blind.
3. Authentic units, frames, tensor semantics, and all E1-E12 numerical inputs required by that scalar path.
4. Exact evaluator initialization and dataset-to-observable mapping.
5. Hash-verified provenance admission with no post-data substitution.
6. A separate human-approved STEP 06 certification and execution decision.

This minimum does not authorize an inferential PASS. Without authenticated collaboration covariance, the result remains SENSITIVITY_ONLY.

Current state: **INCOMPLETE**, blocked by BLK-P0-FROZEN-BUNDLE.

## Full validation unlock set

**FULL_VALIDATION_UNLOCK_SET**

For the frozen primary sequence T11, T7, T3, T1, T10:

1. Complete MINIMUM_VALIDATION_UNLOCK_SET.
2. Authenticated collaboration covariance/likelihood for every reached dataset and split.
3. Authoritative shared nuclear and cross-experiment uncertainty treatment.
4. Production M3 geometry for T10.
5. Explicit LSC-to-external mappings for every external veto actually invoked.
6. Every test-specific input and the unchanged multiple-testing order.

Current state: **INCOMPLETE**.

T12 remains a separate directional-component validation. It is not silently added to scalar validation prerequisites, but no directional claim is allowed while it is blocked.
