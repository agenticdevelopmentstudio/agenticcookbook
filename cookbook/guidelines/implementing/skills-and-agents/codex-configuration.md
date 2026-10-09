---
id: e8870c2b-ae55-4e48-a4e7-081d65f27418
title: "Codex configuration"
domain: agenticdevelopercookbook://guidelines/implementing/skills-and-agents/codex-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Configure Codex through config.toml layers, AGENTS.md discovery, skills directories and, for older setups, custom prompts, keeping repository instructions in files that travel with the repository."
platforms:
  - macos
  - linux
  - windows
tags:
  - codex
  - config-toml
  - agents-md
  - skills
  - prompts
  - llm-tools
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/authoring-skills-and-rules
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/skill-structure-reference
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/context-and-memory-management
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/copilot-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/kimi-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/codex-configuration
references:
  - https://learn.chatgpt.com/docs/agent-configuration/agents-md
  - https://learn.chatgpt.com/docs/build-skills
  - https://learn.chatgpt.com/docs/config-file/config-basic
  - https://learn.chatgpt.com/docs/custom-prompts.md
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - skill-authoring
  - configuration
---

# Codex configuration

Codex reads three kinds of configuration: settings in `config.toml`, instructions in `AGENTS.md`, and reusable procedures in skills. Put each kind in the place Codex looks for it, and keep what the team shares inside the repository.

## config.toml

- User settings live in `~/.codex/config.toml`. The Codex home directory defaults to `~/.codex` and can be moved with the `CODEX_HOME` environment variable.
- Project settings live in `.codex/config.toml` inside the repository. Codex loads a project's file only when the project is trusted, so a setting that must apply on every machine cannot depend on an untrusted checkout.
- Precedence, strongest first: command-line flags and `--config` overrides, project configuration (the closest file wins), a named profile file (`~/.codex/<name>.config.toml`, selected with `--profile`), the user file, cloud-managed defaults, `/etc/codex/config.toml`, and the built-in defaults.
- Typical keys are `model`, `approval_policy` (for example `"on-request"`) and `sandbox_mode` (for example `"workspace-write"`). Check a key against the configuration reference before using it; do not copy keys from another tool.
- Do not store secrets in a checked-in `config.toml`.

## AGENTS.md

- Global instructions come from the Codex home: Codex reads `AGENTS.override.md` if it exists, otherwise `AGENTS.md`, and uses the first non-empty file only.
- Project instructions are collected by walking from the project root down to the working directory. In each directory Codex checks `AGENTS.override.md`, then `AGENTS.md`, then any names listed in `project_doc_fallback_filenames`, and takes at most one file per directory. The files are concatenated from the root down, so a file closer to the working directory overrides a farther one.
- The combined size is limited by `project_doc_max_bytes`, which defaults to 32 KiB. Keep each file short and move reference material into skills, which load on demand.
- Write `AGENTS.md` as instructions for any agent, not for one tool, so other tools can read the same file.

## Skills

- A skill is a directory with a `SKILL.md` whose frontmatter has a `name` and a `description`. The description is what Codex uses to decide when the skill applies, so write it as a trigger.
- Skills are discovered in these places: repository skills in `.agents/skills`, scanned from the working directory up to the repository root; user skills in `$HOME/.agents/skills`; administrator skills in `/etc/codex/skills`; and bundled system skills.
- An optional `agents/openai.yaml` in the skill directory sets invocation policy. `allow_implicit_invocation: false` stops Codex from choosing the skill on its own.
- Disable a skill without deleting it with a `[[skills.config]]` entry in `~/.codex/config.toml`, and restart Codex.
- Follow [Skill structure reference](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/skill-structure-reference) for the contents of `SKILL.md`, and [Never overwrite a user's files](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files) when installing one.

## Custom prompts

- Custom prompts are deprecated in favor of skills. Do not write new ones unless a skill cannot express the need.
- Existing prompts are Markdown files directly in `~/.codex/prompts/` (subdirectories are not scanned). They are per-user, so they cannot be shared through the repository. Frontmatter supports `description` and `argument-hint`, and a prompt runs as `/prompts:<name>`.
- Migrate a prompt that the team uses to a repository skill so it is versioned with the code.

## Why this matters

Codex merges several layers, and the layer a setting sits in decides who gets it. Instructions placed in a user-only file never reach teammates; settings placed in an untrusted project file never load. Knowing the discovery order lets you put each thing where it takes effect.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
