# Write brief: test-impact-analysis

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-impact-analysis/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- fail-closed-when-unsure: supported (claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, rts-safe-selects-all-affected, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push)
- each-selection-justified-by-diff: unsupported (claims: each-selection-justified-by-diff-prior, develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-includes-failing-and-new, develocity-pts-always-chooses)
- every-changed-path-accounted-for: unsupported (claims: every-changed-path-accounted-for-prior, bazel-diff-changed-list-is-correctness-contract, azure-tia-unknown-file-type-runs-all)
- fail-closed-is-stated: unsupported (claims: fail-closed-is-stated-prior, bazel-diff-fallback-costs-speed, develocity-records-selection-reason)
- reasoning-cites-diff-contents: unsupported (claims: reasoning-cites-diff-contents-prior, bazel-diff-content-hashes, nx-selects-by-task-inputs, android-test-mapping-directory-rules, gha-paths-filter-any-match-runs)
- unknown-reach-selects-everything: new (claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push, rts-safe-selects-all-affected)
- shared-inputs-select-everything: new (claims: nx-lockfile-affects-every-task, pants-lockfile-change-all-users, bazel-diff-hashes-all-inputs, hammant-resource-files-unmapped)
- select-by-dependency-graph-not-paths-alone: new (claims: nx-selects-by-task-inputs, nx-dependson-not-affected, bazel-rdeps-operator, bazel-tests-operator, pants-changed-dependents, turborepo-affected, tap-affected-targets-reverse-dependencies, gradle-up-to-date-tests, gha-paths-filter-any-match-runs, mill-module-graph-granularity, single-language-rts-unsafe, rtslinux-ekstazi-misses-dependencies, hammant-coverage-builds-the-map)
- diff-against-a-known-good-base: new (claims: nx-base-latest-successful-commit, gitlab-compare-to-base, target-determinator-changed-targets, turborepo-shallow-checkout-all-changed)
- run-the-full-suite-periodically: new (claims: azure-tia-periodic-full-run, launchable-full-suite-later-in-pipeline, launchable-full-suite-nightly, develocity-remaining-tests-mode, develocity-pts-trades-comprehensiveness, mill-thorough-tests-after-merge, hammant-nightly-all-tests, tap-milestones-batch-commits, apple-test-plans-umbrella-full-run, android-test-mapping-directory-rules)
- always-select-new-changed-and-failing-tests: new (claims: azure-tia-includes-failing-and-new, develocity-pts-always-chooses)
- validate-selection-against-full-runs: new (claims: azure-tia-validate-against-all-tests, launchable-observation-mode, leong-selection-remains-open, meta-retrain-model)
- record-why-each-test-was-selected: new (claims: develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-reports-selection, bazel-diff-fallback-costs-speed)
- select-from-every-changed-file: new (claims: bazel-diff-changed-list-is-correctness-contract, bazel-diff-content-hashes, launchable-model-inputs, azure-tia-unknown-file-type-runs-all)
- measure-selection-recall-and-savings: new (claims: meta-predictive-selection-results, meta-build-deps-overselect, tap-affected-targets-rarely-fail, tap-all-affected-infeasible-per-change, ekstazi-time-savings, rtslinux-ekstazi-misses-dependencies, leong-selection-remains-open)
- path-skipped-required-checks-resolve: new (claims: gha-skipped-required-check-blocks, gha-paths-filter-any-match-runs)

Second-check corrections, refuted (criteria 3 applies to these claims):
- pants-lockfile-change-all-users: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- hammant-resource-files-unmapped: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- hammant-nightly-all-tests: refuted (quote-found yes, supports-claim no); trust 58 -> 18; a rule citing it cannot carry MUST
- azure-tia-reports-selection: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- bazel-diff-changed-list-is-correctness-contract: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST
- tap-all-affected-infeasible-per-change: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **each-selection-justified-by-diff** — verdict `unsupported` (claims: each-selection-justified-by-diff-prior, develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-includes-failing-and-new, develocity-pts-always-chooses). Prior text, kept word for word: "Every included site is justified in the prose by a named path or hunk from the commit range. A site in the list with no stated reason is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Each Develocity build scan records which tests were selected and which were not, with the reason for each.
  - against: Nx can show why each task was selected as affected.
  - against: Target Determinator can explain why each target it selects is being run.
  - against: Azure TIA's selection includes, besides impacted tests, the tests that failed previously and the tests newly added.
  - against: Develocity Predictive Test Selection always selects tests that are recently new, recently changed, recently failed or recently flaky, whatever the model predicts.
- **every-changed-path-accounted-for** — verdict `unsupported` (claims: every-changed-path-accounted-for-prior, bazel-diff-changed-list-is-correctness-contract, azure-tia-unknown-file-type-runs-all). Prior text, kept word for word: "Every residue path handed to the analysis is accounted for: either attributed to sites, or named as unattributable with its candidate sites included anyway. A residue path that goes unmentioned is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The list of changed files fed to a selection must include every file that actually changed; a changed file left off it silently drops the targets it impacts.
  - against: When Azure TIA meets a changed file of a type it cannot map, it runs all tests, which Microsoft calls good from a safety perspective.
- **fail-closed-is-stated** — verdict `unsupported` (claims: fail-closed-is-stated-prior, bazel-diff-fallback-costs-speed, develocity-records-selection-reason). Prior text, kept word for word: "Fail-closed is visible in the output: where the analysis was unsure, the prose says so and the sites are included. An answer that narrows the list on a judgment call it does not state is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: When bazel-diff cannot derive an incremental result it falls back to a full computation, trading speed but never correctness, and logs which path each run took.
  - against: Each Develocity build scan records which tests were selected and which were not, with the reason for each.
- **reasoning-cites-diff-contents** — verdict `unsupported` (claims: reasoning-cites-diff-contents-prior, bazel-diff-content-hashes, nx-selects-by-task-inputs, android-test-mapping-directory-rules, gha-paths-filter-any-match-runs). Prior text, kept word for word: "The reasoning cites the diff. A judgment resting only on commit messages, branch names, or file names without their contents is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: bazel-diff decides a source file changed from a hash of its content, not from its name or the commit metadata.
  - against: Nx selects a task as affected when the change touches one of that task's declared inputs, not by its place in the task graph.
  - against: Android's TEST_MAPPING files map a directory (optionally narrowed by file patterns) to the tests that run in presubmit when files in it change, with separate postsubmit groups.
  - against: A GitHub Actions paths filter runs the workflow when at least one changed path matches; it selects whole workflows by path pattern, with no knowledge of dependencies.

## Open questions

- How often the periodic full run happens and where: Azure TIA leaves the periodicity configurable, Launchable names post-merge and nightly, Develocity names nightly and pre-release, and Google TAP runs all affected targets per milestone (about every 45 minutes); the owner decides whether the rule names one cadence or requires the team to set and record one.
- Whether predictive (machine-learned) selection may gate a merge on its own, or only run pre-merge with a deterministic or full run behind it: Meta and Develocity accept a bounded miss rate, while the safe-selection literature does not.
- Whether each-selection-justified-by-diff, every-changed-path-accounted-for, fail-closed-is-stated and reasoning-cites-diff-contents keep their fail (MUST) strength as team checks or are restated at the SHOULD strength the sources support.
- Whether a test selected for a reason outside the diff (previously failing, newly added, recently flaky, as Azure TIA and Develocity do) counts as justified under each-selection-justified-by-diff.
- Which file classes a team may declare as unable to affect tests (Azure TIA's TIA_IncludePathFilters exclusions, GitHub paths-ignore), and who approves that list, since every exclusion narrows a fail-safe fallback.
- Which shared inputs select everything in the cookbook's general rule (lockfiles, build and CI configuration, toolchains, shared test fixtures): the tools differ, with Nx defaulting a lockfile change to every task and Pants treating a lockfile change as changing all users of any dependency.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md` `run-the-full-suite-periodically`, `selecting-tests-for-a-change.md` step 9, `rationale.md` paragraph 4: the full-run rule outruns two of the claims it cites, and the text calls things full runs that the research says are not. Every instance: (1) `tap-milestones-batch-commits` says TAP runs, per milestone, the targets affected since the previous milestone (the second check confirms: "milestones run tests selected by reverse dependencies on files changed since the previous milestone"), which is a batched affected-set run, not the full suite; step 9 lists "Google TAP's milestones" as a full run. (2) `android-test-mapping-directory-rules` says TEST_MAPPING has separate postsubmit groups, which are still directory-mapped tests, not the full suite; step 9 lists "Android's postsubmit groups" as a full run. (3) Rationale paragraph 4 opens "A full run stays behind the subset in every source that selects", but most of the selecting sources read (Nx, Bazel, Pants, Turborepo, Target Determinator, bazel-diff, GitHub Actions, GitLab, Gradle) say nothing of a full run; only Microsoft, Launchable, Develocity and Mill do. Fix: reword step 9 so TAP milestones are a batched run of everything affected since the last milestone and Android postsubmit groups are a later, wider mapped group, not full runs; either widen the rule so these two claims support it (for example "the full suite, or every test affected by the changes since the last such run, at some later point ...") or cite them from a rule they do support (both claims come from a `new` verdict, so they must stay cited somewhere); and change "in every source that selects" to name the sources that say it.
- R1.2: `rationale.md` (with `rules.md`): the rationale for allowing deviation (behavioral-requirements `must-explain-rationale-for-should-requirements`) and the conditions for a MAY (`should-document-conditions-for-may-requirements`) are missing for these rules; the rationale never mentions them and the rule text gives no reason: `diff-against-a-known-good-base` (SHOULD; why a known-good base and when another base is acceptable), `log-each-fallback` (SHOULD; why the fallback is logged, from `bazel-diff-fallback-costs-speed`), and `decide-change-by-content` (MAY; when content hashing is worth using rather than names or commit metadata). Every other SHOULD has its reason in the rationale or inline (`path-skipped-required-checks-resolve` carries its "so a skipped workflow does not block the merge"). Fix: add one sentence each to the rationale from the claims already cited (Nx's latest-successful-commit recommendation and Turborepo's shallow-checkout behaviour; bazel-diff logging which path each run took; bazel-diff hashing content rather than names or metadata).
- R1.3: `rules.md` `always-select-new-changed-and-failing-tests` ("recently new, recently changed, recently failed or recently flaky") and `retrain-a-learned-selector` ("retrain it regularly"): unanchored relative terms (behavioral-requirements `should-not-use-unanchored-relative-terms`); a reviewer cannot tell PASS from FAIL on "recently" or "regularly". The research gives no threshold (Develocity and Meta use the same words), so a number would be invented. Fix: anchor each to a window the team states and records (for example "recently, within a window the team states" and "on a cadence the team states"), or say in the rationale that the sources give no threshold and the team sets one; the same applies to the matching lines in `a-build-must-establish.md`.
- R1.4: `rationale.md` paragraph 5 ("The four Verify checks"), `a-build-must-establish.md` and `what-a-reviewer-looks-for.md` (the owner rules' "site", "residue path", "the prose", "commit range"): terms the guideline never defines. "Verify checks" is the author's own wording and names nothing in this guideline. "Site" and "residue path" come from the owner rules, whose wording is exempt, but the surrounding text repeats them (build lines for `each-selection-justified-by-diff`, `every-changed-path-accounted-for`, `fail-closed-is-stated`) without ever saying what a site or a residue path is, while every other part speaks of tests, targets and changed files; a reader cannot apply those MUST rules (behavioral-requirements `must-be-independently-testable`). Fix: in the rationale say "the four rules kept as the owner's text" instead of "Verify checks"; outside the exempt rule text (intro or how-to), say what a site and a residue path are in this guideline's terms (a selected test or test target; a changed path handed to the analysis to attribute), without changing the four rules' wording.
- R1.5: `examples.md`: the record shows a fallback for `package-lock.json` ("every test that uses an npm dependency is selected") but never names the tests that fallback selected, so the illustration of `record-why-each-test-was-selected` and `every-changed-path-accounted-for` leaves the one unattributable path without its sites; it is also unclear whether `pricing:test`, `checkout:test` and `cart:test` are the npm users or graph-only selections. Fix: list the tests the lockfile fallback selected (for example "Selected by fallback (package-lock.json): pricing:test, checkout:test, cart:test, search:test") so every changed path in the record is attributed to named tests.

## Round 2 findings

Verdict: pass. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

none
