---
id: 0f999db4-956a-4124-a142-367b1a570983
title: "Context and memory management for agents"
domain: agenticdevelopercookbook://guidelines/implementing/skills-and-agents/context-and-memory-management
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Treat context as a finite budget you curate: prune aggressively, isolate large subtasks to subagents, and persist what must survive across sessions."
platforms: []
tags:
  - agents
  - context
  - ai-workflow
depends-on: []
related:
  - agenticdevelopercookbook://principles/simplicity
  - agenticdevelopercookbook://principles/tight-feedback-loops
references:
  - https://code.claude.com/docs/en/best-practices
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - skill-authoring
---

# Context and memory management for agents

Context engineering is the central reliability discipline for agents: what the model knows *at the moment of action* determines output quality. More tokens are not better — performance degrades as the window fills, and irrelevant history actively distracts the model. Curate context as a finite budget, not a log.

## Core requirements

- The agent **MUST** treat the context window as a finite, actively curated budget — not an append-only transcript.
- The agent **MUST NOT** front-load context "just in case." Retrieve files, tool output, and references just-in-time, at the point they are needed.
- Large or read-heavy subtasks (codebase exploration, multi-file investigation, log analysis) **SHOULD** be delegated to a subagent that runs in an isolated context and returns only a condensed summary.
- The agent **SHOULD** clear or reset context between unrelated tasks rather than carrying stale history forward.
- Information that must outlive the current window (decisions, conventions, task state) **MUST** be written to a persistent memory file, not relied upon to survive in-conversation.

## Compaction is lossy — protect critical state

When context approaches its limit, harnesses summarize older history (compaction). Summaries discard detail, so anything not explicitly preserved can vanish silently.

- Before a compaction is likely, the agent **MUST** ensure the **list of modified files** and the **test/run/build commands** are recorded somewhere durable (a memory file or compaction directive), so they survive the summary.
- The agent **SHOULD** assume compaction loses specifics: exact line numbers, intermediate reasoning, and raw tool output are not guaranteed to persist.
- Where the harness supports it, the agent **SHOULD** declare compaction-preservation directives (e.g. "when compacting, always keep the full modified-file list and test commands").

## Subagent isolation

| Use a subagent when... | Keep in main context when... |
|---|---|
| Exploring many files to answer one question | The result must stay live for ongoing editing |
| Verifying/reviewing a diff in a fresh context | The history itself is the work product |
| Running a noisy, token-heavy investigation | The subtask is a single cheap lookup |

- A subagent **MUST** return a condensed summary (findings, file paths, decisions) — not raw dumps of everything it read.
- The caller **MUST NOT** assume the subagent's intermediate context is available afterward; only the returned summary survives.

## Persistent memory across sessions

- Cross-session continuity (plans, conventions, in-progress task state) **MUST** live in a persistent file the agent re-reads at session start, since the context window does not persist between sessions.
- Memory files **MUST** stay concise and high-signal. An overstuffed memory file dilutes attention and causes the agent to ignore the rules that matter — keep only what changes behavior, and prune regularly.
- The agent **MUST NOT** duplicate information the model can cheaply re-derive (e.g. file contents, standard conventions) into memory; store only what cannot be inferred.

## Pruning between tasks

- On switching to an unrelated task, the agent **SHOULD** reset context so prior files and tool output do not bias the new work.
- After repeated failed correction attempts on one problem, the agent **SHOULD** clear the polluted context and restart from a sharper prompt rather than layering more corrections — failed approaches in-window degrade subsequent reasoning.

> Note: larger context windows (forecast to keep growing) raise the threshold at which curation becomes urgent, but do not remove the degradation-with-fill effect. Treat a bigger window as more headroom, not a license to stop curating — this is a durable property, not a vendor-specific number.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
