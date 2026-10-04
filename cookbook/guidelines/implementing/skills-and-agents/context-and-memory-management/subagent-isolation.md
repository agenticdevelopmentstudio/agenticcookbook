
| Use a subagent when... | Keep in main context when... |
|---|---|
| Exploring many files to answer one question | The result must stay live for ongoing editing |
| Verifying/reviewing a diff in a fresh context | The history itself is the work product |
| Running a noisy, token-heavy investigation | The subtask is a single cheap lookup |

- A subagent **MUST** return a condensed summary (findings, file paths, decisions) — not raw dumps of everything it read.
- The caller **MUST NOT** assume the subagent's intermediate context is available afterward; only the returned summary survives.

