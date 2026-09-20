# M4 Hierarchical Adjudication

## Verdict

**SPECIFICATION_INCOMPLETE**

An authentic high-level M4 detector-systematics schema exists, but no canonical executable hierarchical probability model was recovered.

## Label disambiguation

Historical M4 names a detector/systematics benchmark. STEP 03 provides explicit aliases for experiment normalization, detector systematic, and a proposed hierarchical experiment baseline. These related labels must not be collapsed into a single recovered canonical hierarchy.

The historical implementation schema contains placeholders for systematic components. It does not uniquely define:

- hierarchy levels;
- sampling distributions;
- priors or hyperpriors;
- shared variance;
- experiment and isotope random effects;
- parameter bounds;
- fitting policy or identifiability constraints.

Consequently, implementing a convenient hierarchy now would create a new baseline, not recover canonical M4. The existing fitting gate must keep M_HIERARCHICAL_EXPERIMENT disabled until a source-defined specification is found or a distinctly named future baseline is preregistered.

No new hierarchical model was designed or fit in STEP 05.
