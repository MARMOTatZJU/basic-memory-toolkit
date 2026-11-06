# Configuration and data schema inventory

[Collection index](README.md)

These declarations describe data boundaries. They are not a complete JSON Schema export.
Source declarations preserve validation details that this compact table omits.

## Configuration fields

| Field | Annotation | Source default |
| --- | --- | --- |
| `env` | `Environment` | `'dev'` |
| `projects` | `Dict[str, ProjectEntry]` | `lambda : {'main': ProjectEntry(path=str(Path(os.getenv('BASIC_MEMORY_HOME', Path.home() / 'basic-memory'))))} if os.getenv('BASIC_MEMORY_HOME') else {}` |
| `default_project` | `Optional[str]` | `None` |
| `log_level` | `str` | `'INFO'` |
| `logfire_enabled` | `bool` | `False` |
| `logfire_send_to_logfire` | `bool` | `False` |
| `logfire_service_name` | `str` | `'basic-memory'` |
| `logfire_environment` | `str \| None` | `None` |
| `database_backend` | `DatabaseBackend` | `DatabaseBackend.SQLITE` |
| `database_url` | `Optional[str]` | `None` |
| `redis_url` | `Optional[str]` | `None` |
| `redis_max_connections` | `int` | `20` |
| `semantic_vector_index` | `Literal['pgvector', 'milvus']` | `'pgvector'` |
| `milvus_uri` | `str \| None` | `None` |
| `milvus_token` | `str \| None` | `None` |
| `milvus_timeout_seconds` | `float` | `30.0` |
| `milvus_collection_prefix` | `str` | `'basic_memory'` |
| `milvus_database` | `str` | `'default'` |
| `semantic_embedding_provider` | `str` | `'fastembed'` |
| `semantic_embedding_model` | `str` | `'bge-small-en-v1.5'` |
| `semantic_embedding_api_base` | `str \| None` | `None` |
| `semantic_embedding_api_key` | `str \| None` | `None` |
| `semantic_embedding_dimensions` | `int \| None` | `None` |
| `semantic_embedding_forward_dimensions` | `bool \| None` | `None` |
| `semantic_embedding_batch_size` | `int` | `2` |
| `semantic_embedding_request_concurrency` | `int` | `4` |
| `semantic_embedding_document_input_type` | `str \| None` | `None` |
| `semantic_embedding_query_input_type` | `str \| None` | `None` |
| `semantic_embedding_document_prefix` | `str \| None` | `None` |
| `semantic_embedding_query_prefix` | `str \| None` | `None` |
| `semantic_embedding_sync_batch_size` | `int` | `2` |
| `semantic_postgres_prepare_concurrency` | `int` | `4` |
| `semantic_embedding_cache_dir` | `str \| None` | `None` |
| `semantic_embedding_threads` | `int \| None` | `None` |
| `semantic_embedding_parallel` | `int \| None` | `None` |
| `import_upload_max_bytes` | `int` | `100 * 1024 * 1024` |
| `semantic_vector_k` | `int` | `100` |
| `semantic_min_similarity` | `float` | `0.55` |
| `default_search_type` | `Literal['text', 'vector', 'hybrid'] \| None` | `None` |
| `reranker_enabled` | `bool` | `False` |
| `reranker_provider` | `str` | `'fastembed'` |
| `reranker_model` | `str` | `DEFAULT_FASTEMBED_RERANK_MODEL` |
| `reranker_max_document_chars` | `int` | `2000` |
| `reranker_timeout` | `float` | `30.0` |
| `reranker_api_base` | `str \| None` | `None` |
| `reranker_api_key` | `str \| None` | `None` |
| `reranker_candidates` | `int` | `20` |
| `db_pool_size` | `int` | `20` |
| `db_pool_overflow` | `int` | `40` |
| `db_pool_recycle` | `int` | `180` |
| `materialization_workers` | `int` | `4` |
| `sqlite_synchronous` | `Literal['OFF', 'NORMAL', 'FULL', 'EXTRA']` | `'NORMAL'` |
| `sqlite_mmap_size` | `int` | `268435456` |
| `sqlite_wal_autocheckpoint` | `int` | `1000` |
| `sqlite_page_size` | `int` | `4096` |
| `index_delay` | `int` | `1000` |
| `watch_project_reload_interval` | `int` | `300` |
| `update_permalinks_on_move` | `bool` | `False` |
| `index_changes` | `bool` | `True` |
| `index_batch_size` | `int` | `32` |
| `index_batch_max_bytes` | `int` | `8 * 1024 * 1024` |
| `index_parse_max_concurrent` | `int` | `8` |
| `index_entity_max_concurrent` | `int` | `4` |
| `index_metadata_update_max_concurrent` | `int` | `4` |
| `date_order` | `Literal['YMD', 'DMY', 'MDY']` | `'YMD'` |
| `kebab_filenames` | `bool` | `False` |
| `write_note_overwrite_default` | `bool` | `False` |
| `enable_posix_tools` | `bool` | `True` |
| `enable_project_delete` | `bool` | `False` |
| `cli_output_style` | `Literal['rich', 'plain']` | `'rich'` |
| `ensure_frontmatter_on_sync` | `bool` | `True` |
| `permalinks_include_project` | `bool` | `True` |
| `skip_initialization_sync` | `bool` | `False` |
| `format_on_save` | `bool` | `False` |
| `formatter_command` | `Optional[str]` | `None` |
| `formatters` | `Dict[str, str]` | `dict` |
| `formatter_timeout` | `float` | `5.0` |
| `project_root` | `Optional[str]` | `None` |
| `cloud_client_id` | `str` | `'client_01K6KWQPW6J1M8VV7R3TZP5A6M'` |
| `cloud_domain` | `str` | `'https://eloquent-lotus-05.authkit.app'` |
| `cloud_host` | `str` | `lambda : os.getenv('BASIC_MEMORY_CLOUD_HOST', 'https://cloud.basicmemory.com')` |
| `cloud_promo_opt_out` | `bool` | `False` |
| `cloud_promo_first_run_shown` | `bool` | `False` |
| `cloud_promo_last_version_shown` | `Optional[str]` | `None` |
| `auto_update` | `bool` | `True` |
| `update_check_interval` | `int` | `86400` |
| `auto_update_last_checked_at` | `Optional[datetime]` | `None` |
| `cloud_api_key` | `Optional[str]` | `None` |
| `default_workspace` | `Optional[str]` | `None` |

## Pydantic and persisted data classes

The field list includes fields declared directly on each class. Inherited fields and computed properties require the source.

| Class | Source | Declared fields |
| --- | --- | --- |
| `Entity` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L32) | id, external_id, title, note_type, entity_metadata, content_type, project_id, permalink, file_path, checksum, sync_checksum, mtime, size, vector_sync_deferred_at, created_at, updated_at, created_by, last_updated_by |
| `NoteContent` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L186) | entity_id, project_id, external_id, file_path, markdown_content, db_version, db_checksum, file_version, file_checksum, file_write_status, last_source, updated_at, file_updated_at, last_materialization_error, last_materialization_attempt_at |
| `NoteFileVacate` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L255) | id, project_id, entity_id, file_path, file_checksum, created_at |
| `NoteSection` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L303) | id, project_id, entity_id, heading, level, heading_path, heading_path_digest, duplicate_index, start_line, end_line, start_offset, end_offset |
| `Observation` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L430) | id, project_id, entity_id, content, category, context, tags, duplicate_index |
| `MemoryTimeIndex` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L490) | id, project_id, entity_id, source_type, source_id, time_kind, range_axis, lower_value, upper_value, lower_inclusive, upper_inclusive, is_empty, extractor, source_text, assertion_metadata |
| `Relation` | [knowledge.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/knowledge.py#L596) | id, project_id, from_id, to_id, to_name, relation_type, context, generation |
| `Project` | [project.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/project.py#L26) | id, external_id, name, description, permalink, path, is_active, is_default, created_at, updated_at, last_scan_timestamp, last_file_count, last_indexed_at, partition_position |
| `AcceptedProjectNoteChange` | [project.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/project.py#L123) | id, project_id, project_external_id, partition_position, entity_id, note_external_id, permalink, title, operation, file_path, previous_file_path, accepted_at, source, db_version, db_checksum, actor_user_profile_id, actor_kind, actor_name, materialized_at |
| `RelationSearchRefresh` | [relation_search_refresh.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/models/relation_search_refresh.py#L11) | id, project_id, entity_id, publication_generation, created_at |
| `Observation` | [base.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/base.py#L212) | category, content, tags, context |
| `Relation` | [base.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/base.py#L221) | from_id, to_id, relation_type, context |
| `Entity` | [base.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/base.py#L235) | title, content, directory, file_name, note_type, entity_metadata, content_type |
| `TenantMountInfo` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L12) | tenant_id, bucket_name |
| `MountCredentials` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L19) | access_key, secret_key |
| `CloudProject` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L26) | name, path |
| `CloudProjectList` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L33) | projects |
| `CloudProjectCreateRequest` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L39) | name, path, set_default, visibility |
| `CloudProjectCreateResponse` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L51) | message, status, default, old_project, new_project |
| `WorkspaceInfo` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L65) | tenant_id, workspace_type, slug, name, role, is_default, organization_id, has_active_subscription |
| `WorkspaceListResponse` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L80) | workspaces, count, default_workspace_id, current_workspace_id |
| `CloudProjectIndexStatus` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L140) | project_name, project_id, last_scan_timestamp, last_file_count, current_file_count, total_entities, total_note_content_rows, note_content_synced, note_content_pending, note_content_failed, note_content_external_changes, total_indexed_entities, embedding_opt_out_entities, embeddable_indexed_entities, total_entities_with_chunks, total_chunks, total_embeddings, orphaned_chunks, vector_tables_exist, materialization_current, search_current, embeddings_current, project_current, reindex_recommended, reindex_reason |
| `CloudTenantIndexStatusResponse` | [cloud.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/cloud.py#L178) | tenant_id, fly_app_name, email, projects, error |
| `DeleteEntitiesRequest` | [delete.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/delete.py#L27) | permalinks |
| `DirectoryNode` | [directory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/directory.py#L19) | name, file_path, directory_path, type, children, title, permalink, external_id, entity_id, note_type, content_type, format, updated_at |
| `DirectoryListResponse` | [directory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/directory.py#L43) | nodes, page, page_size, total, has_more |
| `IndexProjectAction` | [doctor.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/doctor.py#L39) | kind |
| `ReindexSearchAction` | [doctor.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/doctor.py#L45) | kind, full |
| `DoctorFinding` | [doctor.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/doctor.py#L63) | check, severity, summary, evidence, action |
| `ProjectDoctorReport` | [doctor.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/doctor.py#L77) | findings |
| `DocumentSourceV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L99) | kind, media_type, entity_external_id, file_path, checksum, size_bytes, storage_version_id, storage_etag |
| `_DocumentExtractionDiagnosticsV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L120) | engine, engine_version, profile, options_hash, classification, status, extracted_at, duration_ms, page_count, extracted_page_count, requires_ocr, ocr_page_count, pages_needing_ocr |
| `DocumentExtractionSummaryV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L167) | confidence, has_encoding_issues, has_tables, has_columns |
| `DocumentExtractionV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L191) | page_map, confidence, has_encoding_issues, has_tables, has_columns |
| `DocumentIngestionV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L215) | stage, pipeline_version, prompt_version, run_id, input_checksum, base_checksum |
| `DocumentMetadataV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L234) | kind, language, authors, published_at |
| `DocumentPageLocatorV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L250) | page, page_label |
| `DocumentCitationSourceV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L263) | id, resource, title, locator |
| `DocumentNoteFrontmatterV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L283) | schema_version, title, type, schema_ref, tags, permalink, created, modified, source, sources, extraction, ingestion, document, bm_parse_semantics |
| `DocumentMarkdownV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L373) | frontmatter, body |
| `DocumentRevisionReferenceV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L390) | kind, checksum, storage_version_id, created_at |
| `DocumentIngestionFailureV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L404) | code, message, retryable |
| `DocumentIngestionRunStateV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L412) | run_id, stage, pipeline_version, prompt_version, input_checksum, started_at, completed_at |
| `DocumentIngestionRunOutputV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L441) | document_entity_external_id, document_file_path, raw, current |
| `DocumentIngestionRunFrontmatterV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L461) | schema_version, title, type, schema_ref, tags, permalink, created, modified, source, extraction, ingestion, output, failure, bm_parse_semantics |
| `DocumentIngestionRunMarkdownV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L539) | frontmatter, body |
| `DocumentAgentObservationV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L554) | category, content, tags, locator, context |
| `DocumentAgentRelationV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L597) | relation_type, target, context |
| `DocumentAgentOutputV1` | [document.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document.py#L641) | schema_version, title, body, tags, document, observations, relations |
| `DocumentPageRangeV1` | [document_page_map.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document_page_map.py#L9) | page, start, end |
| `DocumentPageMapV1` | [document_page_map.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/document_page_map.py#L25) | unit, body_checksum, body_length, pages |
| `ImportResult` | [importer.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/importer.py#L8) | import_count, success, error_message |
| `ChatImportResult` | [importer.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/importer.py#L16) | conversations, messages |
| `ProjectImportResult` | [importer.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/importer.py#L23) | documents, prompts |
| `EntityImportResult` | [importer.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/importer.py#L30) | entities, relations, skipped_entities |
| `InspectChunksRequest` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L34) | identifier |
| `InspectChunkReadiness` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L40) | total, ready, pending, stale, orphaned, missing |
| `InspectChunk` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L55) | chunk_key, ordinal, text, source_hash, embedding_model, vector_index, status, updated_at |
| `InspectSearchRow` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L68) | type, id, title, category, relation_type, content_preview, chunks |
| `InspectDetachedSearchRow` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L80) | type, id, source_row_gone, chunks |
| `InspectIndexBehindRowsDetail` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L89) | entity_fingerprint_indexed, entity_fingerprint_current, missing_chunk_count |
| `InspectRowsBehindFileDetail` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L99) | entity_checksum, current_file_checksum, db_checksum, file_checksum, file_write_status |
| `InspectChunksResponse` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L114) | entity_id, external_id, permalink, file_path, title, entity_checksum, configured_embedding_model, configured_vector_index, readiness, entity_fingerprint_indexed, entity_fingerprint_current, stale, freshness, freshness_detail, rows, detached |
| `InspectQueryRequest` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L176) | query, limit, offset |
| `InspectQueryWindow` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L184) | limit, offset, candidate_limit, rerank_pool |
| `InspectQueryReranker` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L191) | enabled, model, candidates, applied, skipped_reason |
| `InspectQueryEngine` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L199) | embedding_model, vector_index, ready_rows, pending_rows, other_identity_rows, fusion_formula, min_similarity, min_similarity_source, reranker |
| `InspectQueryStage` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L213) | name, count_in, count_out, dropped, ms, relaxed_fallback_used |
| `InspectMatchedChunk` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L224) | chunk_key, similarity |
| `InspectDroppedChunk` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L229) | chunk_key, similarity, reason, stored_model, stored_index |
| `InspectQueryRejectionDetail` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L243) | reason, chunk_key, similarity, threshold, stored_model, stored_index, rank, score |
| `InspectQueryScores` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L254) | fts_raw, fts_normalized, fts_rank, vector_similarity, vector_rank, fused_score, fused_rank, dual_source, pre_rerank_rank, pre_rerank_score, rerank_score, post_rerank_rank, final_rank, final_score |
| `InspectQueryCandidate` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L285) | type, id, external_id, title, permalink, file_path, disposition, rejection_detail, matched_chunks, dropped_chunks, scores |
| `InspectQueryTimings` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L299) | total, embedding, vector_query, fts, fusion, rerank |
| `InspectQueryResponse` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L308) | query, retrieval_mode, project_id, window, engine, stages, candidates, timings_ms |
| `_ForeignOwnerDropKey` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L322) | entity_id, key |
| `_UnattributedDropKey` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L335) | entity_id, raw_chunk_key |
| `_CandidateTrace` | [inspect.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/inspect.py#L347) | key, raw_chunk_key, entity_id, title, permalink, file_path, rejection, matched_chunks, dropped_chunks, scores |
| `EntitySummary` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L136) | type, external_id, entity_id, permalink, title, content, file_path, created_at, updated_at |
| `RelationSummary` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L165) | type, relation_id, entity_id, title, file_path, permalink, relation_type, from_entity, from_entity_id, from_entity_external_id, to_entity, to_name, to_entity_id, to_entity_external_id, created_at |
| `ObservationSummary` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L194) | type, observation_id, entity_id, entity_external_id, title, file_path, permalink, category, content, created_at |
| `MemoryMetadata` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L216) | uri, types, depth, timeframe, generated_at, primary_count, related_count, total_results, total_relations, total_observations |
| `ContextResult` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L236) | primary_result, observations, related_results |
| `GraphContext` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L255) | results, metadata, page, page_size, has_more |
| `ActivityStats` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L271) | total_projects, active_projects, most_active_project, total_items, total_entities, total_relations, total_observations |
| `ProjectActivity` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L283) | project_name, project_path, activity, item_count, last_activity, active_folders |
| `ProjectActivitySummary` | [memory.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/memory.py#L300) | projects, summary, timeframe, generated_at, guidance |
| `ProjectIndexObservedFileResponse` | [project_index.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_index.py#L14) | path, checksum, size |
| `ProjectIndexStatusResponse` | [project_index.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_index.py#L22) | total_files, observed_files, readiness |
| `ProjectIndexRunResponse` | [project_index.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_index.py#L57) | total_files, enqueued_files, enqueued_batches, deleted_files |
| `ProjectStatistics` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L13) | total_entities, total_observations, total_relations, total_unresolved_relations, note_types, observation_categories, relation_types, most_connected_entities, isolated_entities |
| `ActivityMetrics` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L46) | recently_created, recently_updated, monthly_growth |
| `SystemStatus` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L63) | version, database_path, database_size, watch_status, timestamp |
| `EmbeddingStatus` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L82) | vector_runtime_available, embedding_provider, embedding_model, embedding_dimensions, embedding_document_prefix_set, embedding_query_prefix_set, total_indexed_entities, total_entities_with_chunks, total_chunks, total_embeddings, orphaned_chunks, vector_tables_exist, reindex_recommended, reindex_reason |
| `ProjectInfoResponse` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L130) | project_name, project_path, available_projects, default_project, statistics, activity, system, embedding_status |
| `ProjectInfoRequest` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L156) | name, path, set_default |
| `WatchEvent` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L164) | timestamp, path, action, status, checksum, error |
| `WatchServiceState` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L173) | running, start_time, pid, error_count, last_error, last_scan, indexed_files, recent_events |
| `ProjectWatchStatus` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L216) | name, path, watch_status |
| `ProjectItem` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L226) | id, external_id, name, path, is_default, display_name, is_private |
| `ProjectList` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L251) | projects, default_project |
| `ProjectStatusResponse` | [project_info.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_info.py#L258) | message, status, default, old_project, new_project, deletion_status, file_delete_status, job_id |
| `ProjectIndexStage` | [project_readiness.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_readiness.py#L72) | name, phase, pending, total |
| `ProjectIndexReadiness` | [project_readiness.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/project_readiness.py#L86) | phase, last_indexed_at, files_on_disk, indexed_entities, stages |
| `PromptContextItem` | [prompt.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/prompt.py#L10) | primary_results, related_results |
| `ContinueConversationRequest` | [prompt.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/prompt.py#L17) | topic, timeframe, search_items_limit, depth, related_items_limit |
| `SearchPromptRequest` | [prompt.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/prompt.py#L47) | query, timeframe |
| `PromptMetadata` | [prompt.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/prompt.py#L59) | query, timeframe, search_count, context_count, observation_count, relation_count, total_items, search_limit, context_depth, related_limit, generated_at |
| `PromptResponse` | [prompt.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/prompt.py#L79) | prompt, context, metadata |
| `SearchNodesRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L14) | query, category |
| `GetEntitiesRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L46) | permalinks |
| `CreateRelationsRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L57) | relations |
| `EditEntityRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L61) | operation, content, section, find_text, expected_replacements, replace_subsections, metadata |
| `MoveEntityRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L135) | identifier, destination_path, project |
| `MoveDirectoryRequest` | [request.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/request.py#L159) | source_directory, destination_directory, project |
| `ObservationResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L33) | permalink |
| `RelationResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L50) | permalink, from_id, to_id, to_name |
| `EntityResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L152) | permalink, title, file_path, note_type, entity_metadata, checksum, content_type, external_id, observations, relations, created_at, updated_at |
| `EntityListResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L212) | entities |
| `SearchNodesResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L253) | matches, query |
| `DeleteEntitiesResponse` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L282) | deleted |
| `DirectoryMoveError` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L297) | path, error |
| `DirectoryDeleteError` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L304) | path, error |
| `DirectoryMoveResult` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L311) | total_files, successful_moves, failed_moves, moved_files, errors, destination |
| `DirectoryDeleteResult` | [response.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/response.py#L341) | total_files, successful_deletes, failed_deletes, deleted_files, errors |
| `FieldResultResponse` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L16) | field_name, field_type, required, status, values, message |
| `NoteValidationResponse` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L27) | note_identifier, schema_entity, passed, field_results, unmatched_observations, unmatched_relations, warnings, errors |
| `TypeValidationSummary` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L46) | note_type, total_notes, total_entities, valid_count, warning_count, error_count |
| `ValidationReport` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L57) | note_type, total_notes, total_entities, valid_count, warning_count, error_count, results, type_summaries |
| `FieldFrequencyResponse` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L76) | name, source, count, total, percentage, sample_values, is_array, target_type |
| `InferenceReport` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L95) | note_type, notes_analyzed, field_frequencies, suggested_schema, suggested_required, suggested_optional, excluded |
| `DriftFieldResponse` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L116) | name, source, count, total, percentage |
| `DriftReport` | [schema.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/schema.py#L126) | note_type, schema_found, new_fields, dropped_fields, cardinality_changes, notes_compared |
| `SearchQuery` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L63) | permalink, permalink_match, text, title, note_types, entity_types, categories, after_date, metadata_filters, file_path_prefix, tags, status, retrieval_mode, min_similarity, valid_at, valid_overlaps, time_kind |
| `ScopedSearchQuery` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L237) | project_ids |
| `TemporalRangeValue` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L248) | axis, literal, lower, upper, lower_inclusive, upper_inclusive, is_empty |
| `TemporalResultMetadata` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L271) | kind, valid_during, source_text |
| `SearchResult` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L283) | title, type, score, entity, external_id, permalink, content, content_length, content_truncated, matched_chunk, file_path, updated_at, metadata, entity_id, observation_id, relation_id, category, from_entity, to_entity, relation_type, temporal, project_id, project_external_id |
| `SearchResponse` | [search.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/search.py#L327) | results, current_page, page_size, total, total_is_exact, has_more, query_hint, temporal_applied |
| `AcceptedNoteContentBatchRequest` | [accepted_content.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/accepted_content.py#L13) | entity_ids |
| `AcceptedNoteContentItem` | [accepted_content.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/accepted_content.py#L29) | external_id, content |
| `AcceptedNoteContentBatchResponse` | [accepted_content.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/accepted_content.py#L36) | items, missing_entity_ids |
| `EntityResolveRequest` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L11) | identifier, source_path, strict |
| `EntityResolveResponse` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L40) | external_id, entity_id, project_external_id, permalink, file_path, title, resolution_method |
| `LinkResolveRequest` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L57) | identifier, source_path, strict |
| `LinkResolveResponse` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L77) | external_id, entity_id, target_project_external_id, permalink, file_path, title, resolution_method |
| `IndexFileRequest` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L98) | file_path |
| `MoveEntityRequestV2` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L113) | destination_path |
| `MoveDirectoryRequestV2` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L128) | source_directory, destination_directory |
| `DeleteDirectoryRequestV2` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L149) | directory |
| `EntityResponseV2` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L164) | external_id, id, title, note_type, content_type, permalink, file_path, content, entity_metadata, observations, relations, created_at, updated_at, created_by, last_updated_by, db_version, db_checksum, file_version, file_checksum, file_write_status, last_source, file_updated_at, last_materialization_error, sync_error, section, content_start_line, content_end_line, content_total_lines, content_truncated, content_continue_line, api_version |
| `ProjectResolveRequest` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L253) | identifier |
| `ProjectResolveResponse` | [entity.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/entity.py#L269) | external_id, project_id, name, permalink, path, is_active, is_default, resolution_method |
| `GraphNode` | [graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py#L8) | external_id, title, note_type, file_path |
| `GraphEdge` | [graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py#L17) | from_id, to_id, relation_type |
| `GraphResponse` | [graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py#L25) | nodes, edges |
| `OrphanEntitiesResponse` | [graph.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/graph.py#L34) | entities, total |
| `NotePlacementRequest` | [note_placement.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_placement.py#L8) | identifier |
| `NoteCreatePlacementResponse` | [note_placement.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_placement.py#L18) | kind, readings, directory, title |
| `AmbiguousNotePlacementResponse` | [note_placement.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_placement.py#L29) | kind, readings, literal, below_prefix |
| `OutsideProjectPlacementResponse` | [note_placement.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_placement.py#L40) | kind, readings, path |
| `WriteNoteRequest` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L11) | note, overwrite, expected_checksum |
| `NoteCreated` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L27) | kind, entity |
| `NoteUpdated` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L32) | kind, entity |
| `NoteAlreadyExists` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L37) | kind, file_path, external_id, permalink |
| `NoteTargetMoved` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L46) | kind, external_id, title, file_path, permalink |
| `NoteLocked` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L54) | kind, message |
| `NoteRevisionConflict` | [note_write.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/note_write.py#L59) | kind, file_path, db_checksum, title, permalink |
| `ProjectIndexStartedResponse` | [project_index.py](https://github.com/basicmachines-co/basic-memory/blob/14ed21b9eaf892b7774c346898981b355fc92dbe/src/basic_memory/schemas/v2/project_index.py#L10) | status, message |
