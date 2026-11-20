
- `should-make-one-logical-change-per-commit`: each commit holds one logical change, or the commit says why not
- `may-touch-multiple-files-for-one-concept`: every multi-file commit touches only files of the same concept
- `should-commit-as-work-progresses`: the commits were made as work progressed, or the branch says why not
- `should-not-batch-unrelated-changes`: no commit batches unrelated changes, or the commit says why
- `should-build-every-logical-change`: each logical change was built with the platform build command, or the branch says why not
- `must-pass-build-and-tests-before-commit`: at every commit the build passes and existing tests still pass
- `should-commit-each-passing-change`: each passing change was committed with a descriptive message before the next began, or the branch says why not
- `must-not-stack-uncommitted-changes`: no commit is the product of multiple stacked uncommitted changes
- `should-fix-broken-build-before-moving-on`: no change was added on top of a broken build state, or the branch says why
- `should-plan-small-prs-before-coding`: the work was split into small, independently reviewable PRs, or the PR says why not
- `should-split-large-planned-units`: no planned unit of work that looked large was left as one large PR, or the PR says why
- `should-scrutinize-agent-code-more`: agent-generated code received at least the per-line scrutiny hand-written code gets
- `should-decompose-large-agent-changes-before-review`: every large agent-produced change was decomposed into smaller commits or PRs before review, or the PR says why not
- `should-make-one-logical-change-per-commit`: Each commit contains exactly one logical change; no compound diffs mixing unrelated changes; commit message describes the change in isolation.
- `should-bump-version-in-same-change`: Every VERSION HYGIENE lead in the slice was either confirmed against a repo convention and folded into the single finding, or explicitly cleared as trivial/no-convention.
- `should-match-version-bump-magnitude`: version fields the diff does touch move by a magnitude that matches the change (patch for fixes, minor for new behavior, major for breaking).

Judge from the diff and messages only — never demand evidence that a build or test run happened before the commit.
