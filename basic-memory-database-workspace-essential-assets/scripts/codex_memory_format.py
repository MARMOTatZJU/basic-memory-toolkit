#!/usr/bin/env python3
"""Build a Basic Memory corpus from captured Codex conversation exports."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import re
import shutil
from typing import Any

import yaml

PINNED_COMMIT = "c9bd187b83baba549d5cd16bacc180f8023d51c8"
LOCAL_TZ = timezone(timedelta(hours=8))

TOPICS = {
    "memory-agent-infrastructure": {
        "title": "Memory, Skills, and Agent Infrastructure",
        "summary": "Conversation memory, Notion access, Codex skills, context systems, and agent harnesses.",
        "keywords": ["basic memory", "notion", "skill", "context", "memory", "agentic", "codex", "deepseek", "harness", "asd-ste100", "conversation summary"],
    },
    "software-repositories": {
        "title": "Software Engineering and Repository Work",
        "summary": "Repository analysis, installation, code reports, system setup, Git, drivers, and runtime work.",
        "keywords": ["repo", "repository", "code", "install", "git", "wifi", "driver", "runtime", "laya", "muse", "reinstall", "baseline tests"],
    },
    "research-and-papers": {
        "title": "Research Papers and Technical Surveys",
        "summary": "Academic papers, engineering surveys, research directions, and evidence reviews.",
        "keywords": ["paper", "arxiv", "survey", "research", "literature", "jev engineering", "proximal gradient", "近端梯度"],
    },
    "health-and-performance": {
        "title": "Health, Biomechanics, and Human Performance",
        "summary": "Health questions, biomechanics, pain, muscle recovery, training, and athletic performance.",
        "keywords": ["muscle", "pain", "wrist", "pronator", "dental", "plyometric", "cycling", "肌群", "疼痛", "腕关节", "恢复", "旋前圆肌", "腓骨", "训练"],
    },
    "motorcycle-and-control": {
        "title": "Motorcycles, Control, and Driving",
        "summary": "Motorcycle technique, control systems, tracking delay, braking, and related mechanics.",
        "keywords": ["motorcycle", "braking", "dirt bike", "control", "tracking", "frequency", "摩托", "拮抗", "频域", "时滞", "油门", "后刹"],
    },
    "general-analysis": {
        "title": "General Analysis and Workspace Tasks",
        "summary": "Workspace tasks and analyses that do not fit one specialized topic.",
        "keywords": [],
    },
}

SUMMARY_OVERRIDES = {
    "01a15c37-59d6-7933-b90c-6818dabb75c7":
        "Review the laya code and documentation. Write Markdown reports in laya-code/code-report.",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def yaml_frontmatter(metadata: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(
        metadata, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120
    ).rstrip() + "\n---\n\n"


def iso_from_epoch(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value, timezone.utc).astimezone(LOCAL_TZ).isoformat()


def chronological_turns(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    for page in reversed(snapshot.get("pages", [])):
        turns.extend(reversed(page.get("turns", [])))
    return turns


def message_text(item: dict[str, Any]) -> str:
    if item.get("type") == "agentMessage":
        return str(item.get("text", ""))
    values: list[str] = []
    for block in item.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            values.append(str(block.get("text", "")))
        else:
            values.append(json.dumps(block, ensure_ascii=False, sort_keys=True))
    return "\n\n".join(values)


def message_payload(item: dict[str, Any]) -> str:
    if item.get("type") == "agentMessage":
        return str(item.get("text", ""))
    return json.dumps(item.get("content", []), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def choose_fence(text: str, minimum: int = 4) -> str:
    runs = [len(value) for value in re.findall(r"`+", text)]
    return "`" * max(minimum, (max(runs) + 1) if runs else minimum)


def clean_excerpt(text: str, limit: int = 700) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    if len(value) <= limit:
        return value
    cut = value[:limit].rsplit(" ", 1)[0].rstrip(".,;: ")
    return cut + "…"


def select_topic(title: str, summary: str) -> str:
    haystack = (title + "\n" + summary).casefold()
    scores = {
        key: sum(1 for word in topic["keywords"] if word.casefold() in haystack)
        for key, topic in TOPICS.items()
    }
    best = max((key for key in TOPICS if key != "general-analysis"), key=lambda key: scores[key])
    return best if scores[best] else "general-analysis"


def extract_artifacts(texts: list[str], commands: list[str]) -> list[str]:
    candidates: list[str] = []
    patterns = [r"/mnt/[A-Za-z0-9_./+\- ]+", r"[A-Za-z]:/[A-Za-z0-9_./+\- ]+"]
    for text in [*texts, *commands]:
        for pattern in patterns:
            for match in re.findall(pattern, text):
                value = match.strip().rstrip(".,:;)]}>")
                if len(value) > 8 and value not in candidates:
                    candidates.append(value)
    return candidates[:30]


def format_message(item: dict[str, Any], turn: dict[str, Any], index: int) -> str:
    role = "User" if item.get("type") == "userMessage" else "AI agent"
    details = [role, str(item.get("id", f"message-{index}"))]
    if item.get("phase"):
        details.append(str(item["phase"]))
    if turn.get("startedAt"):
        details.append(str(turn["startedAt"]))
    return f"### {' | '.join(details)}\n\n{message_text(item)}\n"


def format_trace_event(item: dict[str, Any], turn: dict[str, Any], index: int) -> str:
    event = dict(item)
    event["turn_id"] = turn.get("id")
    event["turn_started_at"] = turn.get("startedAt")
    return f"### Event {index}: {item.get('type', 'unknown')}\n\n" + json.dumps(
        event, ensure_ascii=False, indent=2, sort_keys=False
    ) + "\n"


def slug(value: str) -> str:
    value = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", value, flags=re.UNICODE).strip("-").lower()
    return value[:70].rstrip("-") or "conversation"


def conversation_record(snapshot: dict[str, Any], source_path: Path) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    entry = snapshot["threadListEntry"]
    turns = chronological_turns(snapshot)
    messages: list[tuple[dict[str, Any], dict[str, Any]]] = []
    trace_events: list[tuple[dict[str, Any], dict[str, Any]]] = []
    reasoning_markers = 0
    for turn in turns:
        for item in turn.get("items", []):
            if item.get("type") in {"userMessage", "agentMessage"}:
                messages.append((item, turn))
            elif item.get("type") == "reasoningBoundary":
                reasoning_markers += 1
            else:
                trace_events.append((item, turn))

    user_texts = [message_text(item) for item, _ in messages if item.get("type") == "userMessage"]
    agent_items = [item for item, _ in messages if item.get("type") == "agentMessage"]
    final_items = [item for item in agent_items if item.get("phase") == "final_answer"]
    latest_result = message_text(final_items[-1]) if final_items else (message_text(agent_items[-1]) if agent_items else "")
    status = "active" if entry.get("status") == "active" else ("complete" if messages and messages[-1][0].get("phase") == "final_answer" else ("interrupted" if messages else "unknown"))
    title = str(entry.get("title") or entry.get("summary") or entry["id"])
    summary = SUMMARY_OVERRIDES.get(entry["id"], str(entry.get("summary") or title))
    topic_key = select_topic(title, summary)
    topic = TOPICS[topic_key]

    commands = [str(item.get("command", "")) for item, _ in trace_events if item.get("type") == "commandExecution"]
    agent_texts = [message_text(item) for item in agent_items]
    artifacts = extract_artifacts(user_texts + agent_texts, commands)
    event_counts = Counter(item.get("type", "unknown") for item, _ in trace_events)

    transcript = "\n".join(
        format_message(item, turn, index)
        for index, (item, turn) in enumerate(messages, 1)
    )
    transcript_fence = choose_fence(transcript)
    trace = "\n".join(
        format_trace_event(item, turn, index)
        for index, (item, turn) in enumerate(trace_events, 1)
    )
    trace_fence = choose_fence(trace)

    message_manifest: list[dict[str, Any]] = []
    for sequence, (item, turn) in enumerate(messages, 1):
        payload = message_payload(item)
        message_manifest.append({
            "sequence": sequence,
            "id": item.get("id"),
            "role": "user" if item.get("type") == "userMessage" else "assistant",
            "phase": item.get("phase"),
            "turn_id": turn.get("id"),
            "sha256": sha256_bytes(payload.encode("utf-8")),
            "characters": len(payload),
        })

    evidence_hash = sha256_bytes(source_path.read_bytes())
    metadata = {
        "title": title,
        "type": "conversation",
        "permalink": f"conversations/{entry['id']}",
        "tags": ["codex-conversation", "aicodingworkspace", topic_key],
        "thread_id": entry["id"],
        "source_kind": "codex",
        "workspace": "AICodingWorkspace",
        "source_status": "unarchived",
        "conversation_status": entry.get("status"),
        "continuation_status": status,
        "created_at": iso_from_epoch(entry.get("createdAt")),
        "updated_at": iso_from_epoch(entry.get("updatedAt")),
        "captured_at": snapshot.get("capturedAt"),
        "summary_method": "exact-message-transcript-plus-extractive-continuation-brief",
        "original_evidence": {"path": str(source_path), "sha256": evidence_hash},
    }
    metadata = {key: value for key, value in metadata.items() if value is not None}

    current_state = (
        "The conversation has a final answer. Verify current files before you extend the work."
        if status == "complete"
        else "The conversation has no final answer. Read the recent messages and verify current files before you continue."
    )
    artifact_lines = "\n".join(f"- `{path}`" for path in artifacts) or "- No explicit file path was found in the message text."
    event_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(event_counts.items())) or "- No operational event was recorded."
    if latest_result:
        result_excerpt = latest_result
        result_fence = choose_fence(result_excerpt)
        result_lines = f"{result_fence}source-excerpt\n{result_excerpt}\n{result_fence}"
    else:
        result_lines = "No agent result was recorded."

    last_request = user_texts[-1] if user_texts else "No user request returned."
    last_progress = message_text(agent_items[-1]) if agent_items else "No agent progress returned."
    request_fence = choose_fence(last_request)
    progress_fence = choose_fence(last_progress)
    body = f"""# {title}

## Continuation brief

{summary}

- Conversation state: **{status}**
- Source state: **unarchived**
- User messages: **{len(user_texts)}**
- AI agent messages: **{len(agent_items)}**
- Observable operational events: **{len(trace_events)}**

{current_state}

### Latest user request

{request_fence}source-excerpt
{last_request}
{request_fence}

### Latest visible progress

{progress_fence}source-excerpt
{last_progress}
{progress_fence}

### Latest reported result

{result_lines}

### Referenced artifacts

{artifact_lines}

### Operational coverage

{event_lines}

## Observations

- [summary] {summary}
- [source_thread_id] {entry['id']}
- [source_status] unarchived
- [continuation_status] {status}
- [message_count] {len(messages)}
- [limitation] Available tool-output bodies are preserved. Consult registry/sync-coverage.json for truncation and fallback limits.
- [limitation] Private internal reasoning is not exported. Observable decisions, messages, commands, tool calls, and file changes remain available.
- [writing_status] Extractive continuation brief. Exact source messages retain their original wording and language.

## Source transcript

The transcript preserves every user message and AI agent message returned by the local chat source.

{transcript_fence}conversation-transcript
{transcript}{transcript_fence}

## Observable execution trace

This trace preserves source events that support task continuation. Output limits and any omitted bodies are recorded in registry/sync-coverage.json.

{trace_fence}jsonl
{trace}{trace_fence}

## Relations

- part_of [[Codex Memory Overview]]
- categorized_as [[{topic['title']}]]
"""
    record = yaml_frontmatter(metadata) + body
    for item, _ in messages:
        text = message_text(item)
        if text and text not in record:
            raise AssertionError(f"Message content missing from record {entry['id']}: {item.get('id')}")
    stats = {
        "id": entry["id"],
        "title": title,
        "summary": summary,
        "topic": topic_key,
        "status": status,
        "turns": len(turns),
        "messages": len(messages),
        "user_messages": len(user_texts),
        "assistant_messages": len(agent_items),
        "trace_events": len(trace_events),
        "reasoning_markers": reasoning_markers,
        "source_sha256": evidence_hash,
        "record_sha256": sha256_bytes(record.encode("utf-8")),
        "artifacts": artifacts,
    }
    return record, stats, message_manifest

