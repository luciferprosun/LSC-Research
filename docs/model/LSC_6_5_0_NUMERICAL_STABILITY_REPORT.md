# LSC 6.5.0 numerical stability report

Status: **PASS for the executable exact finite-dilation profile**

The production path uses IEEE-754 binary64, SciPy's frozen natural cubic spline, `math.exp`, and `math.fsum`. It performs no extrapolation and no silent clipping. Closed-support roundoff within four ULPs is normalized explicitly and reported per line.

Checks passed:

- 58 cross-section knots are finite, ordered, strictly positive, and reproduced by the spline;
- the spline remains finite and positive on a 32,769-point support grid;
- all authoritative 51Cr and 37Ar lines remain in support throughout their derived alpha domain;
- the exact ratio is positive and finite;
- `K(E,0)=1` and `R_pred(0)=1` exactly;
- the central first derivative at zero agrees with the frozen LSC 6.4 linear generator;
- scale-transform composition holds at the kernel level;
- direct numerator evaluation and baseline-measure-times-ratio evaluation agree;
- production and independent stdlib spline/integration implementations agree across source lines, an alpha grid, and boundary-adjacent cases;
- 29 golden vectors pass, including 20 numerical cases and 9 fail-closed cases;
- repeated JSON serialization is bitwise deterministic.

The upper closed-domain endpoint produces a platform-level rounding excursion of approximately one ULP for the largest 37Ar line. The evaluator maps only this explicitly detected endpoint roundoff to the exact support endpoint and sets `support_endpoint_roundoff_normalized=true`. Values farther outside support fail closed.

No derivative approximation is used in production prediction. The derivative remains only a lineage regression test.
