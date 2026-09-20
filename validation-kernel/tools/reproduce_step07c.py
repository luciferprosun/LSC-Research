#!/usr/bin/env python3
"""Read-only reproduction of the frozen STEP 07C receipts."""

from __future__ import annotations

import json
from pathlib import Path

from lsc_kernel.lsc640.determination import verify_frozen_result
from lsc_kernel.lsc640.golden import verify_golden_vectors
from lsc_kernel.lsc640.prefit import run_prefit_audit


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    prefit = run_prefit_audit(root)
    golden = verify_golden_vectors(root)
    result = verify_frozen_result(root)
    receipt = {
        "status": "PASS",
        "model_sha256": prefit["model_sha256"],
        "prefit_freeze_sha256": prefit["prefit_freeze_sha256"],
        "golden_vectors": {"passed": golden["passed"], "failed": golden["failed"]},
        "determination_verdict": result["verdict"],
        "alpha_0_estimate_unconstrained_diagnostic": result["alpha_0_estimate_unconstrained_diagnostic"],
        "alpha_0_estimate_constrained": result["alpha_0_estimate_constrained"],
        "boundary_status": result["boundary_status"],
        "refit_performed": False,
        "BEST2_observed_data_accessed": False,
        "BEST2_prediction_generated": False,
    }
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
