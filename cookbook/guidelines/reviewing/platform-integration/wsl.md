---
id: 65eff0b7-14d5-4cd1-8107-1cfda65e78f3
title: "Windows Subsystem for Linux"
domain: agenticdevelopercookbook://guidelines/reviewing/platform-integration/wsl
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review WSL-aware code and configuration for file placement, wslpath use, line endings, permission and case handling, and guarded interop."
platforms:
  - windows
  - linux
tags:
  - wsl
  - windows
  - review
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/wsl
  - agenticdevelopercookbook://guidelines/reviewing/language/powershell
references:
  - https://learn.microsoft.com/en-us/windows/wsl/filesystems
  - https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity
  - https://learn.microsoft.com/en-us/windows/dev-environment/wsl-interop
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - platform-integration
---

# Windows Subsystem for Linux

Review changes that run across Windows and WSL against [Windows Subsystem for Linux](agenticdevelopercookbook://guidelines/implementing/platform-integration/wsl).

## Files and paths

- Linux-tool project files are not placed under `/mnt/c`, and no path hardcodes the automount root.
- Paths cross the boundary through `wslpath`, not string substitution.

## Line endings

- `.gitattributes` fixes line endings per file type. Shell scripts are LF.

## Permissions and case

- Code does not depend on Linux permissions of files on a Windows drive without the `metadata` option.
- No two paths differ only by case.
- Per-directory case-sensitivity changes are intentional and documented.

## Interop

- Windows programs are called with their `.exe` suffix and only after a check that interop is available.
- WSL detection guards every Windows-only command.
- Network addresses are configurable.

## Configuration

- `wsl.conf` and `.wslconfig` changes say which scope they target and require a restart of the distribution.

## Why this matters

Boundary bugs rarely appear on the author's machine. A checklist aimed at the boundary catches them in review.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
