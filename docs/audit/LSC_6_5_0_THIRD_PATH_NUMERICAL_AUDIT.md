# LSC 6.5.0 third-path numerical audit

Status: **PASS**

## Independence and tolerances

`tools/audit_lsc650_third_path.py` imports neither the production evaluator nor
the existing reference evaluator. It reads the frozen CSV/JSON inputs
directly, solves the 58-knot natural-cubic-spline system as a dense 60-digit
`Decimal` linear system with natural endpoint conditions, and evaluates the
direct numerator `sum q_i sigma(E_i exp(alpha_0))`.

Tolerances were declared in the source before comparison:

- general absolute: `5e-11`;
- boundary absolute: `5e-9`;
- domain absolute: `5e-15`;
- first-order bridge absolute: `5e-7`;
- parameter-root absolute: `5e-10`.

The independent inputs resolved to cross-section SHA-256
`55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5`
and source-line SHA-256
`ecfd559f0ccbb5da7040b42d73f2abc2c49a0637993964c621f6e145da70c70e`.

## Results

The independently derived joint source domain was
`[-0.5747389495096434, 3.6072380250767027]`; its largest absolute difference
from the stored binary64 domain was `1.5066428236193636e-16`.

Exact lower/upper boundaries and points `1e-12` inside both boundaries passed.
Points `1e-12` outside both boundaries returned
`FAIL_CLOSED_UNSUPPORTED_DOMAIN`. There was no clipping, extrapolation, or
substitution.

All 20 numerical golden vectors passed; the largest absolute difference was
`5.4569682106375694e-12`. A separate comparison harness checked every one of
the nine supported Cr51/Ar37 lines at ten alpha values: near both boundaries,
moderate `+/-0.3`, both frozen interval endpoints, frozen `alpha_0`, null, and
small `+/-1e-6`. All `90/90` comparisons passed; the maximum absolute
difference from production was `7.275957614183426e-12`.

The null limit was exactly one. The central derivative of the exact response
at zero agreed with the independently evaluated LSC 6.4.0 linear A2 generator
for both isotopes; the maximum bridge difference was
`5.122204552144778e-14`.

The monotone third-path root solution produced
`alpha_0 = -0.14388795520867112`, a difference of
`6.490719842836765e-12` from the frozen optimizer result. The two interval
endpoint differences were below `3.4e-16`. The independently evaluated
objective at the frozen parameter was approximately `2.16995e-20`.

Verdict: `PASS_THIRD_INDEPENDENT_NUMERICAL_PATH`.
