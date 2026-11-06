---
title: Task
type: schema
permalink: schema/task
tags: [schema, task]
entity: Task
version: 1
schema:
  description: string, what needs to be done
  status?(enum, current state): [active, blocked, done, abandoned]
  assigned_to?: string, who is working on this
  steps?(array): string, ordered steps to complete
  current_step?: integer, which step number we're on (1-indexed)
  context?: string, key context needed to resume after memory loss
  started?: string, when work began
  completed?: string, when work finished
  blockers?(array): string, what's preventing progress
  parent_task?: Task, parent task if this is a subtask
settings:
  validation: warn
---

# Task

This Task schema is a copy from the Basic Memory v1.0.0 memory-tasks skill. Its source commit is `c9bd187b83baba549d5cd16bacc180f8023d51c8`.
