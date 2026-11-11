#!/usr/bin/env python3
"""Check or install the curated Basic Memory database ignore profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


DEFAULT_PROFILE = (
    Path(__file__).resolve().parent.parent
    / "templates"
    / "config"
    / "basic-memory-databases.bmignore"
)


def digest(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", required=True, type=Path)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help="Required in apply mode when an existing .bmignore would change.",
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    profile = args.profile.resolve()
    target = args.config_dir.resolve() / ".bmignore"
    if not profile.is_file():
        parser.error(f"profile does not exist: {profile}")

    before_hash = digest(target)
    profile_hash = digest(profile)
    status = "missing" if before_hash is None else (
        "current" if before_hash == profile_hash else "different"
    )
    backup_path: Path | None = None

    if args.apply and status != "current":
        if status == "different" and args.backup_dir is None:
            parser.error("--backup-dir is required before replacing an existing .bmignore")
        if status == "different":
            backup_dir = args.backup_dir.resolve()
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / "bmignore.before"
            if backup_path.exists():
                parser.error(f"backup already exists: {backup_path}")
            shutil.copy2(target, backup_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(profile, target)

    report = {
        "config_dir": str(args.config_dir.resolve()),
        "target": str(target),
        "profile": str(profile),
        "status_before": status,
        "applied": bool(args.apply and status != "current"),
        "backup": str(backup_path) if backup_path else None,
        "profile_sha256": profile_hash,
        "target_sha256": digest(target),
        "passed": digest(target) == profile_hash,
    }
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if (report["passed"] or not args.apply) else 1


if __name__ == "__main__":
    raise SystemExit(main())
