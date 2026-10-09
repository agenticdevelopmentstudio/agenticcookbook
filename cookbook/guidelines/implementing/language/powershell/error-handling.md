
- `$ErrorActionPreference` defaults to `Continue`: a non-terminating error is reported and the script keeps going. Set `$ErrorActionPreference = 'Stop'` at the top of a script that must not continue after a failure, and override it for one command with `-ErrorAction`.
- Wrap work whose failure you can handle in `try`/`catch`, and use `finally` for cleanup.
- Native commands do not follow `$ErrorActionPreference` by default; `$PSNativeCommandUseErrorActionPreference` is `$false`. After running an external program, test `$LASTEXITCODE` explicitly.

