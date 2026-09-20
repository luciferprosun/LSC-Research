# Baseline implementations

## Implemented models

| Registry identity | Implementation | Fit policy | Current status |
|---|---|---|---|
| M0 / M_NULL | Published conventional expectation | no fit | executable |
| M1 / M_CONSTANT_DEFICIT | One shared normalization times conventional expectation | normalization only | executable |
| M2 / M_CROSS_SECTION_VARIANT | Explicit registered cross-section expectation, optionally with declared source normalization | no post-result model selection | executable per registered model |
| M3 / M_STERILE_3P1 | Standard `1 - sin²(2θee) sin²(1.267 Δm² L/E)` | `sin²(2θee)`, `Δm²` within explicit bounds | executable only with explicit L/E inputs |
| M4 / M_EXPERIMENT_NORMALIZATION | One normalization per declared experiment | experiment normalizations | executable |
| M4 / M_DETECTOR_SYSTEMATIC | Explicit detector-response multiplier | declared response/nuisance only | executable |
| M4 / M_HIERARCHICAL_EXPERIMENT | No canonical hierarchy/prior recovered | none authorized | `SPECIFICATION_INCOMPLETE` |
| M5 / M6 | Frozen LSC trace/full models | forbidden | blocked before dispatch |

The cross-section registry has no default or “correct” model. Results must be emitted for every preregistered alternative. The experiment-normalization model reports its larger parameter count and is not compared to simpler models by raw chi-square alone.

M3 never receives an inferred baseline or energy. Per-observation L/E or a source-approved geometry-averaged representation is mandatory. Missing geometry produces `BaselineSpecificationIncomplete`. M3 contains no LSC parameter.

The hierarchical submodel remains incomplete because Step 03 did not freeze a population distribution, hyperprior, or estimator. Step 04 intentionally does not invent one.

## Optimization record

Fits use SciPy L-BFGS-B with explicit initial values, bounds, tolerance, convergence state, evaluation count, final parameters, final statistic, and optimizer message. The implementation is deterministic and uses no random seed. Any later stochastic method must freeze and report its seed.

`BaselineExecutionEngine` is the public execution boundary. Every call returns a prediction, a `BaselineResult`, and a checksum-bound `StatisticalExecutionManifest` containing dataset hash, model/version, fitted parameters, nuisance policy, covariance scenario, split, metric, optimizer, code commit, source-tree hash, environment hash, classification, timestamp, and `LSC_used=false`. Lower-level model functions are numerical primitives used by this boundary and analytical unit tests.
