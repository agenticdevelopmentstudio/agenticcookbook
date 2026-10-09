
- Begin every script and module with `Set-StrictMode -Version 3.0` (or the highest version you have tested). Strict mode is off by default; with it on, reading an uninitialized variable or a property that does not exist is an error instead of `$null`.
- Do not use `-Version Latest` in shared code. `Latest` means the newest strict mode of whatever PowerShell runs the script, so behavior can change when the host is upgraded.
- Strict mode applies to the current scope and its child scopes, so set it at the top of the script, not inside a function that other code calls.

