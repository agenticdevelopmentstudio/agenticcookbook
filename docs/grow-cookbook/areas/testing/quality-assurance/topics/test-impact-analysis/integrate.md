# Integrate: test-impact-analysis

Lossless: a new topic, with no base text in the cookbook (`roles lossless` reports the artifact is not in the base 77a898dbc718928bbd96ef617723c83ec69cd549); nothing to account for.

## For the owner

`cookr validate` owner-decides warnings for this topic. Each rule below cites its `-prior` claim, which the research rules unsupported. The owner decides each rule: keep it as it is, reword it, or drop it. Each stands, word for word under the lead-in "This MUST hold:", until the owner decides.

- `each-selection-justified-by-diff` (unsupported)
- `every-changed-path-accounted-for` (unsupported)
- `fail-closed-is-stated` (unsupported)
- `reasoning-cites-diff-contents` (unsupported)

The prior text of these rules, kept word for word as the owner list requires, carries the old team's words: "site", "residue path", "the prose" and "commit range". The intro defines them in this guideline's terms; a reword would make them general.

Open questions from owner-list.md:

- How often the periodic full run happens and where: Azure TIA leaves the periodicity configurable, Launchable names post-merge and nightly, Develocity names nightly and pre-release, and Google TAP runs all affected targets per milestone (about every 45 minutes); the owner decides whether the rule names one cadence or requires the team to set and record one.
- Whether predictive (machine-learned) selection may gate a merge on its own, or only run pre-merge with a deterministic or full run behind it: Meta and Develocity accept a bounded miss rate, while the safe-selection literature does not.
- Whether each-selection-justified-by-diff, every-changed-path-accounted-for, fail-closed-is-stated and reasoning-cites-diff-contents keep their fail (MUST) strength as team checks or are restated at the SHOULD strength the sources support.
- Whether a test selected for a reason outside the diff (previously failing, newly added, recently flaky, as Azure TIA and Develocity do) counts as justified under each-selection-justified-by-diff.
- Which file classes a team may declare as unable to affect tests (Azure TIA's TIA_IncludePathFilters exclusions, GitHub paths-ignore), and who approves that list, since every exclusion narrows a fail-safe fallback.
- Which shared inputs select everything in the cookbook's general rule (lockfiles, build and CI configuration, toolchains, shared test fixtures): the tools differ, with Nx defaulting a lockfile change to every task and Pants treating a lockfile change as changing all users of any dependency.

integrated: 2026-11-24
