#!/usr/bin/env python3
"""Scan every reachable commit of every Git repository in the source archive."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from recovery_lib import TEXT_SUFFIXES, git_output, normalized_excerpt, safe_relative, stable_artifact_id, write_csv, write_json
from scan_repository import first_matching_excerpt, matched_terms


MAX_TEXT_BLOB_BYTES = 20 * 1024 * 1024


def discover_repositories(source: Path) -> list[Path]:
    return sorted(path.parent for path in source.rglob(".git") if path.is_dir())


def sanitize_remote(url: str) -> str:
    value = url.strip()
    if not value:
        return value
    if "://" not in value:
        return value
    parsed = urlsplit(value)
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    return urlunsplit((parsed.scheme, host, parsed.path, parsed.query, ""))


def commit_metadata(repo: Path, commit: str) -> dict[str, str]:
    raw = str(git_output(repo, "show", "-s", "--format=%H%x1f%P%x1f%cI%x1f%an%x1f%s", commit)).rstrip("\n")
    fields = raw.split("\x1f", 4)
    return {
        "commit": fields[0],
        "parents": fields[1],
        "date": fields[2],
        "author": fields[3],
        "subject": fields[4] if len(fields) > 4 else "",
    }


def tree_entries(repo: Path, commit: str) -> list[tuple[str, str, str]]:
    raw = git_output(repo, "ls-tree", "-rz", "--full-tree", commit, binary=True)
    assert isinstance(raw, bytes)
    entries: list[tuple[str, str, str]] = []
    for item in raw.split(b"\x00"):
        if not item:
            continue
        header, path = item.split(b"\t", 1)
        mode, kind, object_id = header.decode("ascii").split(" ")
        if kind == "blob":
            entries.append((object_id, path.decode("utf-8", errors="replace"), mode))
    return entries


def refs_containing(repo: Path, commit: str) -> tuple[str, str]:
    branches = str(git_output(repo, "for-each-ref", "--contains", commit, "--format=%(refname)", "refs/heads", "refs/remotes"))
    tags = str(git_output(repo, "tag", "--contains", commit))
    return ";".join(sorted(line for line in branches.splitlines() if line)), ";".join(sorted(line for line in tags.splitlines() if line))


def deleted_files(repo: Path, repo_label: str) -> list[dict[str, str]]:
    raw = str(
        git_output(
            repo,
            "log",
            "--all",
            "--diff-filter=D",
            "--format=@@@%H%x1f%P%x1f%cI%x1f%an",
            "--name-only",
        )
    )
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in raw.splitlines():
        if line.startswith("@@@"):
            commit, parents, date, author = line[3:].split("\x1f", 3)
            current = {"commit": commit, "parents": parents, "date": date, "author": author}
        elif line.strip() and current is not None:
            rows.append(
                {
                    "repository": repo_label,
                    "deleted_path": line.strip(),
                    **current,
                    "path_keyword_matches": ";".join(matched_terms(line.strip())),
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args()
    source = arguments.source.resolve()
    output = arguments.output_dir.resolve()

    repositories = discover_repositories(source)
    summary_rows: list[dict[str, object]] = []
    candidates: dict[tuple[str, str, str], dict[str, object]] = {}
    deleted: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    total_commits = 0
    total_branches = 0
    total_tags = 0
    total_tree_entries = 0
    total_unique_blobs = 0
    total_text_blobs = 0

    for repo in repositories:
        repo_label = safe_relative(repo, source)
        role = "primary_lsc_history" if repo.name == "LSC-Research" else "external_dependency_history"
        try:
            commits = [line for line in str(git_output(repo, "rev-list", "--all", "--reverse", "--topo-order")).splitlines() if line]
            refs = [line for line in str(git_output(repo, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes")).splitlines() if line]
            tags = [line for line in str(git_output(repo, "tag", "--list")).splitlines() if line]
            head = str(git_output(repo, "rev-parse", "HEAD")).strip()
            branch = str(git_output(repo, "branch", "--show-current")).strip()
            status = str(git_output(repo, "status", "--short")).strip()
            remote_lines = str(git_output(repo, "remote", "-v")).splitlines()
            remotes = sorted({sanitize_remote(line.split()[1]) for line in remote_lines if len(line.split()) >= 2})
        except (subprocess.CalledProcessError, OSError) as exc:
            errors.append({"repository": repo_label, "stage": "repository_metadata", "error": f"{type(exc).__name__}: {exc}"})
            continue

        total_commits += len(commits)
        total_branches += len(refs)
        total_tags += len(tags)
        blob_cache: dict[str, tuple[list[str], str, str]] = {}
        ref_cache: dict[str, tuple[str, str]] = {}
        repo_tree_entries = 0
        repo_text_blobs = 0

        for commit in commits:
            try:
                metadata = commit_metadata(repo, commit)
                entries = tree_entries(repo, commit)
            except (subprocess.CalledProcessError, OSError, ValueError) as exc:
                errors.append({"repository": repo_label, "stage": f"commit:{commit}", "error": f"{type(exc).__name__}: {exc}"})
                continue
            repo_tree_entries += len(entries)
            total_tree_entries += len(entries)
            for blob, path, mode in entries:
                suffix = Path(path).suffix.lower()
                path_hits = matched_terms(path)
                if blob not in blob_cache:
                    blob_hits: list[str] = []
                    excerpt = ""
                    scan_status = "metadata_only"
                    try:
                        size = int(str(git_output(repo, "cat-file", "-s", blob)).strip())
                        if suffix in TEXT_SUFFIXES or suffix == ".ipynb":
                            if size <= MAX_TEXT_BLOB_BYTES:
                                raw = git_output(repo, "cat-file", "blob", blob, binary=True)
                                assert isinstance(raw, bytes)
                                if b"\x00" not in raw[:8192]:
                                    text = raw.decode("utf-8", errors="replace")
                                    blob_hits = matched_terms(text)
                                    excerpt = first_matching_excerpt(text, blob_hits)
                                    scan_status = "text_scanned"
                                    repo_text_blobs += 1
                                    total_text_blobs += 1
                                else:
                                    scan_status = "binary_signature"
                            else:
                                scan_status = "text_size_limit"
                    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
                        scan_status = f"scan_error:{type(exc).__name__}"
                    blob_cache[blob] = (blob_hits, excerpt, scan_status)
                    total_unique_blobs += 1
                blob_hits, excerpt, scan_status = blob_cache[blob]
                terms = sorted(set(path_hits) | set(blob_hits))
                if not terms:
                    continue
                key = (repo_label, path, blob)
                if key not in candidates:
                    candidates[key] = {
                        "artifact_id": stable_artifact_id(repo_label, path, blob, prefix="git"),
                        "repository": repo_label,
                        "repository_role": role,
                        "file_path": path,
                        "git_blob_sha1": blob,
                        "file_mode": mode,
                        "first_seen_commit": metadata["commit"],
                        "first_seen_parent": metadata["parents"],
                        "first_seen_date": metadata["date"],
                        "first_seen_author": metadata["author"],
                        "first_seen_subject": metadata["subject"],
                        "last_seen_commit": metadata["commit"],
                        "commit_occurrences": 1,
                        "keyword_matches": ";".join(terms),
                        "scan_status": scan_status,
                        "diff_context": normalized_excerpt(excerpt),
                        "branches_containing_first": "",
                        "tags_containing_first": "",
                    }
                else:
                    row = candidates[key]
                    row["last_seen_commit"] = metadata["commit"]
                    row["commit_occurrences"] = int(row["commit_occurrences"]) + 1

        for row in candidates.values():
            if row["repository"] != repo_label:
                continue
            first_commit = str(row["first_seen_commit"])
            if first_commit not in ref_cache:
                ref_cache[first_commit] = refs_containing(repo, first_commit)
            row["branches_containing_first"], row["tags_containing_first"] = ref_cache[first_commit]

        deleted.extend(deleted_files(repo, repo_label))
        summary_rows.append(
            {
                "repository": repo_label,
                "role": role,
                "head": head,
                "branch": branch,
                "worktree_clean": "YES" if not status else "NO",
                "commits_scanned": len(commits),
                "branch_refs_scanned": len(refs),
                "tags_scanned": len(tags),
                "tree_entries_scanned": repo_tree_entries,
                "unique_blobs_seen": len(blob_cache),
                "text_blobs_scanned": repo_text_blobs,
                "remote_urls": ";".join(remotes),
            }
        )

    candidate_rows = sorted(candidates.values(), key=lambda row: (str(row["repository"]), str(row["file_path"]), str(row["git_blob_sha1"])))
    deleted.sort(key=lambda row: (row["repository"], row["commit"], row["deleted_path"]))
    summary_rows.sort(key=lambda row: str(row["repository"]))
    errors.sort(key=lambda row: (row["repository"], row["stage"]))

    write_csv(
        output / "GIT_REPOSITORY_SUMMARY.csv",
        summary_rows,
        [
            "repository",
            "role",
            "head",
            "branch",
            "worktree_clean",
            "commits_scanned",
            "branch_refs_scanned",
            "tags_scanned",
            "tree_entries_scanned",
            "unique_blobs_seen",
            "text_blobs_scanned",
            "remote_urls",
        ],
    )
    write_csv(
        output / "GIT_HISTORY_CANDIDATES.csv",
        candidate_rows,
        [
            "artifact_id",
            "repository",
            "repository_role",
            "file_path",
            "git_blob_sha1",
            "file_mode",
            "first_seen_commit",
            "first_seen_parent",
            "first_seen_date",
            "first_seen_author",
            "first_seen_subject",
            "last_seen_commit",
            "commit_occurrences",
            "keyword_matches",
            "scan_status",
            "diff_context",
            "branches_containing_first",
            "tags_containing_first",
        ],
    )
    write_csv(
        output / "GIT_DELETED_FILES.csv",
        deleted,
        ["repository", "deleted_path", "commit", "parents", "date", "author", "path_keyword_matches"],
    )
    write_csv(output / "GIT_SCAN_ERRORS.csv", errors, ["repository", "stage", "error"])
    summary = {
        "branch_refs_scanned": total_branches,
        "candidate_blob_versions_found": len(candidate_rows),
        "commits_scanned": total_commits,
        "deleted_file_events": len(deleted),
        "errors": len(errors),
        "git_repositories_scanned": len(summary_rows),
        "tags_scanned": total_tags,
        "text_blobs_scanned": total_text_blobs,
        "tree_entries_scanned": total_tree_entries,
        "unique_blobs_seen_across_repositories": total_unique_blobs,
    }
    write_json(output / "GIT_HISTORY_SCAN_SUMMARY.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
