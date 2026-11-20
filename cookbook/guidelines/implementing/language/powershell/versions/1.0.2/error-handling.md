
- `$ErrorActionPreference` defaults to `Continue`: a non-terminating error is reported and the script keeps going. A script that must not continue after a failure MUST set `$ErrorActionPreference = 'Stop'` at the top, and MAY override it for one command with `-ErrorAction`.
- Work whose failure you can handle SHOULD be wrapped in `try`/`catch`, and cleanup SHOULD use `finally`.
- Native commands do not follow `$ErrorActionPreference` by default; `$PSNativeCommandUseErrorActionPreference` is `$false`. After running an external program, code MUST test `$LASTEXITCODE` explicitly.

