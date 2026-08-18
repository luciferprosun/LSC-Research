# Validation reporting policy

Every preregistered test, split and scenario must be reported, including null, adverse, failed and blocked outcomes. Failed folds and unfavorable experiment/isotope transfers may not be hidden.

Reports must distinguish:

- preregistered from exploratory work;
- sensitivity from inference;
- baseline fit from nuisance profiling and frozen LSC evaluation;
- test-level, component-level and model-level falsification;
- historical non-blind splits from future blind predictions;
- raw source statements from deterministic derived fields;
- missing data from zero or null values.

Assumption-based covariance output is labelled `SENSITIVITY_ONLY` and cannot use discovery, exclusion, sigma evidence or decisive preference language. External constraints are reported separately until a quantitative mapping is frozen; likelihoods are never multiplied automatically.

Every result must cite its `ValidationExecutionManifest` hash, dataset hashes, split, baseline versions, covariance and nuisance policy, metric, code commit, environment hash and authorization state. No Step 03 artifact contains an observed or predicted LSC metric.

Step 04 baseline fits and public reproductions are statistical-instrument checks only. Their outcomes cannot change the frozen LSC object, T1-T12 definitions, covariance grid, split registry, or primary endpoint order. PROSPECT control matrices that fail standalone PSD/rank diagnostics must be reported as such and must not be silently repaired or promoted into likelihood input.
