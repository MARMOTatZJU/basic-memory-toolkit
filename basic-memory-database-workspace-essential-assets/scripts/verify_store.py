#!/usr/bin/env python3
"""Verify every identity/path/scope alias and authored local Markdown link."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

sys.dont_write_bytecode = True
import canonical_db
import store_layout


def verify(root, motorcycle=None, alias_plan=None):
    canonical, _ = store_layout.locate(root)
    records, errors = canonical_db.load_records(root)
    registry = store_layout.registry(root)
    checked = 0
    expected_aliases = registry.get("aliases", {})
    if alias_plan:
        expected_aliases = json.loads(alias_plan.read_text())["registry"]["aliases"]
    for alias, expected in expected_aliases.items():
        try:
            result = canonical_db.resolve(alias, records)
            if result["permalink"] != expected:
                errors.append({"kind": "alias_wrong_target", "alias": alias})
            checked += 1
            if alias.endswith(".md"):
                if canonical_db.resolve(alias[:-3], records)["permalink"] != expected:
                    errors.append({"kind": "extensionless_alias_wrong_target", "alias": alias})
        except ValueError as error:
            errors.append({"kind": "alias_unresolved", "alias": alias, "detail": str(error)})
    scopes = []
    if alias_plan:
        planned = json.loads(alias_plan.read_text())
        old_prefixes = {"/".join(move["old_path"].split("/")[:depth]) + "/"
                        for move in planned["moves"] for depth in range(1, len(move["old_path"].split("/")))}
        for prefix in sorted(old_prefixes):
            expected = {m["permalink"] for m in planned["moves"] if m["old_path"].startswith(prefix)}
            actual = {r["permalink"] for r in records if store_layout.scope_matches(r, prefix)}
            if prefix == "schema/":
                # This one existing folder now intentionally contains all four
                # shared schemas. Original module/schema scopes remain exact.
                scopes.append({"scope": prefix, "members": len(actual), "canonical_shared_schema_folder": True})
                continue
            if actual != expected:
                errors.append({"kind": "legacy_folder_scope", "scope": prefix, "missing": sorted(expected-actual), "extra": sorted(actual-expected)})
            scopes.append({"scope": prefix, "members": len(actual), "correct": actual == expected})
    for path in sorted((canonical / "views").glob("*.json")):
        view = json.loads(path.read_text())
        for prefix in view.get("scope_aliases", []):
            actual = {r["permalink"] for r in records if store_layout.scope_matches(r, prefix)}
            expected = set(view["members"])
            if actual != expected:
                errors.append({"kind": "scope_membership", "scope": prefix, "missing": sorted(expected-actual), "extra": sorted(actual-expected)})
            scopes.append({"scope": prefix, "members": len(actual), "correct": actual == expected})
    links = 0
    for record in records:
        for line_no, line in canonical_db.outside_fences(record["body"]):
            for target in re.findall(r"!?\[[^\]\n]*\]\(([^\)\n]+)\)", line):
                target = target.strip()
                if target.startswith("<") and ">" in target:
                    target = target[1:target.index(">")]
                if re.match(r"[A-Za-z][\w+.-]*:", target) or target.startswith("#"):
                    continue
                target = unquote(target.split("#", 1)[0])
                if not target: continue
                absolute = Path(target) if target.startswith("/") else Path(record["absolute_path"]).parent / target
                links += 1
                if not absolute.exists():
                    errors.append({"kind": "local_markdown_link", "path": record["path"], "line": line_no, "target": target})
    view_result = None
    if motorcycle:
        view_records, issues = canonical_db.load_records(motorcycle)
        errors.extend(issues)
        _, descriptor = store_layout.locate(motorcycle)
        if descriptor is None:
            errors.append({"kind": "motorcycle_view_required"})
            descriptor = {"members": []}
        if {r["permalink"] for r in view_records} != set(descriptor["members"]):
            errors.append({"kind": "lightweight_view_members"})
        view_result = {"members": len(view_records), "files": len(list(motorcycle.glob("*"))) if motorcycle.is_dir() else 0,
                       "requested_root_exists": motorcycle.is_dir(), "internal_view_name": descriptor.get('name'), "duplicate_authored_members": 0,
                       "same_dataset_hash": store_layout.dataset_manifest(motorcycle)["sha256"] == store_layout.dataset_manifest(root)["sha256"]}
        if not view_result["same_dataset_hash"]: errors.append({"kind": "view_dataset_hash"})
    return {"at": datetime.now(timezone.utc).isoformat(), "ok": not errors, "records": len(records), "checked_aliases": checked,
            "checked_local_markdown_links": links, "scopes": scopes, "motorcycle_view": view_result, "errors": errors}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--motorcycle", type=Path)
    parser.add_argument("--alias-plan", type=Path, help="Verify all original planned aliases, including entries removed as redundant")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.root, args.motorcycle, args.alias_plan)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["ok", "records", "checked_aliases", "checked_local_markdown_links", "motorcycle_view"]} | {"errors": len(report["errors"]), "report": str(args.report)}, ensure_ascii=False, indent=2))
