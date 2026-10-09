---
id: 8017637b-8eae-4829-b5a3-85560f7f8fb8
title: "Codex configuration"
domain: agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/codex-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Codex configuration changes for the right layer, AGENTS.md size and placement, skill location and invocation policy, and removal of custom prompts."
platforms:
  - macos
  - linux
  - windows
tags:
  - codex
  - review
  - llm-tools
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/codex-configuration
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/skill-checklist
references:
  - https://learn.chatgpt.com/docs/agent-configuration/agents-md
  - https://learn.chatgpt.com/docs/build-skills
  - https://learn.chatgpt.com/docs/config-file/config-basic
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# Codex configuration

Review Codex configuration against [Codex configuration](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/codex-configuration).

## config.toml

- Each setting is in the layer that reaches the people who need it: shared settings in `.codex/config.toml`, personal ones in `~/.codex/config.toml`.
- Every key exists in the configuration reference.
- No secret is checked in.

## AGENTS.md

- Instructions are agent-neutral and short enough that the combined files stay under `project_doc_max_bytes`.
- Nested files add to the parent rather than repeat it. An `AGENTS.override.md` has a reason.

## Skills

- Repository skills live under `.agents/skills`. `SKILL.md` has a `name` and a trigger-style `description`.
- `allow_implicit_invocation: false` is set for skills that must run only on request.

## Prompts

- No new custom prompt. A prompt the team relies on is converted to a skill.

## Why this matters

Configuration review is mostly about placement. The checklist makes the placement question the first thing asked.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
