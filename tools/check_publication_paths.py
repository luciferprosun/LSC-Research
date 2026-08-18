#!/usr/bin/env python3
"""Check Step 02 artifacts for machine-local filesystem paths."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lsc_kernel.io.publication_paths import scan_publication_paths  # noqa: E402


def changed_paths(base: str) -> tuple[Path, ...]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", base, "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return tuple(ROOT / path for path in sorted(set(tracked + untracked)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="313803a4e018709679d251f9494906f653a54135")
    args = parser.parse_args()
    findings = scan_publication_paths(changed_paths(args.base), root=ROOT)
    for finding in findings:
        print(f"{finding.path}:{finding.line}:{finding.pattern}")
    print(f"publication_path_findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
