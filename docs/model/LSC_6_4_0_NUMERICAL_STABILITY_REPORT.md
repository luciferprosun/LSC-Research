# LSC 6.4.0 numerical stability report

## Scope

This report covers the A2 cross-section representation, its logarithmic derivative, source-line integration, the first-order domain, deterministic execution, and fail-closed boundaries. It uses no measured gallium deficit to select a numerical method.

## Cross-section audit

- 58 strictly increasing energy points.
- 58 finite, strictly positive cross sections.
- Natural cubic spline positive and finite on a 32,769-point audit grid over `[0.240, 30.000] MeV`.
- Analytic derivative finite on the same grid.
- Exact reproduction of every tabulated knot within binary64 rounding.
- No extrapolation.

## A2 equivalence

For every frozen source line, the implementation verifies

`d ln sigma / d ln E = E sigma'(E) / sigma(E)`.

A centered finite difference in logarithmic energy agrees with the analytic spline derivative. The independent reference implementation uses its own tridiagonal natural-spline solver and polynomial derivative; it does not call the SciPy derivative path.

## Source-line response values

| Isotope | Energy MeV | `F_m` |
|---|---:|---:|
| Cr51 | 0.7524 | 1.8223393118256894 |
| Cr51 | 0.7518 | 1.82204616 |
| Cr51 | 0.7465 | 1.8180806774054432 |
| Cr51 | 0.4323 | 1.383777406820946 |
| Cr51 | 0.4317 | 1.39120710 |
| Cr51 | 0.4264 | 1.472431965363944 |
| Ar37 | 0.8138 | 1.7108295711583716 |
| Ar37 | 0.8135 | 1.71175377 |
| Ar37 | 0.8107 | 1.7204094952722646 |

Rounded entries in this human-readable table do not replace machine output or golden vectors.

## Alpha bounds

The bounds have different meanings and are not conflated:

| Class | Result | Meaning |
|---|---|---|
| `THEORY_BOUND` | unavailable | no strict source-derived first-order cutoff exists |
| spline support for all lines | `[-0.5747389495096434, 3.607238025076703]` | all `E exp(alpha_0)` remain within the payload |
| linear positivity lower bound | `alpha_0 > -0.5487452273628239` | all line-level `1+alpha_0 F_m` remain positive |
| `PREREGISTERED_ANALYSIS_BOUND` | `[-0.06137569484389956, 0.09541395625505644]` | maximum relative first-order truncation error at frozen lines is at most 1% |

The analysis bound was frozen before the result and cannot be widened to rescue a boundary outcome.

## Golden vectors

Fifteen vectors pass:

- two exact null cases;
- four signed source cases;
- a universal-sharing label pair;
- two synthetic integration cases;
- two included boundary cases;
- explicit failures for unsupported energy, out-of-bound `alpha_0`, and tensor input.

The numerical tolerance is `1e-13` for the frozen source cases. The null result is exact: `alpha_0=0` produces `S_a=0` and `R_pred=1`.

## Determinism

Canonical JSON serialization forbids NaN and sorts object keys. Prediction hashes depend on the exact input. Repeated production execution is byte-for-byte identical on the frozen environment. Two independent verification processes reproduce all golden vectors and the frozen adverse determination result.
