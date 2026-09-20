# Model-comparison policy

Model comparison is allowed only when dataset, split, covariance, and likelihood-normalization contracts are comparable.

The engine implements raw delta chi-square, likelihood-ratio statistic, AIC, BIC, held-out predictive log-likelihood, and cross-validation score interfaces. Interpretation is restricted as follows:

- delta chi-square is not converted to a confidence level without a valid coverage construction;
- likelihood-ratio interpretation requires nesting/regularity or an explicit calibrated null distribution;
- AIC and BIC require comparable normalized likelihoods and a justified effective parameter count;
- predictive log-likelihood requires the held-out likelihood normalization;
- raw chi-square does not compensate for added experiment-specific parameters;
- assumption-based covariance comparisons remain `SENSITIVITY_ONLY`;
- no comparison result automatically authorizes discovery, exclusion, or global confirmation.

Baseline fits and nuisance profiles may not cause any change to the frozen LSC object, T1-T12 definitions, covariance scan, split registry, or primary endpoint order. Results that contradict an expectation are retained under the reporting and falsification policies.
