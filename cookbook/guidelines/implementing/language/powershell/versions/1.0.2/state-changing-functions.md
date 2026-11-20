
- Each function that changes state has `SupportsShouldProcess`, calls `ShouldProcess` before each change, and sets `ConfirmImpact` where it is destructive.
- PSScriptAnalyzer passes.

