
- No stray expression leaks into the success stream (method calls such as `.Add()` are assigned to `$null` or piped to `Out-Null`).
- Human messages use `Write-Verbose`, `Write-Information` or `Write-Warning`.
- Every function returns one consistent shape.

