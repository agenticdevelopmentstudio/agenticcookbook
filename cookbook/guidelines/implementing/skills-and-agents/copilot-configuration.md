---
id: 4f4ed7a2-a26f-40f2-b863-51715b5c470c
title: "GitHub Copilot configuration"
domain: agenticdevelopercookbook://guidelines/implementing/skills-and-agents/copilot-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Give GitHub Copilot repository instructions through .github/copilot-instructions.md, path-specific instruction files with applyTo globs, AGENTS.md and reusable prompt files."
platforms:
  - macos
  - linux
  - windows
tags:
  - copilot
  - instructions
  - prompt-files
  - llm-tools
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/authoring-skills-and-rules
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/codex-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/kimi-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/context-and-memory-management
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/copilot-configuration
references:
  - https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
  - https://code.visualstudio.com/docs/copilot/customization/prompt-files
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - skill-authoring
  - configuration
---

# GitHub Copilot configuration

GitHub Copilot takes project guidance from files in the repository. Put guidance that applies everywhere in one file, guidance for part of the tree in path-specific files, and repeatable tasks in prompt files.

## Repository-wide instructions

- `.github/copilot-instructions.md` applies to the whole repository. Keep it short: build and test commands, conventions that are not obvious from the code, and what to avoid.
- Pull-request reviews read the instructions from the head branch, so an instruction change takes effect in the pull request that makes it.

## Path-specific instructions

- Put narrower guidance in `.github/instructions/NAME.instructions.md`. Its frontmatter has an `applyTo` glob (several globs are comma-separated) that selects the files it covers.
- Add `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to keep a file away from one of those agents. Without it both use the file.
- Path-specific and repository-wide files are both applied when a file matches, so do not repeat repository-wide rules in a path file.

## Agent instruction files

- Copilot also reads `AGENTS.md`. It may sit anywhere in the repository, and the nearest one to the working file takes precedence.
- A single `CLAUDE.md` or `GEMINI.md` at the repository root is an accepted alternative. Prefer `AGENTS.md`, which is not tied to one tool and can be shared with other agents.

## Precedence

- Personal instructions take precedence over repository instructions, which take precedence over organization instructions. All applicable sets are provided to the model, so contradictory text across sets produces unpredictable behavior. Avoid restating organization policy.

## Prompt files

- A reusable task is a `.github/prompts/NAME.prompt.md` file. Frontmatter keys are `description`, `agent`, `model`, `tools`, `name` and `argument-hint`. The key for the agent is `agent`, not the older `mode`.
- In the body, use `${input:name}` or `${input:name:placeholder}` for values the user supplies and `${selection}` for the selected text.
- Run a prompt with `/<name>` in chat or with the Chat: Run Prompt command.
- Do not give a prompt file the name of a user's own prompt. See [Never overwrite a user's files](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files).

## Why this matters

Copilot's output follows the instructions it can find. Instructions in a personal file help one developer; instructions in the repository help everyone and are reviewed like code. The file names and globs are exact, and a wrong name is silently ignored.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
