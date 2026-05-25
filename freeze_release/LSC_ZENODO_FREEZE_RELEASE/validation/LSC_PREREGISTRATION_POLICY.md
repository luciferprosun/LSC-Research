# LSC Preregistration Policy

Status: Step 2 validation infrastructure  
Purpose: prevent post-hoc theory drift before BEST-2-era analysis  

## 1. Rule

No BEST-2 validation claim is valid unless the analysis was preregistered before target data inspection.

## 2. Frozen Parameter Policy

Before fitting:

- list all active parameters;
- list all nuisance parameters;
- define parameter bounds;
- define which parameters are fixed;
- define which parameters are fitted;
- define penalty method;
- define failure behavior if parameters hit bounds.

Forbidden:

- adding parameters after fit failure;
- widening bounds after seeing data;
- hiding nuisance terms;
- treating tensor components as free without penalty.

## 3. Frozen Equation Policy

Before fitting:

- identify the active equation set from Step 1;
- identify any review-limited equations;
- exclude deprecated equation families;
- freeze all functional forms used in computation.

Forbidden:

- introducing new equations after data inspection;
- reviving PBH/curvature mechanisms;
- reclassifying historical equations as active because they improve a fit.

## 4. Frozen Orientation Policy

If anisotropy or sidereal behavior is tested:

- tensor orientation must be fixed before fitting;
- coordinate frame must be declared;
- lab-to-celestial transform inputs must be specified;
- detector orientation metadata must be included;
- environmental covariates must be handled.

Forbidden:

- selecting orientation after seeing residuals;
- fitting arbitrary tensor direction with insufficient data;
- claiming celestial anisotropy from lab-frame artifacts.

## 5. Anti-Posthoc Rules

Forbidden after data inspection:

- new mechanisms;
- new tensor structures;
- new particle claims;
- selective baseline removal;
- covariance suppression;
- unexplained data exclusion;
- changing success criteria;
- adding external-veto exceptions.

## 6. Blinded Analysis Rules

Recommended:

- freeze code and documents before unblinding;
- run M0-M6 on blinded or scrambled labels where possible;
- define all plots and tables before result inspection;
- archive negative and null outputs.

## 7. Allowed Tuning Boundaries

Allowed only before target data inspection:

- numerical implementation debugging;
- unit conversion fixes;
- documented data parsing correction;
- replacing placeholder covariance with official covariance;
- correcting transcription errors with provenance.

Not allowed:

- tuning response functions to match target residuals;
- changing tensor orientation after seeing residual phase;
- dropping M4 because it outperforms M6;
- changing external veto thresholds.

## 8. Publication Discipline

Every public release must state:

- validation grade: exploratory or validation-grade;
- which data were missing;
- which covariance assumptions were used;
- whether M4 was implemented;
- whether LOO passed;
- whether external vetoes were quantitative;
- whether negative outcomes occurred.

## 9. Negative-Result Acceptance

Negative outcomes are valid outcomes.

Examples:

- M4 beats M6;
- M1/M2 explain trace response;
- anisotropy unidentifiable;
- LOO unstable;
- external veto excludes required region;
- metadata insufficient for sidereal test.

These must be archived and cannot be rewritten as support.

## 10. Explicit Prohibitions

Prohibited:

- retrospective tuning;
- new mechanisms after fitting;
- selective baseline removal;
- covariance suppression;
- AI-consensus-as-evidence;
- theory expansion under Step 2;
- LSC 6.4 creation.

