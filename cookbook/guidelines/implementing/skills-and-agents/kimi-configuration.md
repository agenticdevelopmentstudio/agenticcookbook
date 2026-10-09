---
id: e858e124-8774-450f-ab7a-9b27a6965660
title: "Kimi configuration"
domain: agenticdevelopercookbook://guidelines/implementing/skills-and-agents/kimi-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Configure Kimi Code through its config.toml, AGENTS.md files and skills directories, using the priority order of project, user, extra and built-in skills."
platforms:
  - macos
  - linux
  - windows
tags:
  - kimi
  - config-toml
  - agents-md
  - skills
  - llm-tools
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/authoring-skills-and-rules
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/codex-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/copilot-configuration
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/skill-structure-reference
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/kimi-configuration
references:
  - https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
  - https://www.kimi.com/en/help/kimi-code/cli-customization
  - https://github.com/MoonshotAI/kimi-cli
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - skill-authoring
  - configuration
---

# Kimi configuration

Kimi Code is configured through a TOML config file, `AGENTS.md` instruction files and skill directories. The sources below disagree on the name of the home directory, so the guideline records both.

## Home directory

- The help-center page on customization names the global configuration `~/.kimi/config.toml` (TOML or JSON), editable with the `/config` command, and a global `~/.kimi/AGENTS.md`.
- The skills documentation names the user skills directory under `$KIMI_CODE_HOME/skills/`, which defaults to `~/.kimi-code/skills/`.
- The archived `kimi-cli` project stores its data in `~/.kimi/`.
- Do not assume one. Check which directory the installed version uses, and let scripts that touch these paths accept an override rather than hardcoding either.

## Configuration

- Project-level configuration overrides global configuration, and startup parameters such as `--system-prompt` override both.
- The environment variables `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL` and `KIMI_MAX_TOKENS` take precedence over the configuration file. Keep the API key in the environment, never in a checked-in file.
- The older command-line tool manages MCP servers with `kimi mcp add`, `list`, `remove` and `auth`, and accepts a `--mcp-config-file` whose top-level key is `mcpServers`.

## AGENTS.md

- An `AGENTS.md` in the project root or any subdirectory is read, and `/init` generates one. A global `~/.kimi/AGENTS.md` applies to all projects.
- Write it as agent-neutral instructions so other tools can share it.

## Skills

- Priority is Project, then User, then Extra, then Built-in. A higher level shadows a lower one of the same name.
- Project skills live in `.kimi-code/skills/` or `.agents/skills/`, relative to the nearest directory containing `.git`. User skills live in `$KIMI_CODE_HOME/skills/` and `~/.agents/skills/`. Extra directories are listed in `extra_skill_dirs` in `config.toml`.
- In a skill directory `name/SKILL.md` wins over `name.md`. Frontmatter fields are `name`, `description` (required for the directory form), `type` (`prompt`, `inline` or `flow`), `whenToUse`, `disableModelInvocation` and `arguments`.
- Invoke a skill with `/skill:<name> args`.
- Prefer `.agents/skills/` for a repository skill that other tools can also discover.

## Why this matters

Kimi resolves the same skill name across four levels and several directories. Without the priority order you cannot tell why one skill shadows another, and without the home-directory caveat a script may write to a directory the tool never reads.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
