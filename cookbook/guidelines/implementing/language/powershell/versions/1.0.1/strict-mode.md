
- Every script and module MUST begin with `Set-StrictMode -Version 3.0` (or the highest version you have tested). Strict mode is off by default; with it on, reading an uninitialized variable or a property that does not exist is an error instead of `$null`.
- Shared code MUST NOT use `-Version Latest`. `Latest` means the newest strict mode of whatever PowerShell runs the script, so behavior can change when the host is upgraded.
- Strict mode applies to the current scope and its child scopes, so it SHOULD be set at the top of the script, not inside a function that other code calls.

