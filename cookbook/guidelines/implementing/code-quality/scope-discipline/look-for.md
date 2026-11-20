
- `should-stay-inside-task-boundary`: a change whose diff reaches past the task's boundary
- `must-state-goal-in-one-sentence`: work begun with no one-sentence statement of its goal
- `should-ask-before-assuming-broad-scope`: an ambiguous or broadly readable request taken at its broadest without a question first
- `should-confirm-repository-for-multi-repo-work`: changes made in one repository of a multi-repo task with no confirmation that it was the intended one
- `must-modify-only-what-was-requested`: a bug fix that also refactors surrounding code, adds tests for unrelated functions, updates docs for other features or "improves" adjacent components
- `must-note-but-not-fix-out-of-scope-issues`: an out-of-scope issue (broken import, outdated comment, missing error handling) fixed in the change, or found and never reported to the user
- `should-watch-for-scope-creep-signals`: any of the signals in the diff — unrelated files touched, unrequested functionality, refactors of working code, a redesign for a one-behavior fix, more than the minimum files changed
