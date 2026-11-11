#!/usr/bin/env python3
"""Reindex one local Basic Memory 1.0.0 project with one SQLite writer.

Run this helper inside the Basic Memory application environment. It performs
the file/search-index phase only. Run the public embedding reindex separately
so embedding batches and GPU request concurrency remain independently tunable.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

os.environ.setdefault("LOGFIRE_IGNORE_NO_CONFIG", "1")

from basic_memory import db
from basic_memory.config import ConfigManager
from basic_memory.index.local_project import (
    LocalProjectIndexRuntimeFactory,
    run_local_project_index_for_project,
)
from basic_memory.indexing.models import IndexFileJobStatus
from basic_memory.repository import ProjectRepository


async def reindex(project_name: str, expected_path: Path, force_full: bool) -> dict:
    config = ConfigManager().config
    _, session_maker = await db.get_or_create_db(
        db_path=config.database_path,
        db_type=db.DatabaseType.FILESYSTEM,
    )
    async with db.scoped_session(session_maker) as session:
        projects = await ProjectRepository().get_active_projects(session)
    matches = [project for project in projects if project.name == project_name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one active project named {project_name!r}; found {len(matches)}")
    project = matches[0]
    actual_path = Path(project.path).resolve()
    if actual_path != expected_path.resolve():
        raise RuntimeError(f"Project path differs: {actual_path} != {expected_path.resolve()}")

    started = time.monotonic()
    result = await run_local_project_index_for_project(
        project,
        runtime_factory=LocalProjectIndexRuntimeFactory(batch_size=1, index_max_concurrent=1),
        force_full=force_full,
        embeddings=False,
    )
    failures = []
    for batch in result.batch_results:
        for file_result in batch.file_results:
            if file_result.status is IndexFileJobStatus.failed:
                failures.append({"path": str(getattr(file_result, "path", "")), "reason": file_result.reason})
    return {
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "basic_memory_version": "1.0.0",
        "project": project.name,
        "project_path": str(actual_path),
        "database_path": str(config.database_path),
        "force_full": force_full,
        "batch_size": 1,
        "index_max_concurrent": 1,
        "files_observed": result.total_files,
        "files_enqueued": result.enqueued_files,
        "batches": result.enqueued_batches,
        "failures": failures,
        "seconds": time.monotonic() - started,
        "status": "passed" if not failures else "failed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Configured local project name")
    parser.add_argument("--expected-path", type=Path, required=True, help="Exact path registered for the project")
    parser.add_argument("--incremental", action="store_true", help="Do not request a full file-index pass")
    parser.add_argument("--report", type=Path, required=True, help="JSON result path")
    args = parser.parse_args()

    report = asyncio.run(reindex(args.project, args.expected_path, not args.incremental))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
