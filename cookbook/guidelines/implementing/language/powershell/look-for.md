
Review changed PowerShell against [adc.guideline.implementing.language.powershell](cookbook:4842d5fc-f0cc-48a5-b7c8-0be0e2ce2448).

- `must-set-strict-mode`, `must-not-use-strict-mode-latest`, `should-set-strict-mode-at-top`: `Set-StrictMode` is at the top of the script with a named version, not `Latest`.
- `must-stop-on-error-when-failure-must-halt`: `$ErrorActionPreference` is set deliberately. A script that must stop on failure sets `Stop`.
- `must-test-lastexitcode`: External programs have their `$LASTEXITCODE` checked.
- `should-catch-handleable-failures`, `should-clean-up-in-finally`: `try`/`catch` handles only errors the code can act on, and cleanup is in `finally`.
- `must-suppress-unwanted-output`: No stray expression leaks into the success stream (method calls such as `.Add()` are assigned to `$null` or piped to `Out-Null`).
- `must-send-messages-to-message-streams`: Human messages use `Write-Verbose`, `Write-Information` or `Write-Warning`.
- `must-return-a-stable-shape`, `must-not-return-display-text`: Every function returns one consistent shape.
- `must-name-functions-verb-noun`, `must-not-invent-verb-synonyms`, `should-use-singular-nouns`: Functions are `Verb-Noun` with an approved verb and a singular noun. No `Delete-`, `Kill-` or other synonym.
- `must-declare-supports-should-process`, `must-wrap-each-change-in-should-process`, `should-set-high-confirm-impact-when-destructive`: Each function that changes state has `SupportsShouldProcess`, calls `ShouldProcess` before each change, and sets `ConfirmImpact` where it is destructive.
- `should-run-psscriptanalyzer-in-ci`: PSScriptAnalyzer passes.
- `should-follow-shell-script-rules`: functions are small and `main` only calls them, as the shell-script rules ask.
- `should-not-use-reserved-verbs`: a function of the project's own named with `ForEach`, `Ping`, `Sort` or `Tee`.
- `should-prefix-module-nouns`: a module's exported nouns carry its prefix.
