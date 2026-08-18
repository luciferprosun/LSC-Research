# Cross-validation engine

The engine supports only stable split families frozen in Step 03: leave-one-run-out, leave-one-experiment-out, zone transfer, isotope transfer, and experiment transfer. It does not invent or optimize a split.

Every fold records the split and fold IDs, training indices, hold-out indices, fitted parameters, parameters transferred without refit, nuisance-refit policy, hold-out predictions, and the required `StatisticalExecutionManifest` hash for its fit. Training and hold-out sets must be non-empty and disjoint. A fit callback receives only the training-value vector. It must return exact `fitted_on_indices`; any mismatch raises `DataLeakageError` before scoring. Unregistered split IDs are rejected except for explicitly classified `NON_PHYSICAL_TEST_FIXTURE` IDs.

Baseline parameters and allowed nuisances are fitted inside each training fold only. A frozen LSC parameter is never fitted in either partition. A fold cannot be omitted because its result is unfavorable, and all fold-level outputs must be reported.

Historical BEST, GALLEX/GNO, and SAGE splits remain `NON_BLIND_HISTORICAL`; cross-validation mechanics do not relabel exposed data as a clean blind hold-out.
