# Session: landing the cookbook design and tooling from the devteam branch

- **Date:** 2026-11-19
- **Session:** `42c82725-9e4b-4ae4-aed3-3ac87a841295`
- **Branch:** `cookbook-design-landing`

## Orientation

The cookr and grow-cookbook work, and the new artifact design (roled parts, named rules, one source per topic, a
`research/` folder per topic), had all been built on the devteam's `devteam-scope-specialists` branch. This session
moved that work to the cookbook's `main`, so that everyone using cookr gets it, while the devteam and teamtesting
pins were left alone. It ran as an all-night run under the development playbook.

Phase 1, tooling and design, has landed as PR #81. Phase 2, converting the content, is next. After it, the devteam
re-pins this cookbook.

## Decisions

- **The cookbook lands first, and the devteam re-pins after.** The owner did not want the devteam touched while the
  cookbook was landing. The devteam branch is therefore a later phase, tracked in teamtesting's
  `docs/superpowers/plans/2026-11-19-devteam-scope-specialists-landing.md`.
- **Fold the copies instead of keeping two topics.** 95 unflagged pairs were folded, plus 7 of the 10 flagged ones.
  completeness, unit-test-patterns and properties-of-good-tests stay as separate topics, by the owner's ruling. Two
  topics on one subject break the one-source rule.
- **The fold refuses to drop research.** A copy that holds `research/` or nested artifacts is refused before
  anything is written (review f2). The copy's exemption entry is carried over to the surviving topic (f1), so a fold
  can never make `validate` fail.
- **One cut of a reference file.** run_gaps had rebuilt the cut from gaps' private regexes. When f7 removed one of
  those regexes, every run_gaps cut broke at the test gate. `gaps.pieces` is now public, and both tools cut with it,
  so the two can no longer drift apart.
- **Run conditions for the night run.** Tests ran only at each phase gate and were pre-authorized. Reviews were
  `mycodereview --cr high`. No devteam review was run.

## Considered and rejected

- **Making `held()` in gaps match on whole words only.** This was half of finding f7, and it was refuted.
  `test_gaps_holds_a_substring_whose_edge_words_are_partial` pins the substring behaviour on purpose, and
  `MIN_WORDS` already drops the short sentences that would make that behaviour noisy.
- **Landing everything as one branch.** Rejected under the playbook. Each phase gets its own review and its own
  merge.

## Open threads

- **Phase 2.**
  - Convert about 250 guideline topics in batches of about 20, one commit per topic. Each topic must pass `lossless`
    and an independent judge.
  - Convert the 44 principles.
  - Write the R3 reviewer and build parts for topics that have no review text.
  - Keep every converted topic in `research-exempt.json` until it has been researched.
- **Phase 3 (in teamtesting).** Re-pin the cookbook in agenticdevteam, then point every speciality whose
  `metadata.cookbook` names a folded topic at that topic's survivor. After that, re-pin pipeline and devteam, then
  review and ship each repo.

## Pointers

- Checklist: [2026-11-19-cookbook-design-landing.md](../superpowers/plans/2026-11-19-cookbook-design-landing.md)
- Status: [STATUS.md](../project/STATUS.md), the section for PR #81
- Review: `2026-11-20-live-claude-claude-opus-5-5-e51c` in the private reviews repo
