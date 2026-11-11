#!/usr/bin/env python3
"""Find or expand YAML aliases in Basic Memory Markdown frontmatter.

Basic Memory 1.0.0 rejects YAML anchors and aliases in note frontmatter. The
check mode is read-only. Apply mode requires an explicit backup directory and
verifies that parsed metadata and body text remain equal after normalization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

import yaml
from yaml.tokens import AliasToken, AnchorToken


FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n(.*)\Z", re.DOTALL)


class NoAliasDumper(yaml.SafeDumper):
    """Emit complete values instead of YAML anchors and aliases."""

    def ignore_aliases(self, data):  # noqa: ANN001 - PyYAML hook signature
        return True


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inspect_file(path: Path) -> tuple[dict, str, bool]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.fullmatch(text)
    if match is None:
        raise ValueError(f"Markdown frontmatter is missing or malformed: {path}")
    yaml_text, body = match.groups()
    metadata = yaml.safe_load(yaml_text)
    if not isinstance(metadata, dict):
        raise ValueError(f"Frontmatter must be a mapping: {path}")
    has_alias = any(isinstance(token, (AliasToken, AnchorToken)) for token in yaml.scan(yaml_text))
    return metadata, body, has_alias


def normalize(path: Path, root: Path, backup_dir: Path) -> dict:
    before = path.read_text(encoding="utf-8")
    metadata, body, has_alias = inspect_file(path)
    if not has_alias:
        return {"path": path.relative_to(root).as_posix(), "changed": False}

    relative = path.relative_to(root)
    backup = backup_dir / relative
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup)

    encoded = yaml.dump(
        metadata,
        Dumper=NoAliasDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=4096,
    )
    after = f"---\n{encoded}---\n{body}"
    new_metadata, new_body, still_has_alias = inspect_text(after, path)
    if new_metadata != metadata or new_body != body or still_has_alias:
        raise RuntimeError(f"Normalization invariant failed: {path}")
    path.write_text(after, encoding="utf-8")
    return {
        "path": relative.as_posix(),
        "changed": True,
        "backup": str(backup),
        "metadata_preserved": True,
        "body_preserved": True,
        "before_sha256": digest(before),
        "after_sha256": digest(after),
    }


def inspect_text(text: str, label: Path) -> tuple[dict, str, bool]:
    match = FRONTMATTER.fullmatch(text)
    if match is None:
        raise ValueError(f"Generated frontmatter is malformed: {label}")
    yaml_text, body = match.groups()
    metadata = yaml.safe_load(yaml_text)
    has_alias = any(isinstance(token, (AliasToken, AnchorToken)) for token in yaml.scan(yaml_text))
    return metadata, body, has_alias


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Database root to scan")
    parser.add_argument("--path", action="append", type=Path, default=[], help="Relative Markdown path; repeat as needed")
    parser.add_argument("--apply", action="store_true", help="Expand aliases after creating backups")
    parser.add_argument("--backup-dir", type=Path, help="Required with --apply; must be outside the database root")
    parser.add_argument("--report", type=Path, help="Optional JSON report")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    if args.apply and args.backup_dir is None:
        parser.error("--backup-dir is required with --apply")
    backup_dir = args.backup_dir.resolve() if args.backup_dir else None
    if backup_dir and (backup_dir == root or backup_dir.is_relative_to(root)):
        parser.error("Keep --backup-dir outside the database root")

    files = [root / path for path in args.path] if args.path else sorted(root.rglob("*.md"))
    results = []
    for path in files:
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or not resolved.is_file():
            raise ValueError(f"Path is not a file below the database root: {path}")
        metadata, body, has_alias = inspect_file(resolved)
        result = {
            "path": resolved.relative_to(root).as_posix(),
            "has_yaml_alias": has_alias,
            "metadata_keys": len(metadata),
            "body_sha256": digest(body),
        }
        if args.apply:
            result.update(normalize(resolved, root, backup_dir))
        results.append(result)

    report = {
        "root": str(root),
        "mode": "apply" if args.apply else "check",
        "files_checked": len(results),
        "files_with_aliases": sum(bool(item["has_yaml_alias"]) for item in results),
        "results": results,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("mode", "files_checked", "files_with_aliases")}, indent=2))
    return 1 if not args.apply and report["files_with_aliases"] else 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
