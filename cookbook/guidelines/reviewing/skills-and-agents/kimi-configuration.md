---
id: 5a091e61-8331-4fa0-9214-cb0e142af94f
title: "Kimi configuration"
domain: agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/kimi-configuration
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Kimi configuration changes for skill location and priority, secrets handling, AGENTS.md placement and home-directory assumptions."
platforms:
  - macos
  - linux
  - windows
tags:
  - kimi
  - review
  - llm-tools
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/kimi-configuration
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/skill-checklist
references:
  - https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
  - https://www.kimi.com/en/help/kimi-code/cli-customization
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# Kimi configuration

Review Kimi configuration against [Kimi configuration](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/kimi-configuration).

## Paths

- No script hardcodes `~/.kimi` or `~/.kimi-code`; the location is checked or overridable.

## Secrets

- API keys and base URLs come from the environment variables, not from a checked-in file.

## Skills

- Repository skills are in `.kimi-code/skills/` or `.agents/skills/` under the repository root.
- A new skill name does not shadow a skill at a lower priority level by accident.
- Directory-form skills have `name` and `description` in frontmatter.

## Instructions

- `AGENTS.md` is agent-neutral and placed at the root or in the subdirectory it covers.

## Why this matters

Path and priority mistakes are quiet: the configuration is accepted and ignored. The checklist targets those.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
