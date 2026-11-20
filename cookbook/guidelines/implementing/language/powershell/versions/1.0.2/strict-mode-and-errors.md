
- `Set-StrictMode` is at the top of the script with a named version, not `Latest`.
- `$ErrorActionPreference` is set deliberately. A script that must stop on failure sets `Stop`.
- External programs have their `$LASTEXITCODE` checked.
- `try`/`catch` handles only errors the code can act on, and cleanup is in `finally`.

