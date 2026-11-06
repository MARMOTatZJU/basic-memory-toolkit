#!/usr/bin/env python3
"""Compatible global read/search/check/context commands for a canonical store."""
from legacy_cli import WORKSPACE, DEFAULT_MANIFEST, canonical, check_store, manifest_aliases, resolve
from legacy_cli import emit, main as _main, run

DEFAULT_ROOT = canonical.store_layout.canonical_default()
load_records = canonical.load_records
graph_edges = canonical.graph_edges


def check(root, manifest_path=None):
    report = check_store(root, manifest_path)
    records, _ = canonical.load_records(root)
    edges, _ = canonical.graph_edges(records)
    return report, records, edges


def main(argv=None):
    return _main("global", argv)


if __name__ == "__main__":
    raise SystemExit(run("global"))
