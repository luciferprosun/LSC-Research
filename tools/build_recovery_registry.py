#!/usr/bin/env python3
"""Build the adjudicated frozen provenance registry deterministically."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from recovery_lib import build_registry, duplicate_hash_groups


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-csv", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--kernel-root", required=True, type=Path)
    arguments = parser.parse_args()

    rows = build_registry(
        arguments.source_csv,
        arguments.output_csv,
        arguments.archive_root,
        arguments.kernel_root,
    )
    summary = {
        "classification_counts": dict(sorted(Counter(row["classification"] for row in rows).items())),
        "duplicate_hash_groups": duplicate_hash_groups(rows),
        "registry_rows": len(rows),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
