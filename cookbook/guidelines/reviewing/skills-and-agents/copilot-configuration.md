---
id: 706a3bf7-0fe1-4b12-b4da-0fd8d363b314
title: "GitHub Copilot configuration"
domain: agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/copilot-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review GitHub Copilot instruction and prompt files for correct names, applyTo globs, agent exclusions and non-duplicated guidance."
platforms:
  - macos
  - linux
  - windows
tags:
  - copilot
  - review
  - llm-tools
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/copilot-configuration
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/skill-checklist
references:
  - https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
  - https://code.visualstudio.com/docs/copilot/customization/prompt-files
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# GitHub Copilot configuration

Review Copilot configuration against [GitHub Copilot configuration](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/copilot-configuration).

## Files and names

- Repository-wide guidance is `.github/copilot-instructions.md`. Path-specific files end in `.instructions.md` and live in `.github/instructions/`. Prompt files end in `.prompt.md` and live in `.github/prompts/`.
- A repository does not carry both an `AGENTS.md` and a `CLAUDE.md` or `GEMINI.md` with different content.

## Instruction content

- Each path-specific file has an `applyTo` glob that matches the files it intends.
- `excludeAgent` is set only on purpose.
- Guidance is not duplicated between the repository-wide file and path files.

## Prompt files

- Frontmatter uses `agent` rather than `mode`.
- Variables use the `${input:...}` and `${selection}` forms.
- The prompt name does not collide with an existing one.

## Why this matters

A misnamed instruction file does nothing and gives no error. Checking names and globs first prevents that quiet failure.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
