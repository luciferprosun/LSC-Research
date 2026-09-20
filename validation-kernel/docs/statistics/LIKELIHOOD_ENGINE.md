# Likelihood engine

## Scope

The Step 04 likelihood layer validates the statistical instrument independently of LSC. It accepts observations, predictions, uncertainties or an explicit covariance matrix, an optional mask, and a declared fitted-parameter count. It returns raw and profiled statistics separately, together with observation count, fitted-parameter count, degrees of freedom when justified, convergence, assumptions, covariance diagnostics, nuisance values, and warnings.

Implemented primitives are:

- diagonal Gaussian chi-square;
- full-covariance Gaussian chi-square;
- Gaussian pull terms;
- profiled nuisance chi-square through the nuisance engine;
- release-native grid lookup for KATRIN-like absolute chi-square surfaces.

Input vectors must be finite, one-dimensional, and dimensionally consistent. A mask must select at least one record. Uncertainties must be positive. Full covariance evaluation delegates all matrix policy to `CovarianceMatrix`; it cannot silently invert or repair an invalid matrix.

## Likelihood interpretation

The engine does not infer a normalized log-likelihood from chi-square alone. Predictive log-likelihood is available only when the held-out normalization is explicitly supplied. Likelihood-ratio coverage and Wilks assumptions are never inferred automatically.

KATRIN grid lookup preserves the archived absolute-chi-square surface. Exact and nearest-bin access are available. Interpolation remains unauthorized because neither the source contract nor preregistration froze an interpolation rule.

## Authorization boundary

The module is callable by `NON_PHYSICAL_TEST_FIXTURE` controls and policy-authorized baseline models. It is not a back door to the frozen evaluator. `run-validation --model LSC`, M5, and M6 are rejected before a statistic is computed. `LSC_used` is false in every Step 04 execution manifest.
