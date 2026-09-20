# LSC to KATRIN Mapping Assessment

## Verdict

**MAPPING_NOT_JUSTIFIED**

The official KATRIN release is authoritative and machine-readable, but it is not an LSC likelihood until an explicit physical mapping exists.

## Recovered KATRIN object

The archived record is the KATRIN sterile-neutrino search dataset at 10.5281/zenodo.19369714. Its main result is a 50 by 50 absolute chi-square grid over mnu2sterile and sin2thetaee. The grid is finite and its local minimum, axes, dimensions, and release metadata pass the existing loader. The release documents capped/interpolated regions, which must retain their native meaning.

KATRIN measures beta-spectrum distortions under a sterile-neutrino mass/mixing model. Its axes represent a sterile mass-squared parameter and electron-flavor mixing. The native grid can therefore constrain a compatible sterile 3+1 baseline such as M3 when all its assumptions are satisfied.

## LSC side

Frozen LSC E1-E12 describe detector-response objects through lambda coefficients, response functions, scalar/trace terms, and a directional tensor. The frozen specification contains no equation that maps those objects to:

- a sterile mass eigenstate;
- sin-squared electron mixing;
- beta-spectrum kink amplitude;
- the KATRIN fit nuisance space.

The relationship is therefore neither one-to-one nor a demonstrated many-to-one map. Any proposed translation would be model-dependent new theory, not a deterministic derivation from the frozen object.

## Statistical meaning

Multiplying or looking up the KATRIN chi-square grid without a physical mapping would change the meaning of its likelihood. No external veto is authorized. A future mapping must freeze:

- explicit equations;
- units and parameter domain;
- whether the map is unique or model-dependent;
- preservation of KATRIN nuisance and confidence construction;
- provenance and limitations.

No KATRIN veto or LSC prediction was executed.

Sources: KATRIN Zenodo record 10.5281/zenodo.19369714 and the archived release README/grid.
