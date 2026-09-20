# E1-E12 Equation Execution Map

Source identity: `canonical-equations`, SHA-256 `af801a3f45171f6cc87f526fcfe30b8d87ca445ab304cd614569358aa1f94981`.

The exact symbolic strings and metadata are in `frozen_core/equations/equations.json`.

| ID | Output | Dependencies | Readiness | Implementation scope | Principal blocker |
|---|---|---|---|---|---|
| E1 | `N0_a` | none | `BLOCKED_MISSING_NUMERICAL_CONTRACT` | descriptor only | integration/default/input contract |
| E2 | `epsilon_LSC,a` | E3 | `BLOCKED_MISSING_PARAMETER` | descriptor only | `lambda0`, `lambdaA`, `f0_a`, `fA_a` |
| E3 | `q_a` | E4, E11 | `BLOCKED_MISSING_ORIENTATION` | descriptor only | active tensor, orientation, frame |
| E4 | tensor constraint result | none | `NUMERIC_READY` | non-predictive structural check | none for structure check |
| E5 | `N_LSC,a(theta)` | E2 | `BLOCKED_MISSING_PARAMETER` | descriptor only | `theta`, configuration, integration defaults |
| E6 | `R_a` | E1 | `NUMERIC_READY` | non-LSC arithmetic transform | explicit compatible inputs required |
| E7 | `Delta R_a^LSC` | E8 | `BLOCKED_MISSING_PARAMETER` | descriptor only | amplitudes and exact response functions |
| E8 | `F0_a`, `FA_a` | E1, E3 | `BLOCKED_MISSING_FUNCTION` | descriptor only | response functions and weighting definition |
| E9 | `R_BEST` | E6 | `NUMERIC_READY` | non-LSC tuple transform | explicit ratios required |
| E10 | `chi2` | E5, E6, E7 | `BLOCKED_MISSING_COVARIANCE` | descriptor only | covariance, vector, penalty contract |
| E11 | `n_lab` | none | `BLOCKED_MISSING_FRAME` | descriptor only | timing, coordinates, orientation, transform |
| E12 | `S_a(t)` | E4, E11 | `BLOCKED_MISSING_ORIENTATION` | descriptor only | timing, geometry, tensor, orientation, frames |

## Dependency policy

The dependency graph is a DAG, not the invented sequential chain E1 then E2 through E12. Numbering records the canonical equation labels, not execution order.

Two edges remain explicitly uncertain:

- E5 to E10: E5 may provide a prediction consumed by E10, but the exact ratio binding is not frozen;
- E7 to E10: E7 may provide a residual prediction consumed by E10, but the source does not freeze this binding.

They are emitted as `UNVERIFIED_DEPENDENCY` and drawn as dashed edges in Graphviz. No code resolves them by guess.

Generated representations:

- `frozen_core/equations/equation_dependency_graph.json`
- `frozen_core/equations/equation_dependency_graph.md`
- `frozen_core/equations/equation_dependency_graph.dot`

## Meaning of numerical readiness

`NUMERIC_READY` on E4, E6, or E9 means only that the local algebraic operation is source-defined and testable with explicit input. It does not mean that an LSC prediction is available. Full prediction authorization is a separate evaluator gate and is currently false.
