<!-- leaf: ship-general/atomic-commits · source: guidelines/shipping/atomic-commits.md -->

**Rules** (cite as `ship-general/atomic-commits#<slug>`):

- `verify` MUST — the build MUST pass and existing tests MUST still pass before committing
- `multiple-uncommitted-changes-not-stacked-change-breaks-build` MUST — Multiple uncommitted changes MUST NOT be stacked. If a change breaks the build, fix it before moving on — do not add …
- `written-after-work-split-into-small-independently` SHOULD — The decision to keep a change reviewable happens before code is written, not after. Work SHOULD be split into small, …
- `agent-generated-output-receive-more-per-line` SHOULD — Agent-generated output SHOULD receive more per-line scrutiny than hand-written code, because plausible-looking code can …

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

The decision to keep a change reviewable happens before code is written, not after. Work **SHOULD** be split into small, independently reviewable pull requests up front — plan the slices first, then implement one slice at a time. Large diffs degrade reviewers regardless of who reads them: humans skim past detail and AI reviewers lose precision as context grows.

Agent-generated output **SHOULD** receive more per-line scrutiny than hand-written code, because plausible-looking code can hide subtle defects. That makes small, frequent diffs matter more here, not less — a reviewer (human or AI) can hold a 50-line change fully in view, but not a 1,000-line one. When an agent produces a large change, it **SHOULD** be decomposed into smaller commits or PRs before review rather than reviewed as one block.

## Why this matters

Batched, uncommitted changes create compound failures that are difficult to debug. When three changes interact in a broken build, isolating which change caused the failure requires significantly more effort than catching each failure as it occurs. Small, committed changes are also individually revertible, bisectable, and reviewable.
