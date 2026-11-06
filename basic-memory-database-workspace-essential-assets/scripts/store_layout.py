"""Resolve canonical records, lightweight views, and legacy scope aliases.

This module reads local files. It does not fetch or write Notion content.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


WORKSPACE = next(p for p in Path(__file__).resolve().parents if (p / 'scripts/memory_db.py').exists())


def canonical_default():
    """Allow an isolated staged store without falling back to active aliases."""
    value = os.environ.get('CANONICAL_ROOT')
    if value:
        return Path(value).resolve()
    for parent in WORKSPACE.parents:
        current = parent / 'basic-memory-databases/MARMOTatZJU-s-Notion'
        if (current / 'registry/aliases.json').is_file():
            return current
    return WORKSPACE.parent / 'basic-memory-database/MARMOTatZJU-s-Notion'


def _view(canonical, name):
    if not isinstance(name, str) or Path(name).name != name or name in {'', '.', '..'}:
        raise ValueError('Invalid root-route view name')
    path = canonical / 'views' / (name + '.json')
    if not path.is_file():
        raise ValueError('Canonical view definition is missing: ' + str(path))
    view = json.loads(path.read_text())
    if view.get('name') != name or not isinstance(view.get('members'), list) or not isinstance(view.get('scope_aliases'), list):
        raise ValueError('Invalid authoritative view definition')
    return view


def _registered_route(root, canonical):
    path = canonical / 'registry/root-routes.json'
    if not path.is_file():
        return None
    data = json.loads(path.read_text())
    if data.get('version') != 1 or not isinstance(data.get('routes'), list):
        raise ValueError('Invalid root-route registry')
    routes = {}
    for route in data['routes']:
        alias = Path(route['path'])
        alias = alias.resolve() if alias.is_absolute() else (canonical / alias).resolve()
        if alias in routes and routes[alias]['view'] != route['view']:
            raise ValueError('Conflicting exact root routes')
        routes[alias] = route
    if root not in routes:
        return None
    if not (canonical / 'registry/aliases.json').is_file():
        raise ValueError('Canonical alias registry is missing')
    route = routes[root]
    view = _view(canonical, route['view'])
    # A retired root is a virtual CLI alias. It needs no directory or copy.
    if route.get('kind') == 'internal-view':
        descriptor = root / 'view.json'
        if not descriptor.is_file():
            raise ValueError('Internal view descriptor is missing')
        _descriptor_view(root, canonical)
    return canonical, view


def _descriptor_view(root, required_canonical=None):
    descriptor = root / 'view.json'
    view = json.loads(descriptor.read_text())
    target = Path(view['canonical_root'])
    if not target.is_absolute():
        target = (root / target).resolve()
    else:
        target = target.resolve()
    if target == root:
        raise ValueError('A lightweight view cannot point to itself')
    if required_canonical is not None and target != required_canonical:
        raise ValueError('View points outside the configured canonical store')
    if not (target / 'registry/aliases.json').is_file():
        raise ValueError('Canonical registry is missing: ' + str(target))
    expected = _view(target, view['name'])
    if view.get('members') != expected.get('members') or view.get('scope_aliases') != expected.get('scope_aliases'):
        raise ValueError('Lightweight view differs from its canonical definition')
    return target, view


def locate(root, canonical_root=None):
    root = Path(root).resolve()
    canonical = Path(canonical_root).resolve() if canonical_root is not None else canonical_default().resolve()
    registered = _registered_route(root, canonical)
    if registered is not None:
        return registered
    if (canonical_root is not None or os.environ.get('CANONICAL_ROOT')) and root != canonical:
        # The override is a deliberate isolation boundary, not a fallback hint.
        if (root / 'view.json').is_file():
            return _descriptor_view(root, canonical)
        raise ValueError('Root is outside the configured canonical store: ' + str(root))
    descriptor = root / "view.json"
    if descriptor.is_file():
        return _descriptor_view(root)
    return root, None


def registry(root):
    canonical, _ = locate(root)
    path = canonical / "registry/aliases.json"
    return json.loads(path.read_text()) if path.exists() else {"aliases": {}, "scope_aliases": {}}


def view_members(root):
    _, view = locate(root)
    return set(view["members"]) if view else None


def scope_matches(record, prefix):
    if not prefix:
        return True
    prefix = prefix.replace("\\", "/")
    return any(path.startswith(prefix) for path in [record["path"], *record.get("scope_paths", []), *record.get("legacy_paths", [])])


def normalize_scope(root, prefix):
    """Interpret a relative old folder scope within the requested view."""
    _, view = locate(root)
    if not view:
        return prefix
    if not prefix:
        return view["scope_aliases"][0]
    old = "modules/" + view["name"] + "/" + prefix
    if any(alias.startswith(old) for alias in registry(root).get("aliases", {})):
        return old
    return prefix


def dataset_manifest(root, canonical_root=None):
    """Hash canonical Markdown plus routing definitions, even for a view root."""
    canonical, view = locate(root, canonical_root)
    files = [{"path": p.relative_to(canonical).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(canonical.rglob("*.md"))]
    routing_paths = {p for folder in [canonical / 'registry', canonical / 'views'] for p in folder.glob('*.json')}
    routing_paths.update(canonical.rglob('view.json'))
    routing = [{"path": p.relative_to(canonical).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in sorted(routing_paths)]
    # A view descriptor is checked against its canonical definition by locate().
    # Thus a view and its canonical root share one index freshness identity.
    value = {"files": files, "routing_files": routing}
    return {"scope": "canonical authored Markdown and registry/view routing", "canonical_root": str(canonical),
            "sha256": hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest(), **value}
