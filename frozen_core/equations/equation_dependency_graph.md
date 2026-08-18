# E1-E12 Dependency Graph

This is a source-bounded DAG. Equation numbers do not imply a sequential chain.

Topological order: `E1 -> E4 -> E6 -> E9 -> E11 -> E3 -> E2 -> E5 -> E8 -> E7 -> E10 -> E12`

| From | To | Status | Rationale |
|---|---|---|---|
| `E1` | `E6` | `SOURCE_DERIVED_DEPENDENCY` | E6 consumes N0_a from E1. |
| `E1` | `E8` | `SOURCE_DERIVED_DEPENDENCY` | E8 requires the same flux, cross-section, geometry, and exposure weighting used in E1. |
| `E2` | `E5` | `SOURCE_DERIVED_DEPENDENCY` | E5 consumes epsilon_LSC,a from E2. |
| `E3` | `E2` | `SOURCE_DERIVED_DEPENDENCY` | E2 consumes q_a from E3. |
| `E3` | `E8` | `SOURCE_DERIVED_DEPENDENCY` | E8 consumes q_a from E3. |
| `E4` | `E3` | `SOURCE_DERIVED_DEPENDENCY` | E4 constrains the tensor used by E3. |
| `E4` | `E12` | `SOURCE_DERIVED_DEPENDENCY` | E4 constrains the tensor used by E12. |
| `E6` | `E9` | `SOURCE_DERIVED_DEPENDENCY` | E9 is assembled from inner and outer ratios. |
| `E6` | `E10` | `SOURCE_DERIVED_DEPENDENCY` | E10 consumes observed ratios. |
| `E7` | `E10` | `UNVERIFIED_DEPENDENCY` | E7 may provide R_pred residuals, but the source does not freeze this binding. |
| `E8` | `E7` | `SOURCE_DERIVED_DEPENDENCY` | E7 consumes F0_a and FA_a from E8. |
| `E5` | `E10` | `UNVERIFIED_DEPENDENCY` | E5 may provide predictions for E10, but the exact ratio binding is not frozen. |
| `E11` | `E3` | `SOURCE_DERIVED_DEPENDENCY` | E11 produces n_lab used by E3. |
| `E11` | `E12` | `SOURCE_DERIVED_DEPENDENCY` | E11 produces n_lab used by E12. |
