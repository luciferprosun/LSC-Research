# LSC Failure Modes And Risk Matrix

Status: Step 2 validation infrastructure  

## 1. Risk Matrix

| Risk | Severity | Likelihood | Mitigation | Freeze Status | Unresolved Dependencies |
|---|---|---|---|---|---|
| detector/systematics degeneracy | Critical | High | implement M4 and compare against M6 | active blocker | detector calibration, extraction, background model |
| tensor underidentifiability | Critical | High | predefine orientation, reduce free tensor use, require metadata | active blocker | timestamps, orientation, sufficient observables |
| covariance absence | Critical | High | obtain full covariance or label exploratory | active blocker | BEST/GALLEX/SAGE covariance |
| overfitting | Critical | High | LOO, cross-validation, penalties, model reduction | active blocker | independent validation data |
| metadata incompleteness | Critical | High | require orientation/timestamps/environment logs | active blocker | BEST-2 metadata release |
| external veto conflict | High | Medium | quantitative KATRIN/IceCube/SME/solar checks | unresolved | machine-readable constraints |
| parameter instability | High | Medium | LOO stability and bounds reporting | unresolved | covariance and transfer tests |
| LOO instability | High | Already observed | reduce model complexity or reject current complexity | active warning | independent datasets |
| false anisotropy detection | Critical | High | lab/celestial separation and M4 artifacts | active blocker | orientation/timestamp metadata |
| statistical overclaiming | High | High | enforce covariance policy and claim boundary | active blocker | review discipline |
| source normalization mimicry | High | Medium | independent source calibration nuisance | unresolved | source activity calibration records |
| cross-section mimicry | High | Medium | nuclear cross-section uncertainty propagation | unresolved | literature and uncertainty model |
| background drift | High | Medium | background-only runs and environmental logs | unresolved | timestamped logs |
| selective baseline removal | High | Medium | preregistration and mandatory M0-M6 reporting | prohibited | review enforcement |
| post-hoc tensor tuning | Critical | Medium | frozen orientation policy | prohibited | preregistration |

## 2. Failure Modes

### FM1. M4 reproduces M6

Result:

- LSC is not distinguishable.

Action:

- report as failure or unresolved depending on uncertainty;
- do not claim LSC support.

### FM2. M1/M2 explain trace response

Result:

- trace-only LSC is not supported.

Action:

- reduce claim to normalization/cross-section ambiguity.

### FM3. LOO remains unstable

Result:

- current complexity is overfit or underconstrained.

Action:

- reduce model complexity or defer validation.

### FM4. Cross-experiment transfer fails

Result:

- LSC lacks predictive generality.

Action:

- no cross-experiment support claim.

### FM5. External veto conflict

Result:

- affected parameter region is invalid.

Action:

- reject or revise only in a new preregistered version after human review.

### FM6. Metadata cannot identify anisotropy

Result:

- traceless/directional claim is untestable.

Action:

- freeze as unresolved; no anisotropy claim.

### FM7. Covariance remains unavailable

Result:

- likelihood-grade validation impossible.

Action:

- label all fits exploratory.

## 3. Risk Consolidation By Audit Source

| Audit Source | Confirmed Risk |
|---|---|
| Claude / physics audit | physical underderivation, tensor freedom, covariance, external vetoes |
| Gemini | data limitations, covariance absence, orientation metadata absence |
| DeepSeek | detector/systematics mimicry, extraction and background artifacts |
| Kimi | equation redundancy, trace/traceless freeze, LOO and validation discipline |

## 4. Freeze Status Summary

Frozen:

- risks must be reported;
- negative outcomes remain valid;
- M4 remains active;
- external vetoes remain hard constraints;
- covariance limitations block strong claims.

Not allowed:

- hiding risk;
- moving goalposts;
- expanding theory to avoid failure;
- using AI agreement as evidence.

