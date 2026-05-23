# LSC Version Selection Report

Date: 2026-04-30

## Checked Sources

Local computer:

- `/home/l/LSC-6.0`
- `/home/l/Desktop/LSC_ARXIV_WORKSPACE`
- `/home/l/Desktop/LLM/zenodo`
- `/home/l/Desktop/prace dark neutrino`
- `/home/l/LSC-research-data`
- `/home/l/the saga continue`

GitHub:

- `luciferprosun/LSC-6.0`
- `luciferprosun/LSC_MDLH_PRO`
- `luciferprosun/LSC-the-saga-continue`
- older public LSC/neutrino repos

Zenodo:

- `19780616` - LSC 6.0
- `19843361` - LSC Framework v1.2.0
- `19851006` - MDLH
- `19878587` - LSC 6.2.0

## Public Version Order

1. LSC 4.2
2. LSC 5.0
3. LSC 5.5
4. LSC 6.0
5. LSC Framework v1.2.0
6. LSC 6.2.0 preprint

## GitHub Check

`luciferprosun/LSC-6.0` release order:

- `v1.0.0` - LSC 6.0
- `v1.2.0` - computational/reproducibility update
- `v6.2.0-preprint` - latest release

Current local `LSC-6.0` HEAD:

```text
70c92d3 Add LSC 6.2.0 preprint continuation
```

## Zenodo Check

LSC 6.2.0:

- title: `LSC 6.2.0: A Phenomenological Framework for Neutrino Propagation and Detector-Frame Tensor Anisotropy`
- version: `6.2.0-preprint`
- DOI: `10.5281/zenodo.19878587`
- created: `2026-04-29`

LSC v1.2.0:

- title: `LSC Framework v1.2.0: Computational Extension and Reproducibility Update`
- DOI: `10.5281/zenodo.19843361`
- created: `2026-04-28`

LSC 6.0:

- title: `LSC 6.0: A Phenomenological Framework for Neutrino Propagation and Anisotropic Detection`
- DOI: `10.5281/zenodo.19780616`
- created: `2026-04-26`

MDLH:

- separate AI-safety / documentation case-study track
- not the main physical model
- DOI: `10.5281/zenodo.19851006`

## Conclusion

The most advanced model to develop is **LSC 6.2.0**.

No local file or public record was found that supersedes it. The `LSC61/prism` materials are exploratory and are not better candidates for a clean research base. The LSC 5.5 files are still useful because they contain longer tensor math and early BEST/GALLEX toy tests, so they were copied into `przydatne_dodatki/`.

## BEST-2 Recommendation

Use LSC 6.2.0 as the core theory and build the next code/data layer around:

- volume-integrated BEST geometry,
- inner/outer zone response,
- source finite-size correction,
- gallium source-line library,
- cross-section uncertainty model,
- nuisance parameters for detector anisotropy,
- external consistency checks with KATRIN and IceCube.

