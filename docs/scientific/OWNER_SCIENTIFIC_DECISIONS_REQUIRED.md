# Owner Scientific Decisions Required Before LSC 6.4.0 Design

## Decision gate

Algebra has removed the representational ambiguities. The three questions below are the remaining physical choices. They cannot be selected by software engineering or by goodness-of-fit.

## Decision 1: Choose the response-function hypothesis

### A. Physically derived transferable functions (recommended)

Supply explicit `S_a(E,t)` and `h_A,a(E,t)` forms from an a-priori detector, geometry, cross-section, or other named mechanism. State their domains, normalizations, zone-transfer rule, bounds, and any external constants.

**Consequence:** transferable and falsifiable; may permit zero or few empirical amplitudes; requires LSC 6.4.0 because the functional forms are new physical content.

### B. Finite preregistered phenomenological basis

Choose a small basis before fitting, then determine only its declared coefficients from one frozen historical development set.

**Consequence:** reproducible but explicitly retrospective and non-blind; parameter count and identifiability must be justified; requires LSC 6.4.0.

### C. Observation-specific weighted moments

Treat only `beta0_a=<S_a>` and `betaA_a=<n^T B_a n>` as parameters for a fixed dataset contract.

**Consequence:** removes unobservable functional detail locally but cannot transfer to new spectra, geometries, or exposure schedules; this is a restricted methodological profile, not a complete transferable LSC successor.

**Owner action:** choose A, B, or C. For A or B, provide the exact candidate equations before implementation.

## Decision 2: Choose the anisotropic tensor family

### A. Shared normalized uniaxial tensor with an a-priori axis (recommended for a full M6 model)

Use a Frobenius-normalized tensor proportional to `u u^T - I/3`, with the physical ICRS direction `u` fixed from a named hypothesis before validation.

**Consequence:** two orientation degrees are fixed rather than fitted; anisotropy can reduce to one signed response amplitude after the response shape is frozen; minimal, identifiable in principle, and falsifiable. Uniaxiality and the axis are new physical assumptions, so this requires 6.4.0.

### B. Shared general 3-by-3 symmetric traceless tensor

Retain four continuous tensor shape/orientation degrees after Frobenius normalization.

**Consequence:** closer to the unrestricted E3-E4 form but underidentified by current BEST summary observables; requires substantially richer directional data and 6.4.0 explicit specification.

### C. Disable the anisotropic sector

Publish only a trace response model and keep E3/E4/E11/E12 inactive.

**Consequence:** simplest and most identifiable restricted M5 model, but it is not a complete trace-plus-traceless M6 successor and cannot make directional claims.

**Owner action:** choose A, B, or C. If A, name the physical axis and its provenance; coordinate axes alone are not a physical hypothesis.

## Decision 3: Choose cross-zone and cross-experiment sharing semantics

### A. One physical tensor and one response law shared across experiments/zones (recommended)

Zone dependence enters only through authoritative source, geometry, detector, and exposure weights.

**Consequence:** strongest transfer predictions, lowest parameter count, and clearest falsifiability. Any experiment-specific calibration factor must remain a nuisance, not an independent LSC tensor.

### B. Zone tensors derived deterministically from a frozen geometry law

Allow `T_a` to differ only through an explicit, predeclared mapping from surveyed detector geometry.

**Consequence:** transferable if the mapping is universal and fixed before evaluation; the mapping is new physical/model content and requires 6.4.0.

### C. Independently fitted zone or experiment tensors

Permit unrelated `T_a` objects.

**Consequence:** at least four normalized tensor degrees per zone, weak cross-experiment transfer, and severe non-identifiability. This option is not recommended and may make the model indistinguishable from detector systematics.

**Owner action:** choose A, B, or C. A free post-hoc mixture is prohibited.

## Decisions already resolved without owner input

- Use the gauge-invariant response objects `S_a=lambda0*f0_a` and `B_a=lambdaA*fA_a*A_a`.
- Use three spatial dimensions for the STF tensor.
- Use Frobenius norm only as a factorization gauge representative.
- Use the normalized E1 measure with denominator `N0_a`.
- Use `Rpred=NLSC/N0` as the primary observable binding and treat E7 as its residual diagnostic.
- Keep `theta` for LSC physical parameters and `eta` for nuisances.
- Treat BEST inner and outer ratios as the two independent coordinates; the double ratio is derived.

These decisions remove redundancy or follow from the existing ratio equations. They do not select new physical predictive content.
