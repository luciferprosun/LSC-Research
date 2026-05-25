#!/usr/bin/env python3
"""Validate and update Zenodo draft 20038802 metadata.

The script deliberately does not publish the record. It only updates metadata
after checking that the draft appears to belong to the LSC version chain.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import urllib.error
import urllib.request


API = "https://zenodo.org/api"
DRAFT_ID = 20038802
LATEST_LSC_RECORD_ID = 20037838
EXPECTED_CONCEPT_DOI = "10.5281/zenodo.19780615"
METADATA_FILE = "zenodo_6_3_0_metadata.json"
TOKEN_FILE = os.path.expanduser("~/.config/zenodo/token")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def request_json(method: str, url: str, token: str | None, data: dict | None = None) -> dict:
    body = None
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"{method} {url} failed with HTTP {exc.code}: {detail}")
    except urllib.error.URLError as exc:
        fail(f"{method} {url} failed: {exc}")
    except socket.timeout as exc:
        fail(f"{method} {url} timed out: {exc}")


def main() -> None:
    token = os.environ.get("ZENODO_TOKEN")
    if not token and os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as handle:
            token = handle.read().strip()
    if not token:
        fail(
            "Set ZENODO_TOKEN or create ~/.config/zenodo/token. "
            "Required scope: deposit:write."
        )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_path = os.path.join(script_dir, METADATA_FILE)
    with open(metadata_path, "r", encoding="utf-8") as handle:
        update_payload = json.load(handle)

    latest = request_json("GET", f"{API}/records/{LATEST_LSC_RECORD_ID}", None)
    conceptdoi = latest.get("conceptdoi")
    if conceptdoi != EXPECTED_CONCEPT_DOI:
        fail(f"Latest LSC record concept DOI mismatch: {conceptdoi!r}")

    draft = request_json("GET", f"{API}/deposit/depositions/{DRAFT_ID}", token)
    if draft.get("submitted") is True:
        fail(f"Deposition {DRAFT_ID} is already published; refusing to edit.")

    links = draft.get("links", {})
    metadata = draft.get("metadata", {})
    draft_conceptdoi = draft.get("conceptdoi") or metadata.get("conceptdoi")
    related = metadata.get("related_identifiers", [])
    related_ids = {item.get("identifier") for item in related if isinstance(item, dict)}

    lineage_signals = [
        draft_conceptdoi == EXPECTED_CONCEPT_DOI,
        str(LATEST_LSC_RECORD_ID) in json.dumps(links),
        "10.5281/zenodo.20037838" in related_ids,
        "10.5281/zenodo.19878587" in related_ids,
    ]
    if not any(lineage_signals):
        fail(
            "Draft does not expose an LSC version-chain signal. "
            "It may be a standalone New upload; refusing to write metadata."
        )

    response = request_json(
        "PUT",
        f"{API}/deposit/depositions/{DRAFT_ID}",
        token,
        update_payload,
    )

    print("Updated Zenodo draft metadata.")
    print(json.dumps({
        "id": response.get("id"),
        "state": response.get("state"),
        "submitted": response.get("submitted"),
        "title": response.get("metadata", {}).get("title"),
        "version": response.get("metadata", {}).get("version"),
        "links": response.get("links", {}),
    }, indent=2, ensure_ascii=False))
    print("Not published. Review in Zenodo UI before running any publish action.")


if __name__ == "__main__":
    main()
