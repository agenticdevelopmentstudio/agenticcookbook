# test-impact-analysis: research agent run (fallback)

team_probe: researchteam not runnable (missing distributions: PyYAML, aiohttp, mcp, websockets); one fresh Opus
agent ran the filled research prompt. Its reply, verbatim:

I've written both research files and the validator prints `Research passed.` Of the five listed rules, only `fail-closed-when-unsure` is supported, at SHOULD. The other four are unsupported at their fail strength, and the research adds 11 `new` rules. Nothing is committed, as you asked.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-impact-analysis/research/research.md`

**Claims per question (60 in total)**
- best-practices: 10 (6 researched, plus the 4 `-prior` claims)
- known-solutions: 21
- platform-guidelines: 21
- experts-view: 8

**Verdicts**
- fail-closed-when-unsure: supported, at SHOULD. Claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, rts-safe-selects-all-affected, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push
- each-selection-justified-by-diff: unsupported. Claims: each-selection-justified-by-diff-prior, develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-includes-failing-and-new, develocity-pts-always-chooses
- every-changed-path-accounted-for: unsupported. Claims: every-changed-path-accounted-for-prior, bazel-diff-changed-list-is-correctness-contract, azure-tia-unknown-file-type-runs-all
- fail-closed-is-stated: unsupported. Claims: fail-closed-is-stated-prior, bazel-diff-fallback-costs-speed, develocity-records-selection-reason
- reasoning-cites-diff-contents: unsupported. Claims: reasoning-cites-diff-contents-prior, bazel-diff-content-hashes, nx-selects-by-task-inputs, android-test-mapping-directory-rules, gha-paths-filter-any-match-runs
- unknown-reach-selects-everything: new. This covers your fail-closed impact analysis subject. Claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push, rts-safe-selects-all-affected
- shared-inputs-select-everything: new. Claims: nx-lockfile-affects-every-task, pants-lockfile-change-all-users, bazel-diff-hashes-all-inputs, hammant-resource-files-unmapped
- select-by-dependency-graph-not-paths-alone: new. Claims: nx-selects-by-task-inputs, nx-dependson-not-affected, bazel-rdeps-operator, bazel-tests-operator, pants-changed-dependents, turborepo-affected, tap-affected-targets-reverse-dependencies, gradle-up-to-date-tests, gha-paths-filter-any-match-runs, mill-module-graph-granularity, single-language-rts-unsafe, rtslinux-ekstazi-misses-dependencies, hammant-coverage-builds-the-map
- diff-against-a-known-good-base: new. Claims: nx-base-latest-successful-commit, gitlab-compare-to-base, target-determinator-changed-targets, turborepo-shallow-checkout-all-changed
- run-the-full-suite-periodically: new. Claims: azure-tia-periodic-full-run, launchable-full-suite-later-in-pipeline, launchable-full-suite-nightly, develocity-remaining-tests-mode, develocity-pts-trades-comprehensiveness, mill-thorough-tests-after-merge, hammant-nightly-all-tests, tap-milestones-batch-commits, apple-test-plans-umbrella-full-run, android-test-mapping-directory-rules
- always-select-new-changed-and-failing-tests: new. Claims: azure-tia-includes-failing-and-new, develocity-pts-always-chooses
- validate-selection-against-full-runs: new. Claims: azure-tia-validate-against-all-tests, launchable-observation-mode, leong-selection-remains-open, meta-retrain-model
- record-why-each-test-was-selected: new. This covers your impact analysis evidence subject. Claims: develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-reports-selection, bazel-diff-fallback-costs-speed
- select-from-every-changed-file: new. Claims: bazel-diff-changed-list-is-correctness-contract, bazel-diff-content-hashes, launchable-model-inputs, azure-tia-unknown-file-type-runs-all
- measure-selection-recall-and-savings: new. Claims: meta-predictive-selection-results, meta-build-deps-overselect, tap-affected-targets-rarely-fail, tap-all-affected-infeasible-per-change, ekstazi-time-savings, rtslinux-ekstazi-misses-dependencies, leong-selection-remains-open
- path-skipped-required-checks-resolve: new. Claims: gha-skipped-required-check-blocks, gha-paths-filter-any-match-runs

The four unsupported rules state their checks as fails, but the sources hold them only at SHOULD. Tools also select tests for reasons outside the diff, such as previously failing, new or flaky tests. No source covers reasoning from commit messages or branch names, so that part of `reasoning-cites-diff-contents` could be neither supported nor contradicted. The six open questions in research.json, one owner decision each, include whether to keep these four at fail strength or restate them at SHOULD.
