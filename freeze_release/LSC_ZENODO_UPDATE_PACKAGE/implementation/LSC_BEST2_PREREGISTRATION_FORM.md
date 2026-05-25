# LSC BEST-2 Preregistration Form

Status: Step 3 implementation artifact  
Purpose: preregistration-ready freeze form  

## 1. Project Identity

- project: LSC Pre-BEST-2 Freeze Validation
- theory status: unvalidated phenomenological framework
- active freeze state: LSC 6.3.0
- no LSC 6.4 creation: confirmed

## 2. Frozen Equations

Reference:

- Step 1 `LSC_ACTIVE_EQUATION_SET.md`

Checklist:

- [ ] active equation set copied verbatim;
- [ ] deprecated equation families excluded;
- [ ] dimensional-review items labeled;
- [ ] no new equation introduced.

## 3. Frozen Parameter Structure

Checklist:

- [ ] all active parameters listed;
- [ ] nuisance parameters listed;
- [ ] bounds specified;
- [ ] tensor orientation specified if anisotropy tested;
- [ ] `f0_a` and `fA_a` functional forms frozen if used.

## 4. Frozen Datasets

Checklist:

- [ ] BEST data version listed;
- [ ] GALLEX data version listed;
- [ ] SAGE data version listed;
- [ ] BEST-2 target data access conditions listed;
- [ ] external veto data versions listed;
- [ ] missing data declared.

## 5. Frozen Validation Hierarchy

M0-M6 must all be included:

- [ ] M0;
- [ ] M1;
- [ ] M2;
- [ ] M3;
- [ ] M4;
- [ ] M5;
- [ ] M6.

## 6. Prohibited Post-Hoc Actions

Prohibited:

- adding mechanisms;
- adding equations;
- adding tensor structures;
- changing tensor orientation after data inspection;
- suppressing covariance limitations;
- dropping M4;
- dropping M3;
- changing success/failure criteria;
- using AI consensus as evidence.

## 7. Allowed Statistical Interpretations

Allowed:

- exploratory sensitivity;
- validation-grade comparison only if covariance and data requirements are met;
- unresolved ambiguity;
- failure;
- negative result.

Not allowed:

- discovery claim;
- sterile-neutrino exclusion claim;
- confirmed new physics claim.

## 8. Failure Conditions

Failure or major weakening if:

- M4 reproduces M6;
- M1/M2 perform as well as M5/M6 after penalties;
- LOO unstable;
- cross-experiment transfer fails;
- covariance unavailable for claimed validation;
- external veto excludes required parameter space.

## 9. Publication Discipline

Every release must include:

- data versions;
- covariance status;
- M0-M6 results;
- M4 status;
- LOO results;
- external veto status;
- negative outcomes;
- unresolved blockers.

