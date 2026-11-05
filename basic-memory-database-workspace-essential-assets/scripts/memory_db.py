#!/usr/bin/env python3
"""Compatible MotorcycleNotes commands over the canonical store or a view."""
from legacy_cli import authored as _authored, canonical as _canonical
from legacy_cli import WORKSPACE, check_store, legacy_context, main as _main, run

# Preserve the old parser helpers for local importers. Parsing lives separately.
for _name in dir(_authored):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_authored, _name)
load_records = _canonical.load_records
resolve = _canonical.resolve
graph_edges = _canonical.graph_edges
DEFAULT_ROOT = _canonical.store_layout.canonical_default() / 'driving/MotorcycleNotes'


def check(root, records=None, load_issues=None, source_dir=None):
    return check_store(root, sources=source_dir, records=records, load_issues=load_issues)


def main(argv=None):
    return _main("memory", argv)


if __name__ == "__main__":
    raise SystemExit(run("memory"))
