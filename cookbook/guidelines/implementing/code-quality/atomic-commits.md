---
id: 8075b95b-2678-4893-9a5a-eb77aa9232aa
title: "Small, atomic commits"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/atomic-commits
type: guideline
version: 1.2.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "One logical change per commit. A change may touch multiple files if they are part of the same concept. Commit as work progresses; do not batch up unrelated changes."
platforms: []
tags:
  - atomic-commits
  - code-quality
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/scope-discipline
  - agenticdevelopercookbook://guidelines/testing/post-generation-verification
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - pre-commit
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2.2 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.2.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.2.0 | 2026-06-09 | Mike Fullerton | Add small-diff discipline for agent-generated changes |
| 1.1.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.1.0 | 2026-03-28 | Mike Fullerton | Add build-verify-commit loop, expand guidance |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
