<!-- leaf: implement-code-quality/atomic-commits · source: guidelines/implementing/code-quality/atomic-commits.md -->

**Rules** (cite as `implement-code-quality/atomic-commits#<slug>`):

- `verify` MUST — the build MUST pass and existing tests MUST still pass before committing
- `multiple-uncommitted-changes-not-stacked-change-breaks-build` MUST — Multiple uncommitted changes MUST NOT be stacked. If a change breaks the build, fix it before moving on — do not add …
- `work-planned-into-small-reviewable` SHOULD — Work SHOULD be planned into small, reviewable pull requests before writing code, not carved down afterward. Large diffs …

# Small, atomic commits

One logical change per commit. A change may touch multiple files if they are part of the same concept. Commits should happen as work progresses — do not batch up unrelated changes.

## The build-verify-commit loop

For every logical change:

1. **Make the change** — implement one coherent unit of work
2. **Build** — run the platform build command (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`, `cargo build`)
3. **Verify** — the build MUST pass and existing tests MUST still pass before committing
4. **Commit** — commit the passing change with a descriptive message
5. **Repeat** — move to the next logical change

Multiple uncommitted changes MUST NOT be stacked. If a change breaks the build, fix it before moving on — do not add more changes on top of a broken state. This prevents compound debugging sessions where multiple interacting changes all break at once.

## What counts as one logical change

A single logical change is the smallest unit of work that makes sense on its own:

- Adding one function and its tests
- Renaming a symbol and updating all references
- Fixing one bug
- Adding one configuration option

A change may touch multiple files if they are part of the same concept — an interface and its implementation, a component and its test file.

## Small diffs for agent-generated changes

Work SHOULD be planned into small, reviewable pull requests **before** writing code, not carved down afterward. Large diffs degrade both human and AI reviewers: once a change exceeds what fits in a reviewer's working context, review collapses into shallow pattern-matching rather than reasoning about correctness. AI-generated code SHOULD receive more per-line scrutiny, not less — which makes small, frequent diffs more important for agent-authored work, not a luxury to be skipped under time pressure. When a planned unit of work looks like it will produce a large diff, it SHOULD be split into a sequence of smaller PRs.

## Why this matters

Batched, uncommitted changes create compound failures that are difficult to debug. When three changes interact in a broken build, isolating which change caused the failure requires significantly more effort than catching each failure as it occurs. Small, committed changes are also individually revertible, bisectable, and reviewable.
