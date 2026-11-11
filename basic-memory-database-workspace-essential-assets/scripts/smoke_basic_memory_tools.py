#!/usr/bin/env python3
"""Smoke-test Basic Memory read, search, and graph tools without exporting bodies.

Run inside the configured Basic Memory application environment. Repeat each
operation argument as needed. Values use PROJECT:IDENTIFIER or PROJECT:QUERY.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import time

os.environ.setdefault("LOGFIRE_IGNORE_NO_CONFIG", "1")

from loguru import logger

from basic_memory.mcp.tools.context import bm_context
from basic_memory.mcp.tools.ranked_search import bm_search
from basic_memory.mcp.tools.read import bm_read

logger.remove()


def scoped(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise ValueError("Operation values must use PROJECT:VALUE")
    project, target = value.split(":", 1)
    if not project or not target:
        raise ValueError("PROJECT and VALUE must both be nonempty")
    return project, target


def identifiers(value) -> list[str]:  # noqa: ANN001 - recursive JSON data
    found = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"permalink", "file_path", "entity"} and isinstance(item, str):
                found.add(item)
            found.update(identifiers(item))
    elif isinstance(value, list):
        for item in value:
            found.update(identifiers(item))
    return sorted(found)


async def run(args) -> dict:  # noqa: ANN001 - argparse namespace
    result = {"reads": [], "searches": [], "contexts": []}
    for value in args.read:
        project, identifier = scoped(value)
        started = time.monotonic()
        response = await bm_read(identifier=identifier, project=project, output_format="json")
        content = response.get("content", "") if isinstance(response, dict) else str(response)
        result["reads"].append(
            {
                "project": project,
                "identifier": identifier,
                "title": response.get("title") if isinstance(response, dict) else None,
                "permalink": response.get("permalink") if isinstance(response, dict) else None,
                "file_path": response.get("file_path") if isinstance(response, dict) else None,
                "content_returned": bool(content),
                "content_bytes": len(content.encode("utf-8")),
                "seconds": time.monotonic() - started,
            }
        )
    for value in args.search:
        project, query = scoped(value)
        started = time.monotonic()
        response = await bm_search(
            query=query,
            mode=args.mode,
            project=project,
            compact=True,
            page_size=10,
            output_format="json",
        )
        hits = response.get("results", [])
        result["searches"].append(
            {
                "project": project,
                "query": query,
                "mode": args.mode,
                "hits": [
                    {key: hit.get(key) for key in ("permalink", "file_path", "score", "type")}
                    for hit in hits
                ],
                "seconds": time.monotonic() - started,
            }
        )
    for value in args.context:
        project, identifier = scoped(value)
        started = time.monotonic()
        response = await bm_context(
            identifier=identifier,
            project=project,
            depth=2,
            since="365d",
            max_related=100,
            compact=True,
            output_format="json",
        )
        result["contexts"].append(
            {
                "project": project,
                "identifier": identifier,
                "returned_identifiers": identifiers(response),
                "seconds": time.monotonic() - started,
            }
        )
    result["status"] = "passed" if (
        all(item["content_returned"] for item in result["reads"])
        and all(item["hits"] for item in result["searches"])
        and all(item["returned_identifiers"] for item in result["contexts"])
    ) else "failed"
    result["scope"] = "Tool availability and nonempty results; result relevance and source claims are not validated."
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--read", action="append", default=[])
    parser.add_argument("--search", action="append", default=[])
    parser.add_argument("--context", action="append", default=[])
    parser.add_argument("--mode", choices=("text", "semantic", "hybrid"), default="text")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = asyncio.run(run(args))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
