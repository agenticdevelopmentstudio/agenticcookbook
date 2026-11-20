# Cookbook design landing — phase checklist

Lands the cookr and grow-cookbook improvements and the new artifact design from the `devteam-scope-specialists`
branch on the cookbook's `main`, so everyone using cookr and the cookbook gets them. Only this repo changes: the
devteam and teamtesting pins stay where they are and are re-pinned later.

Gate rule (owner, 2026-11-19): no tests and no code review run before the end of a phase. For the 2026-11-19 night
run the owner pre-authorized every phase's test gate, and reviews are `mycodereview --cr high`.

## Phase 1 — tooling and design (`cookbook-design-landing`)

Tooling
- ✅ gapfix15 committed (G303–G305); grow-cookbook 1.4.44 (G305: no time or order dependence found by reading; the repeat runs happen at the test gate)
- ✅ main's 6d9333f (NEEDS REVIEW markers) merged; the 3 cookr conflicts resolved keeping both features; cookr 0.22.0
- ✅ the conventions guide describes roled parts, named rules, one source per topic and `research/` as the standard
- ✅ `cookr validate` requires `research/` on every topic not listed in `research-exempt.json`
- ✅ `research-exempt.json` explains itself with no path outside this repo
- ✅ grow-cookbook stage 1 without a devteam checkout exits with a plain message naming what it needs

Content
- ✅ the copies folded into their surviving topics (95 unflagged + 7 of the 10 flagged pairs, by the owner's ruling;
  completeness, unit-test-patterns and properties-of-good-tests kept as separate topics); every link and UUID redirected
- ✅ every topic still owed research listed in `research-exempt.json` (380; `OWED_CEILING = 380`)
- ✅ ab-testing, debug-mode and feature-flags pass `cookr roles lossless --require-judged` and `cookr validate`
- ✅ `cookr update` run; README and CLAUDE.md counts current

Gates
- ✅ cookr and skill suites, full `validate` and lint pass (cookr unit + functional, grow-cookbook 696; validate and
  `lint --no-llm` over 383 artifacts)
- ✅ whole-branch review (`mycodereview --squashed --cr high`, review `2026-11-20-live-claude-claude-opus-5-5-e51c`):
  10 findings, each fixed in its own commit (f4, f7 and f10 in part; the refuted halves say why in their commits);
  fixes recorded with `teambench live fixes`; suites re-run after the fixes: cookr 1550, grow-cookbook 698,
  `validate` and `lint --no-llm` over 383 artifacts all pass
- ⬜ landed with `/ship no-squash`

## Phase 2 — convert the content (`cookbook-design-landing-phase-2`)

A fresh worktree off `main` after phase 1 lands.

- ⬜ ~250 guideline topics converted to roled parts in batches of ~20; each passes `lossless` and an independent judge;
  one commit per topic
- ⬜ all 44 principles converted
- ⬜ topics with no review text get reviewer and build parts written from their own rules (R3)
- ⬜ each converted topic stays in `research-exempt.json` until researched
- ⬜ `cookr update`; gates as in phase 1; landed with `/ship no-squash`
