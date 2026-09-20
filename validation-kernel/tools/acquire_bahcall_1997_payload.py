#!/usr/bin/env python3
"""Acquire and deterministically materialize the frozen Bahcall 1997 table.

The publication exports do not redistribute the author-hosted source table
because no explicit redistribution license was located.  This tool downloads
only when invoked explicitly, verifies the exact source bytes, and writes the
canonical payload only when its final SHA-256 matches the frozen model binding.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import urllib.request
from pathlib import Path


SOURCE_URL = "https://www.sns.ias.edu/~jnb/SNdata/Export/Galliumcross/galliumcrosstabs"
SOURCE_SHA256 = "bba57204fb909a846f8fd77034ef420755c10ffeeb07acb8adc1f043e921f92a"
PAYLOAD_SHA256 = "55dc0006cbb2bca205f03162521dbbc75ba68af223810b312113398528a49da5"
MAX_SOURCE_BYTES = 100_000
NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def acquire_source(source: Path | None) -> bytes:
    if source is not None:
        payload = source.read_bytes()
    else:
        request = urllib.request.Request(
            SOURCE_URL,
            headers={"User-Agent": "LSC-Validation-Kernel/0.6.0 deterministic-acquisition"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read(MAX_SOURCE_BYTES + 1)
    if len(payload) > MAX_SOURCE_BYTES:
        raise RuntimeError("source response exceeds the frozen acquisition limit")
    if sha256_bytes(payload) != SOURCE_SHA256:
        raise RuntimeError("author-hosted source SHA-256 does not match the frozen provenance record")
    return payload


def canonical_payload(source: bytes) -> bytes:
    text = source.decode("ascii")
    try:
        best_section = text.split("Best", 1)[1].split("-3 Sigma", 1)[0]
    except IndexError as exc:
        raise RuntimeError("source table sections are not recognizable") from exc
    rows: list[tuple[float, float]] = []
    for line in best_section.splitlines():
        values = NUMBER.findall(line)
        if len(values) not in {0, 2, 4, 6}:
            raise RuntimeError("unexpected numeric layout in source table")
        for offset in range(0, len(values), 2):
            rows.append((float(values[offset]), float(values[offset + 1])))
    rows.sort()
    if len(rows) != 58 or len({energy for energy, _ in rows}) != 58:
        raise RuntimeError("expected exactly 58 unique best-estimate knots")
    output = "energy_mev,cross_section_1e_minus_46_cm2\n"
    output += "".join(f"{energy:.3f},{value:.2f}\n" for energy, value in rows)
    encoded = output.encode("ascii")
    if sha256_bytes(encoded) != PAYLOAD_SHA256:
        raise RuntimeError("materialized payload does not match the frozen model hash")
    return encoded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="use an already acquired exact source file")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("external_physics/gallium_capture/bahcall_1997_best_estimate.csv"),
    )
    arguments = parser.parse_args()
    payload = canonical_payload(acquire_source(arguments.source))
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    if arguments.output.exists():
        if arguments.output.is_file() and sha256_bytes(arguments.output.read_bytes()) == PAYLOAD_SHA256:
            print(f"{PAYLOAD_SHA256}  {arguments.output} (already verified)")
            return 0
        raise FileExistsError(
            "refusing to overwrite an existing output that is not the frozen payload"
        )
    with arguments.output.open("xb") as handle:
        handle.write(payload)
    print(f"{PAYLOAD_SHA256}  {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
