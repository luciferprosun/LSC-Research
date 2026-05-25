# LSC M4 Detector/Systematics Baseline

Status: Step 2 validation infrastructure  
Role: required primary competitor to M6  

## 1. Core Rule

M4 is not a nuisance footnote. M4 is a primary competitor to M6.

If M4 reproduces M6-level structures, LSC is not distinguishable.

## 2. Purpose

M4 tests whether ordinary detector, source, calibration, extraction, background or metadata effects can reproduce structures that LSC would otherwise describe as trace or traceless response.

M4 must be evaluated before any LSC preference claim.

## 3. M4 Components

| Component | Mechanism | LSC Structure It Can Mimic | Required Separation Test |
|---|---|---|---|
| Calibration drift | time-dependent calibration shift | trace response or false time trend | calibration logs and stability runs |
| Source normalization uncertainty | wrong source activity estimate | global deficit / trace term | independent source activity calibration |
| Cross-section normalization | gallium capture uncertainty | trace term | nuclear cross-section review and uncertainty propagation |
| Extraction efficiency asymmetry | inner/outer or run-dependent extraction differences | zone structure / false anisotropy | spiked recovery tests and zone-specific efficiency model |
| Detector geometry asymmetry | hardware, dead volumes, guide tubes, tank structure | lab-frame anisotropy | geometry model and rotation/source-position tests |
| Background subtraction uncertainty | imperfect low-rate background model | trace or time-dependent residual | background-only runs and timestamped event logs |
| Environmental drift | temperature, radon, pressure, electronics | false time/sidereal trend | environmental sensor correlation analysis |
| Covariance incompleteness | missing correlations | false significance | full covariance or conservative correlated-error envelope |
| Timing/orientation artifacts | lab-frame orientation confused with celestial frame | false traceless tensor | orientation/timestamp metadata and sidereal-phase analysis |

## 4. M4 Minimum Implementation Requirements

M4 must include:

- source activity nuisance;
- cross-section nuisance;
- zone-specific extraction efficiency nuisance;
- background subtraction nuisance;
- detector geometry asymmetry nuisance;
- environmental drift nuisance if time information exists;
- covariance-correlation nuisance;
- lab-frame orientation artifact term if anisotropy is tested.

These are not new LSC physics. They are detector/systematics competitors.

## 5. M4 vs M6 Decision Logic

| Result | Interpretation |
|---|---|
| M4 matches or exceeds M6 after penalties | LSC not distinguishable |
| M6 beats M4 but fails LOO | LSC unresolved / overfit risk |
| M6 beats M4 and passes LOO but lacks covariance | exploratory support only |
| M6 beats M4, passes LOO, transfers across experiments and survives vetoes | candidate validation support |
| M4 explains trace while M6 explains no additional structure | trace-only LSC not supported |

## 6. Required M4 Outputs

Every M4 run must report:

- included systematics;
- excluded systematics and why;
- nuisance parameter count;
- covariance assumptions;
- fit quality;
- penalty-adjusted score;
- residual structure;
- comparison to M5 and M6;
- failure modes.

## 7. DeepSeek Detector-Attack Consolidation

DeepSeek-style detector audit conclusions are treated as mandatory constraints:

- cross-section normalization errors can mimic trace response;
- source activity miscalibration can mimic global deficit;
- extraction efficiency asymmetry can mimic zone structure;
- background/environment drift can mimic time or sidereal structure;
- missing orientation and timestamps make celestial anisotropy non-identifiable;
- incomplete covariance can inflate significance.

## 8. M4 Failure To Implement

If M4 is not implemented, then:

- M6 cannot be claimed preferred;
- directional/traceless claims remain unresolved;
- any fit result is exploratory only.

