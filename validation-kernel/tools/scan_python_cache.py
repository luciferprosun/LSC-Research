#!/usr/bin/env python3
"""Inventory Python bytecode caches without importing or unmarshalling them."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from recovery_lib import safe_relative, sha256_file, stable_artifact_id, write_csv, write_json
from scan_repository import matched_terms


PRINTABLE = re.compile(rb"[\x20-\x7e]{4,}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args()
    source = arguments.source.resolve()
    output = arguments.output_dir.resolve()

    rows: list[dict[str, object]] = []
    for path in sorted(source.rglob("*.pyc")):
        relative = safe_relative(path, source)
        raw = path.read_bytes()
        strings = "\n".join(match.group().decode("ascii", errors="replace") for match in PRINTABLE.finditer(raw))
        terms = sorted(set(matched_terms(relative)) | set(matched_terms(strings)))
        digest = sha256_file(path)
        rows.append(
            {
                "artifact_id": stable_artifact_id(relative, digest, prefix="pyc"),
                "source_path": relative,
                "size_bytes": len(raw),
                "sha256": digest,
                "header_hex": raw[:16].hex(),
                "printable_strings_scanned": "YES",
                "marshal_or_import_performed": "NO",
                "keyword_matches": ";".join(terms),
            }
        )
    write_csv(
        output / "PYTHON_CACHE_SCAN.csv",
        rows,
        [
            "artifact_id",
            "source_path",
            "size_bytes",
            "sha256",
            "header_hex",
            "printable_strings_scanned",
            "marshal_or_import_performed",
            "keyword_matches",
        ],
    )
    summary = {
        "cache_artifacts_scanned": len(rows),
        "cache_candidates_found": sum(1 for row in rows if row["keyword_matches"]),
        "code_execution_or_unmarshal_performed": "NO",
    }
    write_json(output / "PYTHON_CACHE_SCAN_SUMMARY.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
