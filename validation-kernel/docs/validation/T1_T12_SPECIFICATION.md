# T1-T12 specification

## Canonical mapping

The numbering below is source-derived from `LSC_6_3_0_VALIDATION/18_VALIDATION_READY/FROZEN_PREDICTION_PROTOCOL.md`. The separate 13-row readiness matrix is not treated as another numbering scheme; BEST-2 is a future contract outside T1-T12.

| ID | Canonical test | Primary readiness | Principal blockers |
|---|---|---|---|
| T1 | BEST inner to outer zone transfer | `PARTIAL` | frozen numerical bundle, joint covariance |
| T2 | BEST outer to inner zone transfer | `PARTIAL` | reverse identifiability, bundle, covariance |
| T3 | BEST to GALLEX/SAGE transfer | `PARTIAL` | cross-experiment mapping, bundle, covariance |
| T4 | GALLEX/SAGE to BEST transfer | `PARTIAL` | cross-experiment mapping, bundle, covariance |
| T5 | 51Cr to 37Ar transfer | `SENSITIVITY_ONLY` | energy mapping, shared isotope covariance |
| T6 | leave one run out | `PARTIAL` | bundle, run covariance |
| T7 | leave one experiment out | `PARTIAL` | bundle, cross-experiment covariance |
| T8 | cross-section sensitivity | `SENSITIVITY_ONLY` | bundle, cross-isotope covariance |
| T9 | systematic/covariance sensitivity | `SENSITIVITY_ONLY` | bundle, collaboration covariance |
| T10 | sterile 3+1 versus LSC | `PARTIAL` | bundle, geometry integration, external mappings |
| T11 | null/baselines versus LSC | `PARTIAL` | bundle, full covariance |
| T12 | directional/sidereal | `BLOCKED` | timing, orientation, geometry, tensor, frames, units |

The complete machine definition in `preregistration/tests.json` freezes scientific question, hypothesis, datasets, calibration/hold-out subsets, target, observable, metrics, baselines, nuisance handling, covariance requirement, cross-section handling, timing, geometry, orientation, blockers, test-level outcome rule and reporting requirements.

## Test-level outcomes

For inferentially valid tests, a test-level PASS requires frozen LSC to improve preregistered held-out prediction over every declared equally or less complex baseline after the declared complexity treatment. Equal or better performance by a simpler baseline is a test/component failure. These are predictive-comparison rules, not discovery thresholds. Global confirmation remains prohibited while multiple-testing policy is unresolved.

T8 and T9 never produce inferential PASS/FAIL under assumption-based covariance. They report stability or reversal as `SENSITIVITY_ONLY`. All folds, failed transfers, null outcomes and blockers must be retained.

## T12 hard block

T12 has state `BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT`. It requires precise event/sub-run timing, surveyed detector/source orientation, sufficient Earth-fixed geometry, a complete authentic active tensor, reference-frame transforms and required units. Exposure midpoint is explicitly rejected as an event-time substitute. Even if metadata later become complete, the historical statistic and power/PASS rule must be frozen before execution.
