# LSC 6.5.0 cross-section accounting audit

Status: **PASS**

Audit input: frozen LSC 6.5.0 RC1 at input commit
`1f715b9b8777f89d17a84d340a24107531ccaed4`.

## Accounting identity

For source line `i`, collect every conventional factor other than the capture
cross section into `q_i`. The frozen baseline measure is

`B_i = q_i sigma(E_i)`.

It therefore contains exactly one conventional capture cross section. The
production denominator and numerator are

`D = sum_i q_i sigma(E_i)`

`N = sum_i B_i [sigma(E_i exp(alpha_0)) / sigma(E_i)]`

and hence, by direct cancellation,

`N = sum_i q_i sigma(E_i exp(alpha_0))`.

The response factor replaces the one baseline `sigma(E_i)` in the numerator
with one transformed `sigma(E_i exp(alpha_0))`. It neither adds a second cross
section nor removes the denominator cross section.

## Code audit

`src/lsc_kernel/lsc650/evaluator.py` implements the identity explicitly:

- lines 34--38 construct `q_i` and then `B_i = q_i sigma(E_i)`;
- line 39 forms `B_i K_i`;
- line 40 independently forms the direct term `q_i sigma(E_i exp(alpha_0))`;
- lines 58--65 sum the unchanged denominator and transformed numerator, then
  fail if the two independent numerator forms disagree.

`src/lsc_kernel/lsc650/cross_section.py` lines 211--230 implement
`E_i exp(alpha_0)` and the exact ratio. The production path does not call the
derivative or linear generator. Natural-cubic interpolation is frozen and has
`extrapolate=False`; requests outside support fail closed.

The strict input contract preserves source-line energies and branching
fractions for authorized inputs. Activity, exposure, conventional
probability, geometry, detector efficiency, and nuisance/covariance labels
remain conventional factors. No one of them is passed through the dilation.

## Findings

- `sigma^2`: absent;
- missing numerator `sigma`: absent;
- duplicated normalization: absent;
- altered denominator: absent;
- clipping or extrapolation: absent;
- exact one-for-one replacement invariant: enforced at runtime;
- critical findings: **0**.

Verdict: `PASS_EXACTLY_ONE_BASELINE_CROSS_SECTION_REPLACED`.
