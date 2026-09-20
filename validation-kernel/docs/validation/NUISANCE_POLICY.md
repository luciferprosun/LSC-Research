# Nuisance policy

The registry covers source activity, extraction efficiency, counting efficiency, background/radon, geometry, detector efficiency, gallium capture cross section, isotope-transition uncertainty, experiment normalization and shared nuclear uncertainty.

Each category fixes scope, experiment, correlation axes, published-covariance availability and allowed treatment scenarios. Unknown correlation is never converted into a numerical correlation silently.

Three operations remain distinct:

1. baseline fitting may optimize only the named baseline parameters on a preregistered calibration subset;
2. nuisance profiling may vary only declared nuisance parameters under declared priors/covariance;
3. frozen LSC evaluation may vary no frozen LSC parameter.

If a nuisance is mathematically entangled with a frozen LSC parameter, the run must fail closed until the parameter boundary is specified. Profiling a field in the `FROZEN_LSC` scope raises `FrozenModelRefitForbidden`.
