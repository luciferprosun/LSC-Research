# Reproduce LSC 6.5.0 RC1

Requirements are frozen in `requirements-step07e.lock`; the recorded environment uses Python 3.12.3, NumPy 2.5.2, SciPy 1.18.0, and pytest 9.1.1.

From the repository root:

```bash
make reproduce-650
```

From the release-candidate root:

```bash
PYTHONPATH=src python3 tools/reproduce_lsc650.py
sha256sum -c SHA256SUMS.txt
```

The reproduction is read-only. It verifies all model-identity components, reconstructs the exact objective under the frozen protocol, compares the result with the frozen bundle, runs the independent golden/reference checks, and validates RC hashes. It never invokes the write-once result function.

No network download, observed BEST-2 data, or unversioned input is permitted.
