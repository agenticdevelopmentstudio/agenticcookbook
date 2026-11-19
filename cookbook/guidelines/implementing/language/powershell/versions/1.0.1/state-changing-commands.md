
- A command that changes state MUST declare `[CmdletBinding(SupportsShouldProcess)]`, which adds `-WhatIf` and `-Confirm`, and MUST wrap each change in `if ($PSCmdlet.ShouldProcess($target, $action)) { ... }`.
- Destructive commands SHOULD set `ConfirmImpact` to `High` so they prompt by default; the default is `Medium`, compared with `$ConfirmPreference`.
- PSScriptAnalyzer enforces this with `UseApprovedVerbs` and `UseShouldProcessForStateChangingFunctions` (state-changing verbs include New, Set, Remove, Start, Stop, Restart, Reset and Update). CI SHOULD run it.

