# LSC to IceCube Mapping Assessment

## Verdict

**MAPPING_NOT_JUSTIFIED**

The IceCube release is a valid external sterile-neutrino constraint object, but frozen LSC does not define a map into its parameter or observable space.

## IceCube object

The retained DeepCore release corresponds to arXiv:2407.01314. The analysis uses atmospheric neutrino energy and baseline/zenith dependence, matter effects, flavor mixing, and profiled detector/flux/systematic parameters. Its reported sterile space includes absolute mixing elements such as |U_mu4| squared and |U_tau4| squared under a stated mass-splitting regime.

The Step 04 integrity loader verifies the release index and the selected numerical contours/maps. That establishes data integrity only.

## Missing map

Frozen LSC provides no equations connecting its response functions and tensor to:

- a unitary 3+1 mixing matrix;
- flavor-transition probabilities in matter;
- atmospheric energy/zenith distributions;
- IceCube nuisance parameters or confidence construction.

A directional or environmental response tensor is not automatically equivalent to sterile flavor mixing. Energy dependence, baselines, and Earth matter propagation prevent an identity mapping.

## Authorization boundary

Any future relationship would be a model-dependent extension and must be separately specified and preregistered. It must include equations, units, domain, statistical interpretation, provenance, and limitations. Until then the status remains EXTERNAL_VETO_BLOCKED_MAPPING_MISSING.

No IceCube veto, likelihood multiplication, or numerical LSC evaluation was performed.

Sources: IceCube DeepCore paper arXiv:2407.01314 and the archived release objects listed in 07_ICECUBE/ICECUBE_FILE_INTEGRITY.csv.
