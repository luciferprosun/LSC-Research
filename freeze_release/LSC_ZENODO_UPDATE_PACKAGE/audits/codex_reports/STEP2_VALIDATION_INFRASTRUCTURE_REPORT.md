---
title: "Kodeks STEP2 Validation Infrastructure"
date: "2026-05-25"
toc: true
toc-depth: 3
geometry: margin=2cm
fontsize: 10pt
---

# Executive Summary

STEP 2 defines the validation infrastructure required before BEST-2-era analysis, freeze archival or public release. It does not extend LSC. It does not introduce new equations, new physics, new tensor structures, new mechanisms, new particle claims or LSC 6.4.

The core Step 2 answer is:

> LSC can only be scientifically tested by comparing the frozen trace/traceless detector-response framework against mandatory null, normalization, cross-section/systematics, sterile-neutrino and detector-systematics baselines under covariance-aware, preregistered, externally constrained validation.

# Validation Architecture

## M0-M6 Hierarchy

| Model | Role |
|---|---|
| M0 null / published baseline | Reference expectation |
| M1 scalar normalization only | Tests global scale explanation |
| M2 cross-section / source-systematics only | Tests nuclear/source explanation |
| M3 sterile-neutrino benchmark | Required physics competitor |
| M4 detector-systematics benchmark | Required primary mundane competitor |
| M5 LSC trace-only | Tests scalar LSC response |
| M6 LSC trace + traceless anisotropy | Tests full frozen LSC template |

M4 is primary. If M4 reproduces M6-level structures, LSC is not distinguishable.

## Required Comparisons

- M6 vs M0, M1, M2, M3, M4 and M5.
- M5 vs M1/M2.
- M4 vs M5/M6.
- Leave-one-out stability.
- Cross-experiment transfer.
- External veto survival.

## What Counts As Validation

Validation requires:

- M5/M6 outperform simpler baselines after penalties;
- M6 outperforms M4 detector-systematics baseline;
- LOO remains stable;
- cross-experiment transfer succeeds;
- covariance-aware uncertainty is used or limitation explicitly blocks strong claims;
- external vetoes are survived quantitatively;
- negative and null outcomes are reported.

## What Does Not Count As Validation

- exact anchor fits;
- visual agreement;
- diagonal-error chi-squared with missing covariance;
- AI audit agreement;
- fit improvement without complexity penalty;
- sterile-neutrino baseline omission;
- detector-systematics baseline omission;
- post-hoc tensor orientation;
- adding terms after seeing failures.

# M4 Competitor Structure

| M4 Component | LSC Structure It Can Mimic |
|---|---|
| calibration drift | trace response or false time trend |
| source normalization uncertainty | global deficit / trace term |
| cross-section normalization | trace term |
| extraction efficiency asymmetry | zone structure / false anisotropy |
| detector geometry asymmetry | lab-frame anisotropy |
| background subtraction uncertainty | trace or time-dependent residual |
| environmental drift | false time/sidereal trend |
| covariance incompleteness | false significance |
| timing/orientation artifacts | false traceless tensor |

Required rule:

> If M4 matches or exceeds M6 after penalties, LSC is not distinguishable.

# Covariance Policy

## Required Covariance Structures

| Data Object | Class | Current Status |
|---|---|---|
| BEST statistical covariance | ESSENTIAL | Currently unavailable |
| BEST systematic covariance | ESSENTIAL | Currently unavailable |
| GALLEX covariance | IMPORTANT | Currently unavailable |
| SAGE covariance | IMPORTANT | Currently unavailable |
| cross-experiment covariance | IMPORTANT | Currently unavailable |
| external veto covariance | IMPORTANT | Currently unavailable |

## Forbidden Shortcuts

- final likelihood claims from diagonal-only errors;
- ignoring correlated systematics;
- suppressing covariance limitations;
- silently dropping experiments;
- fitting anisotropy without orientation metadata;
- claiming precision from rounded summary tables.

# Data Limitations

| Requirement | Class | Validation Impact |
|---|---|---|
| BEST extraction table | ESSENTIAL | full likelihood and time/zone validation |
| BEST counter efficiencies | ESSENTIAL | detector/systematics separation |
| BEST source calibration details | ESSENTIAL | source normalization nuisance |
| exposure timestamps | ESSENTIAL for anisotropy | sidereal tests |
| detector orientation | ESSENTIAL for anisotropy | lab/celestial separation |
| environmental logs | IMPORTANT | drift/background checks |
| GALLEX exposure data | IMPORTANT | transfer validation |
| SAGE run-by-run data | IMPORTANT | isotope/source validation |

# External Veto Logic

| Veto | Must Check | Falsifies Region If |
|---|---|---|
| KATRIN | beta-spectrum energy distortion | Gallium response implies excluded KATRIN distortion |
| IceCube | anisotropy/tensor constraints | mapped tensor amplitude exceeds bounds |
| SME/Lorentz-style bounds | fixed tensor implications | implied coefficients exceed published limits |
| solar neutrino consistency | scalar response transfer | required parameters break solar constraints |
| standard oscillation fits | compatibility with 3-flavor results | global fits exclude required behavior |
| detector calibration literature | source/cross-section/extraction uncertainties | M2/M4 reproduces M6-level structures |

# Preregistration Discipline

Before fitting:

- freeze active parameters;
- freeze nuisance parameters;
- freeze equation set from Step 1;
- freeze `f0_a` and `fA_a` if used;
- freeze tensor orientation if anisotropy is tested;
- freeze M0-M6 implementations;
- freeze success/failure criteria;
- freeze external veto thresholds.

Forbidden after data inspection:

- new mechanisms;
- new tensor structures;
- new particle claims;
- selective baseline removal;
- covariance suppression;
- unexplained data exclusion;
- changing success criteria;
- adding external-veto exceptions.

Negative outcomes are valid outcomes.

# Risk Matrix

| Risk | Severity | Likelihood | Mitigation | Status |
|---|---|---|---|---|
| detector/systematics degeneracy | Critical | High | implement M4 | active blocker |
| tensor underidentifiability | Critical | High | fixed orientation + metadata | active blocker |
| covariance absence | Critical | High | obtain covariance or label exploratory | active blocker |
| overfitting | Critical | High | LOO, penalties, model reduction | active blocker |
| metadata incompleteness | Critical | High | timestamps/orientation/environment logs | active blocker |
| external veto conflict | High | Medium | KATRIN/IceCube/SME/solar checks | unresolved |
| parameter instability | High | Medium | LOO and bounds reporting | unresolved |
| false anisotropy detection | Critical | High | lab/celestial separation | active blocker |
| statistical overclaiming | High | High | covariance policy and claim boundary | active blocker |

# Integrated Audit Findings

## Claude / Physics Audit

- physical underderivation remains a risk;
- tensor freedom is too large for current data;
- covariance absence blocks statistical claims;
- Lorentz/SME and external vetoes require quantitative treatment.

## Gemini

- freeze with downgraded claims;
- public data are insufficient for directional tensor validation;
- covariance and orientation metadata are fatal missing inputs.

## DeepSeek

- detector and analysis artifacts can mimic LSC trace/traceless structures;
- M4 must be a primary competitor;
- BEST-2 must use systematic-breaking and blinded analysis discipline.

## Kimi

- freeze the compressed core;
- keep M0-M6;
- enforce validation discipline;
- archive redundant equations and historical mechanisms.

# Remaining Blockers

Full likelihood validation is blocked by:

- missing covariance matrices;
- missing extraction-level data;
- missing orientation/timestamp metadata;
- missing quantitative M4 implementation;
- missing external veto mappings;
- unresolved tensor identifiability;
- observed LOO instability in prior analysis.

# Final Recommendations Before Step 3

Step 3 should not expand theory.

Step 3 should produce validation implementation artifacts:

1. Machine-readable data requirement matrix.
2. M0-M6 analysis specification templates.
3. M4 detector-systematics baseline schema.
4. Covariance placeholder and sensitivity-analysis template.
5. Leave-one-out execution plan.
6. Cross-experiment transfer plan.
7. External veto data-request checklist.
8. Preregistration form for BEST-2-era analysis.

# Final Validation Check

No new physics introduced: yes.  
No new equations invented: yes.  
Detector/systematics competition remains active: yes.  
Negative outcomes remain valid outcomes: yes.  
Statistical limitations are explicit: yes.  

