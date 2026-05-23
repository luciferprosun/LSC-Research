#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "[1/3] Baseline smoke run"
python3 scripts/framework/run_baselines.py

echo "[2/3] Unit tests"
if python3 -c "import pytest" >/dev/null 2>&1; then
  python3 -m pytest -q
else
  echo "pytest not installed; running direct fallback for tests/test_baselines.py"
  python3 - << 'PY'
import sys
from pathlib import Path

repo_root = Path.cwd()
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import tests.test_baselines as t

t.test_null_model_output_size()
t.test_sterile_model_output_size()
t.test_chi2_nonnegative()
t.test_leave_one_out_null()
print("Fallback tests passed.")
PY
fi

echo "[3/3] Basic structure checks"
for path in data/raw loaders likelihood baselines notebooks tests docs scripts/framework; do
  [[ -d "$path" ]] || { echo "Missing directory: $path"; exit 1; }
done

echo "All checks passed."
