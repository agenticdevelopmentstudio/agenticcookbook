---
id: 4842d5fc-f0cc-48a5-b7c8-0be0e2ce2448
title: "PowerShell"
domain: agenticdevelopercookbook://guidelines/implementing/language/powershell
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-10-09
modified: 2026-11-07
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Write PowerShell with strict mode, a deliberate error preference, clean pipeline output, approved verbs and ShouldProcess support for state-changing commands."
platforms:
  - windows
  - macos
  - linux
languages:
  - powershell
tags:
  - language
  - powershell
  - strict-mode
  - pipeline
  - approved-verbs
  - shouldprocess
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/wsl
  - agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
  - agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files
  - agenticdevelopercookbook://guidelines/reviewing/language/powershell
  - agenticdevelopercookbook://principles/fail-fast
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-strictmode
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_return
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/out-null
  - https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_cmdletbindingattribute
  - https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs
  - https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useshouldprocessforstatechangingfunctions
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - error-handling
  - configuration
---

# PowerShell

PowerShell scripts and modules in this cookbook's projects follow the rules below. The general script rules in [Shell scripts](agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts) (small functions, a `main` that only calls) apply here too.

## Strict mode

- Every script and module MUST begin with `Set-StrictMode -Version 3.0` (or the highest version you have tested). Strict mode is off by default; with it on, reading an uninitialized variable or a property that does not exist is an error instead of `$null`.
- Shared code MUST NOT use `-Version Latest`. `Latest` means the newest strict mode of whatever PowerShell runs the script, so behavior can change when the host is upgraded.
- Strict mode applies to the current scope and its child scopes, so it SHOULD be set at the top of the script, not inside a function that other code calls.

## Error handling

- `$ErrorActionPreference` defaults to `Continue`: a non-terminating error is reported and the script keeps going. A script that must not continue after a failure MUST set `$ErrorActionPreference = 'Stop'` at the top, and MAY override it for one command with `-ErrorAction`.
- Work whose failure you can handle SHOULD be wrapped in `try`/`catch`, and cleanup SHOULD use `finally`.
- Native commands do not follow `$ErrorActionPreference` by default; `$PSNativeCommandUseErrorActionPreference` is `$false`. After running an external program, code MUST test `$LASTEXITCODE` explicitly.

## Pipeline output

- Every statement that produces a value writes it to the success output stream, whether or not it uses `return`. A stray method call that returns a value (for example `$list.Add($x)`) silently becomes part of the function's output.
- Unwanted output MUST be suppressed with `$null = ...` or `| Out-Null`, or with a redirection such as `> $null`. Messages for people MUST go to `Write-Verbose`, `Write-Information` or `Write-Warning`, never to the success stream.
- A function MUST return a stable shape: either objects, or nothing. It MUST NOT return text meant for display.
- Each stream has a number and redirects with `n>`: for example `2>&1` merges errors into the success stream. In PowerShell 7.4 and later, redirecting a native command's output passes bytes through unchanged.

## Naming and verbs

- Functions MUST be named `Verb-Noun` with a verb from the approved list (`Get-Verb` prints it). Use `Remove`, not `Delete`; code MUST NOT invent synonyms. The verbs `ForEach`, `Ping`, `Sort` and `Tee` are reserved for built-in commands.
- Nouns SHOULD be singular, and a module SHOULD use a prefix so names do not collide.

## State-changing commands

- A command that changes state MUST declare `[CmdletBinding(SupportsShouldProcess)]`, which adds `-WhatIf` and `-Confirm`, and MUST wrap each change in `if ($PSCmdlet.ShouldProcess($target, $action)) { ... }`.
- Destructive commands SHOULD set `ConfirmImpact` to `High` so they prompt by default; the default is `Medium`, compared with `$ConfirmPreference`.
- PSScriptAnalyzer enforces this with `UseApprovedVerbs` and `UseShouldProcessForStateChangingFunctions` (state-changing verbs include New, Set, Remove, Start, Stop, Restart, Reset and Update). CI SHOULD run it.

## Why this matters

PowerShell's defaults favor an interactive session: errors keep going, typos in variable names are `$null`, and any expression leaks into output. Strict mode, a Stop preference and disciplined output turn the same script into one that fails where the mistake is, and `-WhatIf` lets a person see a destructive change before it happens.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-11-07 | Mike Fullerton | State the rules with RFC 2119 keywords |
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
