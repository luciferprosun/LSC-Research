# Nuisance engine

The nuisance layer represents every parameter by name, category, initial value, bounds, prior, effect vector, effect mode, and optional fixed value. Supported categories cover fixed, Gaussian-pull, bounded, correlated, shared-across-observations, and experiment-specific nuisances.

Effects are explicit additive or fractional-multiplicative vectors. Shared behavior is therefore a declared vector, not a name-based inference. Fixed values are never counted as fitted parameters. Floating values are optimized through the same policy-gated SciPy wrapper used by baselines, and Gaussian prior penalties are included in the profiled statistic. A supplied correlated prior covariance is validated through `CovarianceMatrix`.

Every profile reports:

- statistic before nuisance adjustment;
- profiled data statistic plus pull terms;
- fitted and fixed nuisance values;
- number of floating nuisance parameters;
- bounds, optimizer, tolerance, evaluations, convergence and warnings;
- covariance diagnostics.

The analytical shared-nuisance fixture has observation 2, prediction 1, unit data variance, and a unit Gaussian prior on one additive offset. The exact optimum is 0.5 and the total profiled chi-square is 0.5; the implementation reproduces both.

Nuisance profiling may not alter any frozen LSC parameter. The `NoRefitPolicy` checks the target model and parameter scope before optimization.
