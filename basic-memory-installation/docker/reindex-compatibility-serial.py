#!/usr/bin/env python3
"""Reindex only disposable compatibility projects with one SQLite writer.
Uses a release-specific internal adapter. Does not alter the installed image.
"""
import asyncio,importlib.util,json,time
from pathlib import Path
spec=importlib.util.spec_from_file_location('harness','/test/test-database-compatibility.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
from basic_memory.config import ConfigManager
from basic_memory import db
from basic_memory.repository import ProjectRepository
from basic_memory.index.local_project import LocalProjectIndexRuntimeFactory,run_local_project_index_for_project
from loguru import logger
logger.remove()
async def main():
 h.mark('codex-serial-index-repair');start=time.time();config=ConfigManager().config
 assert str(config.database_path)=='/work/state/memory.db'
 _,sessions=await db.get_or_create_db(db_path=config.database_path,db_type=db.DatabaseType.FILESYSTEM)
 async with db.scoped_session(sessions) as session:projects=await ProjectRepository().get_active_projects(session)
 project=next(p for p in projects if p.name=='codex')
 assert project.path=='/work/YindaXU-s-Codex-Memory'
 result=await run_local_project_index_for_project(project,runtime_factory=LocalProjectIndexRuntimeFactory(batch_size=1,index_max_concurrent=1),force_full=True,embeddings=False)
 failures=[{'path':str(f.path) if hasattr(f,'path') else None,'reason':f.reason} for b in result.batch_results for f in b.file_results if f.status.value=='failed']
 report={'seconds':time.time()-start,'files':result.total_files,'enqueued':result.enqueued_files,'batches':result.enqueued_batches,'failures':failures,'index_max_concurrent':1,'batch_size':1,'adapter':'Basic Memory 1.0.0 LocalProjectIndexRuntimeFactory'}
 (h.OUT/'serial-index-repair.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
 if failures:raise RuntimeError('Serial indexing still failed')
if __name__=='__main__':
 try:
  asyncio.run(main())
  h.cli(['reindex','--embeddings','--project','codex'],'codex-serial-embedding-refresh')
  h.inspect_state()
 finally:h.server.shutdown()
