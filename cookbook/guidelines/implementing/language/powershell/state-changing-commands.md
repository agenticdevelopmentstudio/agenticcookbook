
- A command that changes state declares `[CmdletBinding(SupportsShouldProcess)]`, which adds `-WhatIf` and `-Confirm`, and wraps each change in `if ($PSCmdlet.ShouldProcess($target, $action)) { ... }`.
- Set `ConfirmImpact` to `High` for destructive commands so they prompt by default; the default is `Medium`, compared with `$ConfirmPreference`.
- PSScriptAnalyzer enforces this with `UseApprovedVerbs` and `UseShouldProcessForStateChangingFunctions` (state-changing verbs include New, Set, Remove, Start, Stop, Restart, Reset and Update). Run it in CI.

