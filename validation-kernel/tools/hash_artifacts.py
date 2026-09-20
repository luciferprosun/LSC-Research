#!/usr/bin/env python3
"""Hash an explicit allow-list of important evidence artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from recovery_lib import sha256_file, write_csv


OUTPUT_COLUMNS = ["artifact_id", "source_path", "importance", "reason", "size_bytes", "sha256"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--kernel-root", required=True, type=Path)
    arguments = parser.parse_args()

    with arguments.input_csv.open(encoding="utf-8", newline="") as handle:
        inputs = list(csv.DictReader(handle))
    required = {"artifact_id", "source_path", "importance", "reason"}
    if not inputs or not required.issubset(inputs[0]):
        raise ValueError(f"input must contain {sorted(required)}")

    rows: list[dict[str, object]] = []
    for item in sorted(inputs, key=lambda row: row["artifact_id"]):
        source_path = item["source_path"].strip()
        if source_path.startswith("kernel:"):
            resolved = arguments.kernel_root / source_path.removeprefix("kernel:")
        else:
            resolved = arguments.archive_root / source_path
        if not resolved.is_file():
            raise FileNotFoundError(f"{item['artifact_id']}: {source_path}")
        rows.append(
            {
                **item,
                "size_bytes": resolved.stat().st_size,
                "sha256": sha256_file(resolved),
            }
        )
    write_csv(arguments.output_csv, rows, OUTPUT_COLUMNS)
    print(json.dumps({"artifacts_hashed": len(rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
