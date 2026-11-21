#!/usr/bin/env python3
"""Verify one PDF archive whose README lists local files and SHA-256 hashes."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import file_digest
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def inventory_rows(archive):
    rows = defaultdict(list)
    for row in (archive / "README.md").read_text(encoding="utf-8-sig").splitlines():
        if not row.lstrip().startswith("|"):
            continue
        for target in re.findall(r"\]\(([^)]+?\.pdf)\)", row, re.IGNORECASE):
            if not urlsplit(target).scheme:
                rows[unquote(target.removeprefix("./"))].append(row)
    return rows


def check_archive(archive, page_checks):
    rows = inventory_rows(archive)
    hashes = {}
    for path in sorted(archive.rglob("*.pdf")):
        with path.open("rb") as stream:
            hashes[path.relative_to(archive).as_posix()] = file_digest(stream, "sha256").hexdigest()
    counts = Counter(hashes.values())
    errors = {
        "missing_or_repeated_rows": [name for name in hashes if len(rows[name]) != 1],
        "hash_not_in_matching_row": [
            name for name, digest in hashes.items()
            if not any(re.search(rf"\b{digest}\b", row, re.IGNORECASE) for row in rows[name])
        ],
        "links_without_file": sorted(rows.keys() - hashes.keys()),
        "duplicate_hash_count": sum(count - 1 for count in counts.values()),
        "page_count_errors": [],
    }
    pages = {}
    if page_checks:
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError

        for name, expected in page_checks:
            if name not in hashes:
                errors["page_count_errors"].append({"path": name, "error": "file missing"})
                continue
            try:
                actual = len(PdfReader(archive / name).pages)
            except (OSError, ValueError, PdfReadError) as error:
                errors["page_count_errors"].append({"path": name, "error": str(error)})
                continue
            pages[name] = {"pages": actual, "sha256": hashes[name]}
            if actual != expected:
                errors["page_count_errors"].append({
                    "path": name, "expected": expected, "actual": actual,
                })
    return {
        "ok": not any(errors.values()),
        "at": datetime.now(timezone.utc).isoformat(),
        "scope": "PDF byte hashes, README rows, and requested page counts.",
        "files": len(hashes),
        "unique_hashes": len(counts),
        "checked_page_counts": pages,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--page-count", nargs=2, action="append", default=[], metavar=("PATH", "N"))
    args = parser.parse_args()
    try:
        page_checks = [(name, int(count)) for name, count in args.page_count]
    except ValueError:
        parser.error("--page-count N must be an integer")
    result = check_archive(args.archive, page_checks)
    output = json.dumps(result, indent=2) + "\n"
    args.report.write_text(output, encoding="utf-8", newline="\n")
    print(output, end="")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
