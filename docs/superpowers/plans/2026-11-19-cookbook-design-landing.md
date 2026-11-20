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
- ✅ landed with `/ship no-squash` (PR #81, `c37f15c`)

## Phase 2 — convert the content (`cookbook-design-landing-phase-2`)

A fresh worktree off `main` after phase 1 lands.

- ✅ ~250 guideline topics converted to roled parts in batches of ~20; each passes `roles lossless --base 0005775`, and
  every reworded or dropped sentence has an independent judge's pass in the topic's `lossless.json` (a topic whose
  every old sentence survives verbatim needs no `lossless.json`: six do, file-paths, no-external-dependencies-in-core-
  libraries, type-hints, use-roadmaplib, yaml-frontmatter and data-types). The conversions were committed one per
  topic, then squashed (`squashr`) before the review into one content commit, `508d051`, with the rename, orphan-part
  cleanup and index regeneration that rode along (278 guidelines; 268 roled, the 10 under `guidelines/reviewing/`
  stay unroled by rule)
- ✅ all 44 principles converted
- ✅ topics with no review text get reviewer and build parts written from their own rules (R3)
- ✅ each converted topic stays in `research-exempt.json` until researched
- ✅ `cookr update` run; README and CLAUDE.md counts current
- ✅ whole-branch review (`mycodereview --squashed --cr high`, review `2026-11-20-live-claude-claude-opus-5-5-ac2d`):
  8 findings, each fixed in its own commit (f6 in two: the cookr fix and the 13 topics; f8 by recording why the
  pinned bundles stay); fixes recorded with `teambench live fixes`; suites re-run after the fixes: cookr 1543,
  grow-cookbook 698, `validate` and `lint --no-llm` over 383 artifacts all pass
- ✅ landed with `/ship no-squash` (PR #83, `23deb6d`)
- ℹ️ Two reviewed commits bundle changes that could have stood alone (review `2026-11-20-live-claude-claude-opus-5-5-ac2d`,
  f8). They stay bundled, because they are the commits that review pinned. Splitting them now would rewrite the pinned
  commit and cut its fix commits off from it. What each one holds, for anyone reverting part of it:
  - `fe1451b`: cookr 0.22.1 (`renamed_from`, so a renamed topic is checked against its old folder), 0.22.2 (a twin
    folded into its survivor is accounted as a copy) and 0.23.0 (per-use-case routes);
  - `508d051`: the 312 conversions; `unit-test-patterns` renamed to `test-vector-patterns` (its `lossless.json`
    `renamed_from`); the orphan parts removed; the `writing-comments-and-docs` content change; the regenerated
    indexes; the batch reports under `docs/superpowers/reports/2026-11-19-phase-2/`.
  For the next branch, the squash happens before the review, so a branch's logical changes land as separate commits.
