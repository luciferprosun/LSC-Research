# Neutrino Oscillations and Primordial Black Holes

Full documentation archive for LSC versions and earlier related theory notes:

https://www.facebook.com/ProximaCentauri333

## Kompilacja dokumentu
1. Upewnij się, że masz zainstalowany system LaTeX (np. TeX Live) oraz biblatex z biberem.
2. W katalogu głównym uruchom:
```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Python example

Install scientific dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the example:

```bash
python3 src/main_example.py
```

The script writes plots under `plots/`.
