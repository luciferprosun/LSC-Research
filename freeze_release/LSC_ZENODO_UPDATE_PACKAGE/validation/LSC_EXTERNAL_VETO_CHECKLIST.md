# LSC External Veto Checklist

Status: Step 2 validation infrastructure  
Purpose: define required external constraints before any strong LSC claim  

## 1. Rule

External vetoes are hard constraints.

If an LSC parameter region improves Gallium residuals but violates an external veto, that region is not viable.

## 2. Veto Summary

| Veto | Must Check | Would Weaken LSC | Would Falsify / Reject Region | Current Status |
|---|---|---|---|---|
| KATRIN | whether response implies beta-spectrum energy distortion | required response close to KATRIN-sensitive scale | required universal distortion excluded by KATRIN | unresolved |
| IceCube | whether anisotropy/tensor behavior conflicts with neutrino anisotropy constraints | qualitative analogy only | mapped tensor amplitude exceeds bounds | unresolved |
| SME / Lorentz-style bounds | whether fixed tensor implies Lorentz-violation-like coefficients | no mapping exists | implied coefficients exceed published limits | unresolved |
| solar neutrino consistency | whether scalar response conflicts with solar rates | solar inconsistency under same response | required parameters break solar constraints | unresolved |
| standard oscillation fits | whether survival/transition behavior conflicts with 3-flavor fits | tension under transfer | required behavior incompatible with global fits | unresolved |
| detector calibration literature | whether calibration/cross-section uncertainties explain signal | M1/M2/M4 match LSC | mundane explanation fully reproduces M6 | unresolved |

## 3. KATRIN Checklist

Must check:

- whether LSC trace response implies universal energy-scale distortion;
- whether `f0_a(E,t)` transfers to tritium beta-spectrum observables;
- whether response is detector-specific or universal;
- whether KATRIN constraints allow required amplitude.

Weakens LSC:

- required trace response is near a KATRIN-excluded scale.

Falsifies parameter region:

- same response required for Gallium would produce excluded KATRIN distortion.

Unresolved:

- no final frozen `f0_a` mapping exists.

## 4. IceCube Checklist

Must check:

- whether anisotropy tensor is detector-local, lab-local, or celestial-frame;
- whether any claimed celestial tensor implies constraints from IceCube anisotropy or Lorentz-violation searches;
- whether IceCube is only a detector-systematics analogy or a quantitative veto.

Weakens LSC:

- IceCube is cited qualitatively without a calculation.

Falsifies parameter region:

- mapped anisotropy amplitude exceeds relevant IceCube bounds.

Unresolved:

- no machine-readable tensor-bound mapping is yet integrated.

## 5. SME / Lorentz-Style Tensor Bounds

Must check:

- whether fixed background tensor language implies SME-like coefficients;
- whether the detector-response tensor is purely detector-local or physical-background-like;
- whether published bounds constrain the required amplitude.

Weakens LSC:

- tensor is physically interpreted but no SME mapping is provided.

Falsifies parameter region:

- required tensor amplitude conflicts with SME/Lorentz bounds.

Unresolved:

- physical status of tensor remains intentionally limited to detector-response phenomenology.

## 6. Solar Neutrino Consistency

Must check:

- whether scalar response affects solar Gallium interpretation;
- whether the response is source-experiment-specific or universal;
- whether solar-neutrino rates remain consistent.

Weakens LSC:

- scalar response improves source experiments but worsens solar consistency.

Falsifies parameter region:

- required response breaks solar-neutrino constraints under the same assumptions.

Unresolved:

- response transfer rules are not frozen.

## 7. Standard Oscillation Fits

Must check:

- compatibility with three-flavor oscillation results;
- sterile-neutrino benchmark comparison under identical data treatment;
- whether LSC introduces effective behavior already excluded by global fits.

Weakens LSC:

- fit requires parameters inconsistent with established oscillation data.

Falsifies parameter region:

- required residual structure cannot coexist with global oscillation constraints.

Unresolved:

- no full global-fit integration exists.

## 8. Detector Calibration Literature

Must check:

- source activity uncertainties;
- gallium cross-section uncertainty;
- extraction efficiency uncertainty;
- background subtraction uncertainty;
- detector response/counter efficiency.

Weakens LSC:

- calibration/systematics can explain trace response.

Falsifies LSC preference:

- M4 or M2 reproduces M6-level structures after penalties.

Unresolved:

- M4 implementation is Step 2/Step 3 work.

