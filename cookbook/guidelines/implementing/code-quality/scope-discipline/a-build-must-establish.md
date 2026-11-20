
- `should-stay-inside-task-boundary`: every file in the build's diff serves the task, or the build says why not
- `must-state-goal-in-one-sentence`: the build records its goal in one sentence before its first change
- `should-ask-before-assuming-broad-scope`: for an ambiguous or broad request, the build asked before taking broad scope, or says why not
- `should-confirm-repository-for-multi-repo-work`: for multi-repo work, the build confirmed the repository before changing it, or says why not
- `must-modify-only-what-was-requested`: every changed line traces to something the request asked for
- `must-note-but-not-fix-out-of-scope-issues`: the build's report lists each out-of-scope issue it found, and its diff fixes none of them
- `should-watch-for-scope-creep-signals`: the build's diff shows none of the scope-creep signals, or the build says why not
