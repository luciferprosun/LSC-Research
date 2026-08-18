# STEP 07E aborted-run forensics

Status: **PASS**

Required verdict: `NO_RESULT_EXPOSURE_BEFORE_PRIMARY_RUN`

## Chronology

1. Pre-fit revision R1 was frozen at `2026-08-16T16:56:48Z`.
2. Attempt R1 aborted at `2026-08-16T16:58:55Z` with
   `NameError: name 'false' is not defined`.
3. Pre-fit revision R2 was frozen at `2026-08-16T16:58:55Z`.
4. Attempt R2 aborted at `2026-08-16T17:00:28Z` with the same exception from
   three remaining invalid JSON-style boolean names.
5. Pre-fit revision R3 was frozen at `2026-08-16T17:00:28Z`; only then did the
   single primary determination complete and serialize its result.

## Reconstructed execution point

Both aborted attempts loaded the frozen inputs, passed the pre-fit audit,
constructed the evaluator and objective, invoked the bounded optimizer, and
computed local numerical values in process memory. Python evaluates a returned
dictionary from left to right. In both revisions it then encountered an
undefined lowercase `false` while constructing that dictionary. Therefore:

- data loaded: **YES**;
- objective evaluated: **YES**;
- optimizer began and completed sufficiently to hold local values: **YES**;
- result dictionary completed: **NO**;
- result serialized or result file created: **NO**;
- result printed or returned: **NO**;
- alpha/result exposed to a decision maker: **NO**.

The local, unreturned optimizer value is not treated as a completed scientific
result. The incident records accurately state
`ABORTED_BEFORE_RESULT_CONSTRUCTION_OR_SERIALIZATION`; they do not incorrectly
claim that the objective was never evaluated.

## Source reconstruction

The R1 determination-source SHA-256 was
`86070aded79a0c9c5e959d441414bed83f5598d8f4a9d69a65a741c3e94bc02b`.
Replacing exactly the first two invalid boolean names with Python `False`
reconstructs the R2 SHA-256
`86c0bd75072da14f6260eeca9b82ed3c8a95b6148022f25054beadf8ffaa86b3`.
Replacing the remaining three names reconstructs the R3 SHA-256
`fc8b7e1517b98995e6a140aa190d264fa2f19c1899d20927996558bcf9818879`.
No other source byte was needed to explain either transition.

The frozen physics, data rows, hashes, response, support domain, bounds,
objective, covariance, nuisance policy, optimizer settings, interval rule, and
success criteria did not change. R3 also added the pre-fit AST gate that
rejects loaded names `false`, `true`, and `null`.

## Preregistration assessment

Because neither aborted result object was completed, emitted, written, or
available to the decision maker, no scientific/configuration choice was made
after result exposure. The preserved incident and freeze revisions provide a
complete adverse software-attempt trail. Preregistration integrity is not
invalidated by these two disclosed technical aborts.

Final verdict: `NO_RESULT_EXPOSURE_BEFORE_PRIMARY_RUN`.
