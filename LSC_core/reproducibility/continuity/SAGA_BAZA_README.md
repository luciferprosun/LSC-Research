# Baza LSC do dalszego rozwoju

Ten folder zawiera wybraną bazę teorii LSC do dalszych obliczeń i przygotowania pod eksperyment typu BEST-2.

## Decyzja

Najbardziej zaawansowanym i najbezpieczniejszym punktem startowym jest:

```text
LSC 6.2.0: A Phenomenological Framework for Neutrino Propagation and Detector-Frame Tensor Anisotropy
```

Powody:

- Jest najnowszą opublikowaną wersją w linii LSC.
- Ma publiczny rekord Zenodo: https://doi.org/10.5281/zenodo.19878587
- Ma GitHub release: https://github.com/luciferprosun/LSC-6.0/releases/tag/v6.2.0-preprint
- Rozwija LSC 6.0 zamiast zaczynać osobną, niespójną gałąź.
- Wprowadza jawny tensor anizotropii w układzie detektora `D_ij`.
- Oddziela energię propagacyjną `E_true` od energii rekonstruowanej `E_rec`.
- Daje naturalne testy pod BEST/GALLEX/SAGE, KATRIN, IceCube i dane standardowych oscylacji.

## Struktura

```text
model_lsc_6_2_0/
  LSC_6_2_0_main.tex
  LSC_6_2_0_main.md
  LSC_6_2_0_preprint.pdf
  LSC_6_2_0_BASE_THEORY_FOR_BEST2.md
  README_original_release.md
  CHANGELOG_LSC_6_2_0.md
  VERSION_HISTORY.md
  zenodo_6_2_0.json

przydatne_dodatki/
  lsc55_math_and_tests/
  lsc60_simulation/
  prism_exploratory/
  zenodo_github_checks/
```

## Status starszych wersji

- LSC 4.2: historyczny początek formalizmu.
- LSC 5.0/5.5: przydatna matematyka i testy tensorowe, ale mniej czyste publicznie.
- LSC 6.0: czysta wersja fenomenologiczna.
- LSC v1.2.0: aktualizacja obliczeniowa i reprodukowalność.
- LSC 6.2.0: aktualna baza teoretyczna.
- LSC 6.1/prism: eksploracyjne notatki, nie baza główna.

