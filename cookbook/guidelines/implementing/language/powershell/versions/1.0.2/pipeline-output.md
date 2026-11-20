
- Every statement that produces a value writes it to the success output stream, whether or not it uses `return`. A stray method call that returns a value (for example `$list.Add($x)`) silently becomes part of the function's output.
- Unwanted output MUST be suppressed with `$null = ...` or `| Out-Null`, or with a redirection such as `> $null`. Messages for people MUST go to `Write-Verbose`, `Write-Information` or `Write-Warning`, never to the success stream.
- A function MUST return a stable shape: either objects, or nothing. It MUST NOT return text meant for display.
- Each stream has a number and redirects with `n>`: for example `2>&1` merges errors into the success stream. In PowerShell 7.4 and later, redirecting a native command's output passes bytes through unchanged.

