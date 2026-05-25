# LSC Validation Protocol

Status: Step 2 validation infrastructure  
Scope: validation architecture only  
Theory status: constrained, unvalidated phenomenological validation framework  

## 1. Purpose

This protocol defines how LSC can be tested, constrained, weakened, falsified or rejected without extending the framework.

It does not:

- add mechanisms;
- add equations;
- create LSC 6.4;
- add tensor structures;
- add particle claims;
- reinterpret LSC as established physics.

## 2. Required Model Hierarchy

Every validation run must compare all active baselines:

| Model | Name | Required Role |
|---|---|---|
| M0 | null / published baseline | Reference expectation |
| M1 | scalar normalization only | Tests whether deficit is simple scale shift |
| M2 | cross-section / source-systematics only | Tests nuclear/source normalization explanation |
| M3 | sterile-neutrino benchmark | Required physics competitor |
| M4 | detector-systematics benchmark | Required primary mundane competitor |
| M5 | LSC trace-only | Tests scalar LSC response |
| M6 | LSC trace + traceless anisotropy | Tests full frozen LSC template |

M4 is a primary competitor to M6. If M4 reproduces M6-level structures, LSC is not distinguishable.

## 3. Mandatory Comparisons

Validation must report:

- M6 vs M0;
- M6 vs M1;
- M6 vs M2;
- M6 vs M3;
- M6 vs M4;
- M5 vs M1/M2;
- M6 vs M5;
- M4 vs M5/M6;
- cross-experiment transfer performance;
- leave-one-out stability.

No single comparison is sufficient.

## 4. Penalty Policy

All model comparisons must penalize complexity.

Allowed penalty classes:

- AIC-style information penalty;
- BIC-style information penalty;
- cross-validation penalty;
- preregistered nuisance-parameter penalty.

Forbidden:

- comparing raw fit quality only;
- counting tensor degrees of freedom as free but not penalized;
- adding nuisance terms without reporting them;
- fitting multiple variants and reporting only the best.

## 5. Covariance Policy

The preferred statistic is covariance-aware.

Requirements:

- use full statistical and systematic covariance when available;
- include correlated source-strength, cross-section, extraction and detector-efficiency terms;
- clearly label any diagonal or block-diagonal approximation as exploratory;
- never claim likelihood-level validation from diagonal-only errors when full covariance is missing.

If covariance is unavailable:

- validation status is limited to exploratory;
- no discovery, exclusion or strong preference claim is allowed;
- missing covariance must be listed as a blocker.

## 6. Leave-One-Out Requirements

LOO is mandatory because exact anchor fits are insufficient.

Required LOO modes:

- omit BEST inner, predict BEST inner;
- omit BEST outer, predict BEST outer;
- omit GALLEX combined/split, predict GALLEX;
- omit SAGE 51Cr, predict SAGE 51Cr;
- omit SAGE 37Ar, predict SAGE 37Ar;
- omit each experiment group, predict the omitted group.

Validation requires:

- residuals remain stable under omission;
- parameters do not swing into unrelated values;
- M6 does not degrade into a flexible interpolation of anchors;
- M4 and M3 are evaluated under the same omissions.

LOO instability is evidence against current model complexity.

## 7. Cross-Experiment Transfer Rules

Required transfers:

- fit BEST, predict GALLEX/SAGE;
- fit GALLEX/SAGE, predict BEST;
- fit 51Cr sources, predict 37Ar source behavior;
- fit inner/outer BEST split, test external gallium experiments.

Rules:

- transfer must use frozen mappings;
- no experiment-specific refit is allowed for a claimed prediction;
- failures must be reported, not absorbed into new nuisance terms.

## 8. External Veto Policy

External vetoes are hard constraints.

At minimum:

- KATRIN energy-response constraints;
- IceCube or SME-style tensor/anisotropy constraints where relevant;
- solar-neutrino consistency;
- standard three-flavor oscillation fits;
- detector calibration and cross-section literature.

If a parameter region improves Gallium residuals but violates a veto, it is not viable.

## 9. Detector/Systematics Separation Rules

Detector/systematics explanations must be modeled before LSC preference is claimed.

Required separation tests:

- source activity normalization;
- gallium cross-section normalization;
- inner/outer extraction efficiency asymmetry;
- geometry asymmetry;
- background subtraction drift;
- environmental drift;
- lab-frame orientation artifacts;
- covariance incompleteness.

If any of these reproduce LSC-like structures, LSC is unresolved or not distinguishable.

## 10. Preregistration Rules

Before BEST-2 fitting:

- freeze model equations from Step 1;
- freeze active parameters and bounds;
- freeze `f0_a` and `fA_a` if used;
- freeze orientation assumptions if anisotropy is claimed;
- freeze M0-M6 implementations;
- freeze success/failure criteria;
- freeze treatment of missing data;
- freeze external veto thresholds.

After data inspection:

- no new mechanism may be added under the same freeze;
- no selective baseline removal is allowed;
- no tensor reorientation is allowed;
- no covariance suppression is allowed.

## 11. What Counts As Validation

Validation requires all of:

- M5/M6 outperform simpler baselines after penalties;
- M6 outperforms M4 detector-systematics baseline;
- LOO remains stable;
- cross-experiment transfer succeeds;
- covariance-aware uncertainty is used or limitation explicitly blocks strong claims;
- external vetoes are survived quantitatively;
- negative and null outcomes are reported.

## 12. What Does Not Count As Validation

Not validation:

- exact anchor fits;
- visual agreement;
- diagonal-error chi-squared with missing covariance;
- AI audit agreement;
- fit improvement without complexity penalty;
- sterile-neutrino baseline omission;
- detector-systematics baseline omission;
- post-hoc tensor orientation;
- adding terms after seeing failures.

## 13. What Counts As Failure

Failure or major weakening occurs if:

- M4 reproduces M6-level structures;
- M1/M2 perform as well as M5/M6 after penalties;
- LOO remains unstable;
- cross-experiment transfer fails;
- anisotropy collapses into scalar normalization under covariance;
- external vetoes exclude required parameter regions;
- tensor parameters are unidentifiable.

## 14. What Counts As Unresolved Ambiguity

Unresolved:

- summary data support a deficit scale but cannot separate trace and traceless components;
- covariance is missing;
- orientation/timestamp metadata are missing;
- M4 is incomplete;
- external veto mapping is qualitative only;
- parameter degeneracy remains.

