# Cookbook design landing — phase checklist

Lands the cookr and grow-cookbook improvements and the new artifact design from the `devteam-scope-specialists`
branch on the cookbook's `main`, so everyone using cookr and the cookbook gets them. Only this repo changes: the
devteam and teamtesting pins stay where they are and are re-pinned later.

Gate rule (owner, 2026-11-19): no tests and no code review run before the end of a phase, and at each gate the work
stops and asks the owner before running it.

## Phase 1 — tooling and design (`cookbook-design-landing`)

Tooling
- ✅ gapfix15 committed (G303–G305); grow-cookbook 1.4.44 (G305: no time or order dependence found by reading; the repeat runs happen at the test gate)
- ✅ main's 6d9333f (NEEDS REVIEW markers) merged; the 3 cookr conflicts resolved keeping both features; cookr 0.22.0
- ⬜ the conventions guide describes roled parts, named rules, one source per topic and `research/` as the standard
- ✅ `cookr validate` requires `research/` on every topic not listed in `research-exempt.json`
- ✅ `research-exempt.json` explains itself with no path outside this repo
- ⬜ grow-cookbook stage 1 without a devteam checkout exits with a plain message naming what it needs

Content
- ⬜ the 105 copies folded into their surviving topics; every link and UUID redirected; flagged pairs ruled by the owner
- ⬜ every topic still owed research listed in `research-exempt.json`
- ⬜ ab-testing, debug-mode and feature-flags pass `cookr roles lossless --require-judged` and `cookr validate`
- ⬜ `cookr update` run; README and CLAUDE.md counts current

Gates (each asked for before it runs)
- ⬜ cookr and skill suites, full `validate` and lint pass
- ⬜ whole-branch review (`--skip devteam`) has no unrefuted finding open
- ⬜ landed with `/ship no-squash`

## Phase 2 — convert the content (`cookbook-design-landing-phase-2`)

A fresh worktree off `main` after phase 1 lands.

- ⬜ ~250 guideline topics converted to roled parts in batches of ~20; each passes `lossless` and an independent judge;
  one commit per topic
- ⬜ all 44 principles converted
- ⬜ topics with no review text get reviewer and build parts written from their own rules (R3)
- ⬜ each converted topic stays in `research-exempt.json` until researched
- ⬜ `cookr update`; gates as in phase 1 (asked for first); landed with `/ship no-squash`
