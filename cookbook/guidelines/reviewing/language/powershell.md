---
id: ce0c62c0-f2a1-4b60-b46e-844adc164d92
title: "PowerShell"
domain: agenticdevelopercookbook://guidelines/reviewing/language/powershell
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review PowerShell for strict mode, error preference, clean pipeline output, approved verbs and ShouldProcess on state-changing functions."
platforms:
  - windows
  - macos
  - linux
languages:
  - powershell
tags:
  - language
  - powershell
  - review
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/powershell
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/shell-scripts
references:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-strictmode
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables
  - https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# PowerShell

Review changed PowerShell against [PowerShell](agenticdevelopercookbook://guidelines/implementing/language/powershell).

## Strict mode and errors

- `Set-StrictMode` is at the top of the script with a named version, not `Latest`.
- `$ErrorActionPreference` is set deliberately. A script that must stop on failure sets `Stop`.
- External programs have their `$LASTEXITCODE` checked.
- `try`/`catch` handles only errors the code can act on, and cleanup is in `finally`.

## Output

- No stray expression leaks into the success stream (method calls such as `.Add()` are assigned to `$null` or piped to `Out-Null`).
- Human messages use `Write-Verbose`, `Write-Information` or `Write-Warning`.
- Every function returns one consistent shape.

## Naming

- Functions are `Verb-Noun` with an approved verb and a singular noun. No `Delete-`, `Kill-` or other synonym.

## State-changing functions

- Each function that changes state has `SupportsShouldProcess`, calls `ShouldProcess` before each change, and sets `ConfirmImpact` where it is destructive.
- PSScriptAnalyzer passes.

## Why this matters

Leaked output and silent `$null` reads are invisible in a diff and costly in production. The checklist names the places to look.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
