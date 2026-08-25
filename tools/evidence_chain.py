#!/usr/bin/env python3
"""Create and verify the append-only LSC research evidence chain.

The manifest is calculated from the Git index, not from mutable working-tree
bytes. Stage the intended research changes before creating a record, then
commit the generated chain entry together with those changes.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHAIN_REL = "evidence-chain/chain.jsonl"
SCOPE_REL = "evidence-chain/scope.json"
SCHEMA_VERSION = "1.0.0"


class EvidenceError(RuntimeError):
    """A fail-closed evidence-chain validation error."""


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> bytes:
    result = subprocess.run(
        ("git", "-C", str(ROOT), *args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise EvidenceError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout


def load_scope() -> dict[str, Any]:
    path = ROOT / SCOPE_REL
    try:
        scope = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"cannot load {SCOPE_REL}: {exc}") from exc

    required_strings = (
        "schema_version",
        "network_id",
        "repository",
        "authority_role",
        "coverage",
        "recorded_by",
    )
    for key in required_strings:
        if not isinstance(scope.get(key), str) or not scope[key].strip():
            raise EvidenceError(f"scope field {key!r} must be a non-empty string")
    if scope["schema_version"] != SCHEMA_VERSION:
        raise EvidenceError(
            f"unsupported scope schema {scope['schema_version']!r}; expected {SCHEMA_VERSION!r}"
        )
    for key in ("include", "exclude", "required_paths"):
        value = scope.get(key)
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item for item in value
        ):
            raise EvidenceError(f"scope field {key!r} must be a list of strings")
    return scope


def selected(path: str, scope: dict[str, Any]) -> bool:
    if path == CHAIN_REL:
        return False
    included = any(fnmatch.fnmatchcase(path, pattern) for pattern in scope["include"])
    excluded = any(fnmatch.fnmatchcase(path, pattern) for pattern in scope["exclude"])
    return included and not excluded


def nul_paths(raw: bytes) -> list[str]:
    return [
        item.decode("utf-8", "strict")
        for item in raw.split(b"\0")
        if item
    ]


def ensure_staged_scope_is_stable(scope: dict[str, Any]) -> None:
    unstaged = nul_paths(git("diff", "--name-only", "-z", "--"))
    untracked = nul_paths(git("ls-files", "--others", "--exclude-standard", "-z"))
    offenders = sorted(
        path
        for path in (*unstaged, *untracked)
        if selected(path, scope)
    )
    if offenders:
        rendered = "\n  - ".join(offenders)
        raise EvidenceError(
            "scoped files must be staged before snapshotting:\n  - " + rendered
        )


def index_manifest(scope: dict[str, Any]) -> list[dict[str, Any]]:
    raw = git("ls-files", "--stage", "-z")
    entries: list[tuple[str, str, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            metadata, raw_path = item.split(b"\t", 1)
            mode, object_id, stage = metadata.decode("ascii").split()
            path = raw_path.decode("utf-8", "strict")
        except (ValueError, UnicodeDecodeError) as exc:
            raise EvidenceError("cannot parse Git index entry") from exc
        if stage != "0":
            raise EvidenceError(f"unmerged index entry in evidence scope: {path}")
        if selected(path, scope):
            entries.append((path, mode, object_id))

    entries.sort(key=lambda item: item[0])
    manifest: list[dict[str, Any]] = []
    for path, mode, object_id in entries:
        if mode == "160000":
            payload = object_id.encode("ascii")
            kind = "gitlink"
        else:
            payload = git("cat-file", "blob", object_id)
            kind = "symlink" if mode == "120000" else "file"
        manifest.append(
            {
                "bytes": len(payload),
                "git_mode": mode,
                "kind": kind,
                "path": path,
                "sha256": sha256_bytes(payload),
            }
        )

    present = {entry["path"] for entry in manifest}
    missing = [path for path in scope["required_paths"] if path not in present]
    if missing:
        raise EvidenceError(
            "required evidence-governance paths are absent from the staged scope: "
            + ", ".join(missing)
        )
    if not manifest:
        raise EvidenceError("evidence scope resolved to an empty manifest")
    return manifest


def load_chain(*, required: bool) -> list[dict[str, Any]]:
    path = ROOT / CHAIN_REL
    if not path.exists():
        if required:
            raise EvidenceError(f"missing {CHAIN_REL}")
        return []
    try:
        lines = path.read_bytes().splitlines(keepends=True)
    except OSError as exc:
        raise EvidenceError(f"cannot read {CHAIN_REL}: {exc}") from exc
    if not lines:
        if required:
            raise EvidenceError(f"empty {CHAIN_REL}")
        return []

    records: list[dict[str, Any]] = []
    for number, raw_line in enumerate(lines, start=1):
        if not raw_line.endswith(b"\n"):
            raise EvidenceError(f"chain line {number} has no terminating newline")
        payload = raw_line[:-1]
        try:
            record = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise EvidenceError(f"invalid JSON on chain line {number}: {exc}") from exc
        if not isinstance(record, dict):
            raise EvidenceError(f"chain line {number} is not a JSON object")
        if canonical_json(record) != payload:
            raise EvidenceError(f"chain line {number} is not canonical JSON")
        records.append(record)
    return records


def validate_records(records: list[dict[str, Any]]) -> None:
    previous_hash: str | None = None
    for sequence, record in enumerate(records, start=1):
        if record.get("schema_version") != SCHEMA_VERSION:
            raise EvidenceError(f"record {sequence}: unsupported schema version")
        if record.get("sequence") != sequence:
            raise EvidenceError(f"record {sequence}: non-contiguous sequence")
        if record.get("previous_record_sha256") != previous_hash:
            raise EvidenceError(f"record {sequence}: broken previous-record link")

        manifest = record.get("manifest")
        if not isinstance(manifest, list):
            raise EvidenceError(f"record {sequence}: manifest is not a list")
        paths = [entry.get("path") for entry in manifest if isinstance(entry, dict)]
        if len(paths) != len(manifest) or paths != sorted(paths) or len(paths) != len(set(paths)):
            raise EvidenceError(f"record {sequence}: manifest paths are invalid")
        expected_manifest_hash = sha256_bytes(canonical_json(manifest))
        if record.get("manifest_sha256") != expected_manifest_hash:
            raise EvidenceError(f"record {sequence}: manifest hash mismatch")

        unsigned = dict(record)
        claimed_hash = unsigned.pop("record_sha256", None)
        expected_record_hash = sha256_bytes(canonical_json(unsigned))
        if claimed_hash != expected_record_hash:
            raise EvidenceError(f"record {sequence}: record hash mismatch")
        previous_hash = claimed_hash


def current_scope_hash(manifest: list[dict[str, Any]]) -> str:
    for entry in manifest:
        if entry["path"] == SCOPE_REL:
            return str(entry["sha256"])
    raise EvidenceError(f"{SCOPE_REL} is not covered by the evidence manifest")


def verify(*, require_current: bool) -> dict[str, Any]:
    scope = load_scope()
    records = load_chain(required=True)
    validate_records(records)
    latest = records[-1]

    for key in ("network_id", "repository", "authority_role", "coverage"):
        if latest.get(key) != scope.get(key):
            raise EvidenceError(f"latest record and scope disagree on {key!r}")

    result: dict[str, Any] = {
        "chain_records": len(records),
        "current_manifest_verified": False,
        "latest_record_sha256": latest["record_sha256"],
        "repository": scope["repository"],
        "status": "valid",
    }
    if require_current:
        ensure_staged_scope_is_stable(scope)
        manifest = index_manifest(scope)
        if latest.get("manifest") != manifest:
            raise EvidenceError(
                "current staged scope differs from the latest evidence record; "
                "append a new snapshot"
            )
        if latest.get("scope_sha256") != current_scope_hash(manifest):
            raise EvidenceError("latest scope hash does not match the staged scope")
        result["current_manifest_verified"] = True
    return result


def snapshot(event: str, statement: str, recorded_by: str | None) -> dict[str, Any]:
    scope = load_scope()
    records = load_chain(required=False)
    if records:
        validate_records(records)
        latest = records[-1]
        for key in ("network_id", "repository"):
            if latest.get(key) != scope.get(key):
                raise EvidenceError(f"refusing to continue a chain with changed {key!r}")
        if event == "baseline":
            raise EvidenceError("baseline is allowed only for the first record")
    elif event != "baseline":
        raise EvidenceError("the first record must use event 'baseline'")

    statement = statement.strip()
    if not statement:
        raise EvidenceError("snapshot statement cannot be empty")
    actor = (recorded_by or scope["recorded_by"]).strip()
    if not actor:
        raise EvidenceError("recorded-by identity cannot be empty")

    ensure_staged_scope_is_stable(scope)
    manifest = index_manifest(scope)
    manifest_hash = sha256_bytes(canonical_json(manifest))
    parent_commit = git("rev-parse", "HEAD").decode("ascii").strip()
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    record: dict[str, Any] = {
        "authority_role": scope["authority_role"],
        "coverage": scope["coverage"],
        "created_at_utc": created_at,
        "event": event,
        "manifest": manifest,
        "manifest_sha256": manifest_hash,
        "network_id": scope["network_id"],
        "parent_commit": parent_commit,
        "previous_record_sha256": records[-1]["record_sha256"] if records else None,
        "recorded_by": actor,
        "repository": scope["repository"],
        "schema_version": SCHEMA_VERSION,
        "scope_sha256": current_scope_hash(manifest),
        "sequence": len(records) + 1,
        "statement": statement,
    }
    record["record_sha256"] = sha256_bytes(canonical_json(record))

    chain_path = ROOT / CHAIN_REL
    chain_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(chain_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(descriptor, canonical_json(record) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return {
        "manifest_files": len(manifest),
        "manifest_sha256": manifest_hash,
        "record_sha256": record["record_sha256"],
        "repository": scope["repository"],
        "sequence": record["sequence"],
        "status": "appended",
    }


def emit(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return
    print(
        f"{result['status']}: {result['repository']} "
        f"record={result.get('latest_record_sha256', result.get('record_sha256'))}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify_parser = subparsers.add_parser("verify", help="verify chain integrity")
    verify_parser.add_argument("--require-current", action="store_true")
    verify_parser.add_argument("--json", action="store_true")

    snapshot_parser = subparsers.add_parser("snapshot", help="append a staged snapshot")
    snapshot_parser.add_argument(
        "--event",
        required=True,
        choices=("baseline", "update", "checkpoint", "correction"),
    )
    snapshot_parser.add_argument("--statement", required=True)
    snapshot_parser.add_argument("--recorded-by")
    snapshot_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            emit(verify(require_current=args.require_current), args.json)
        else:
            emit(
                snapshot(args.event, args.statement, args.recorded_by),
                args.json,
            )
    except EvidenceError as exc:
        print(f"evidence-chain: ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
