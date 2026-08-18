# LSC 6.3.0 frozen validation preregistration master

## Status and scope

This is a methodology freeze, not a registration of numerical LSC results. It defines the decisions that can be defined from authentic archive evidence while keeping numerical LSC prediction and validation unauthorized.

## Questions and tests

T1-T12 are bound to `tests.json`. The source-derived mapping is described in `docs/validation/T1_T12_SPECIFICATION.md`. T1-T11 cover zone, experiment, isotope, run/experiment hold-out, cross-section/systematic sensitivity, sterile comparison and null comparison. T12 is hard blocked.

## Data, transformations and exclusions

`validation_datasets.json` is the sole machine-readable dataset registry. `datasets.json` binds to it by SHA-256. Each dataset contract fixes source identity/hash, allowed rows, exclusions, deterministic transformations, units, missing values, derived fields, uncertainty/covariance, timing, geometry and provenance. Raw sources are immutable. BEST's 1070/1069 discrepancy is preserved. SAGE controls are not primary rows. Isotopes remain separate.

## Splits and blindness

`splits.json` freezes stable-ID split membership before outcomes. Historical data are `MODEL_EXPOSED` and `NON_BLIND_HISTORICAL`, not clean hold-outs. BEST-2 remains `FUTURE_BLIND`, has zero observations and is outside T1-T12.

## Models and no-refit rule

`baseline_models.json` preserves M0-M6 and stable aliases. Baselines may be fitted only on declared calibration data. `no_refit_policy.json` forbids every fit/refit/optimization/calibration of M5/M6/frozen LSC. Nuisance profiling cannot alter a frozen LSC field.

## Statistics

`metric_registry.json` defines prerequisites and limits for chi-square, delta chi-square, likelihood ratio, predictive log-likelihood, residuals, AIC, BIC, cross-validation, predictive calibration and posterior predictive checks. No Wilks, Gaussian or Bayesian interpretation is assumed without its prerequisites.

## Nuisance and covariance

`nuisance_registry.json` fixes nuisance categories and correlation scopes. `covariance_scenarios.json` freezes four assumption-based sensitivity scenarios and an unavailable authentic collaboration scenario. Assumption-based output is never significance.

## Cross-section treatment

`gallium_cross_section_models.json` contains every archived alternative. No model is default/correct. The complete registered set is reported; alternatives are not selected after outcomes and incompatible Krofcheck/Frekers inputs are not combined.

## External constraints

`external_constraints.json` requires explicit quantitative mapping into KATRIN/IceCube parameter spaces. Both mappings currently fail with `EXTERNAL_VETO_BLOCKED_MAPPING_MISSING`. No likelihood multiplication is automatic.

## Multiple testing

Step 04 adjudicated `multiple_testing_policy.json` before any numerical LSC evaluation. Status is `MULTIPLE_TESTING_POLICY_FROZEN`. The primary family uses fixed-sequence hierarchical gatekeeping (`T11 -> T7 -> T3 -> T1 -> T10`) at family-wise alpha 0.05, stopping at the first non-rejection, blocker, invalid endpoint, or missing prerequisite. T2/T4/T6 are secondary descriptive tests; T5/T8/T9 remain sensitivity-only; T12 remains blocked. Holm family-wise control, false-discovery-rate control, and a single-primary strategy were documented as valid alternatives but were not selected. No global confirmation claim is authorized while the numerical LSC bundle or a required primary gate remains blocked.

## Stopping rules

Stop before numerical execution if the authentic frozen bundle, dataset hash, contract, required covariance, mapping or authorization is absent. Stop a run on schema/hash mismatch. Do not retry with altered splits, metrics, nuisance treatment or covariance. Report the first blocker. T12 and BEST-2 have their additional hard gates.

## Falsification and negative results

`falsification_rules.json` defines test-, component- and model-level rules. All negative, null, adverse and blocked outcomes are retained. A simpler equally predictive baseline removes the claimed LSC predictive advantage. No single failure escalates globally without a predeclared rule.

## Authorization boundary

The dry-run harness may load and hash contracts, select stable splits, resolve baseline/covariance definitions and emit a deterministic execution manifest. It sets `prediction_authorized=false` and `numerical_validation_authorized=false`; it cannot emit an LSC prediction or scientific result.
