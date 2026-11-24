## azure-tia-safe-fallback
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists "Safe fallback" and gives the example that a commit changing HTML or CSS files makes TIA fall back to running all tests.

## azure-tia-unknown-file-type-runs-all
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The next sentence reads "While this action is good from a safety perspective, tuning this behavior might be useful in some cases."

## bazel-diff-fallback-costs-speed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is in the README's `--partialGraph` section. When a derivation is impossible (added or renamed paths, BUILD or .bzl edits and so on), it "falls back to a full generation".

## turborepo-shallow-checkout-all-changed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote comes right after "The comparison requires everything between base and head to exist in the checkout."

## gha-diff-timeout-always-runs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same list also says "If a push contains more than 1,000 commits, the workflow will always run."

## gitlab-changes-true-without-push
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source names tag, scheduled and manual pipelines as having no push event, and points to `compare_to` for these cases.

## rts-safe-selects-all-affected
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The PDF text loses the "ff" ligature ("afected"), which is a formatting difference only. The paper says techniques "all greatly vary in safety and precision".

## nx-lockfile-affects-every-task
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The URL now redirects to nx.dev/docs/features/ci-features/affected. The default can be narrowed with `projectsAffectedByDependencyUpdates: "auto"`.

## pants-lockfile-change-all-users
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only the hedge that third-party changes "may not be surfaced as you expect". The claim's main point is in the next sentence, which the quote leaves out: any change to one dependency in a lockfile or target generator "will consider all users of any dependency changed, transitively."
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## bazel-diff-hashes-all-inputs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The hash combines the rule implementation hash, every attribute and all rule inputs, so a change to any input changes the hash.

## hammant-resource-files-unmapped
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: "The tool" is Testar, one contributor's tool described in the article's appendix. The user has to list resource files for it, otherwise it re-runs all tests. The source does not state this as a limit of coverage-based mapping in general.
- correction: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST

## nx-selects-by-task-inputs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is under the heading "What decides whether a task is affected".

## nx-dependson-not-affected
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Nearby text says "An edge that only orders the two tasks doesn't carry the change across. Declare inputs and outputs, even for tasks you don't cache."

## bazel-rdeps-operator
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source states the definition verbatim.

## bazel-tests-operator
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source has the definition verbatim. Chaining `rdeps` then `tests` is the claim's own composition of two operators the page documents.

## pants-changed-dependents
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source goes on to offer `--changed-dependents=direct` or `=transitive` to include the targets that depend on the changed files.

## turborepo-affected
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The flag is documented under `turbo run` Options, and by default it equals `--filter=...[main...HEAD]`.

## tap-affected-targets-reverse-dependencies
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: TAP builds a reverse dependency structure from the build dependencies declared in BUILD files.

## gradle-up-to-date-tests
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same passage offers `--rerun` to force a task to rerun.

## gha-paths-filter-any-match-runs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The filter is glob patterns over changed paths that gate a whole workflow. "No knowledge of dependencies" is the claim's own description of that, and the source says nothing to the contrary.

## mill-module-graph-granularity
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: In the source's example, a change to `backend_service_utils` runs tests for all three services even when one is not affected.

## single-language-rts-unsafe
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The PDF loses the "fi" ligature ("language-speciic"), a formatting difference only. The paper says this of existing dynamic RTS techniques.

## rtslinux-ekstazi-misses-dependencies
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The paper concludes "Ekstazi is less safe than RTSLinux". It gives an example change where RTSLinux selects tests that Ekstazi "misses to select".

## hammant-coverage-builds-the-map
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source sentence continues "(details below)", and the next sentence describes the resulting map of production sources to tests.

## nx-base-latest-successful-commit
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The stated reason is "This ensures that all changes since the last successful CI run are accounted for."

## gitlab-compare-to-base
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This covers tag, scheduled, manual and new-branch pipelines. The claim text has a typo ("has a team name") but its sense matches.

## target-determinator-changed-targets
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The README sentence is verbatim, and the usage takes a before-revision and compares it with the current checkout.

## azure-tia-periodic-full-run
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is under "Manage Test Impact Analysis behavior", in the VSTest task UI part.

## launchable-full-suite-later-in-pipeline
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source calls this a "defensive run" that catches issues the subset may miss.

## launchable-full-suite-nightly
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is in the shift-left use case and continues "(and recording the outcome of those runs with launchable record tests)". That recording is what feeds the model.

## develocity-remaining-tests-mode
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source pairs "relevant tests" mode in early stages with "remaining tests" mode in later, less frequent stages such as nightly or pre-release builds. The URL now redirects to the 2026.3 guide.

## develocity-pts-trades-comprehensiveness
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same sentence says this makes it worthwhile "where reducing feedback time is critical, such as local and pre-merge/pull-request builds."

## mill-thorough-tests-after-merge
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source sentence goes on with "and prevent bugs from being shipped to customers", and then advises bisecting any bug found after merge.

## hammant-nightly-all-tests
- quote-found: yes
- supports-claim: no
- citation 1: holds-quote
- result: refuted
- note: The source says teams using suites and tags "might choose" a smaller suite per commit plus a nightly job, and criticises it right away ("delays bad news, and defeats the aims of Continuous Integration"). It does not describe a practice of teams that select tests per commit.
- correction: refuted (quote-found yes, supports-claim no); trust 58 -> 18; a rule citing it cannot carry MUST

## tap-milestones-batch-commits
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The paper says testing each change individually caused unsustainable compute demand. It says milestones run tests selected by reverse dependencies on files changed "since the previous milestone".

## apple-test-plans-umbrella-full-run
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page's text is in its JSON data and is verbatim. The preceding sentence says to run "only the tests relevant to that target to get faster feedback."

## android-test-mapping-directory-rules
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full sentence adds "or any of its subdirectories". The sample file shows `file_patterns` and a separate `postsubmit` group.

## azure-tia-includes-failing-and-new
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is listed under "A robust test selection mechanism".

## develocity-pts-always-chooses
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is in the FAQ "How Does Predictive Test Selection Choose Tests?"

## azure-tia-validate-against-all-tests
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source uses two test tasks, T1 for impacted tests and T2 for all tests: "If there was a failing test in T1, check that T2 reports the same set of failures."

## launchable-observation-mode
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The subset output includes all tests, and Launchable analyses what the subset would have caught and how much time it would have saved.

## leong-selection-remains-open
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is verbatim from the abstract of the ICSE-SEIP 2019 paper, which evaluates algorithms on Google's CI data.

## meta-retrain-model
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The preceding sentence says "our test selection strategy must adapt" because the codebase keeps changing, and retraining is how it adapts.

## develocity-records-selection-reason
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full sentence begins "The Build Scan® indicates which tests were selected…"

## nx-explain-why-affected
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: With `--explain`, Nx prints the explanation and exits, and `--verbose` lists each task with its reasons.

## target-determinator-verbose-explains
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full flag text is "-verbose Whether to explain (messily) why each target is getting run".

## azure-tia-reports-selection
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote only says TIA is part of test reporting at the summary and details levels. Manual validation is a different sentence on the same page that the quote leaves out: "A developer who knows how the SUT and tests are architected could manually validate the test selection using the TIA reporting capabilities."
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## bazel-diff-changed-list-is-correctness-contract
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source sets this rule for one input: bazel-diff's `modifiedFilepaths` list in the query-server API (the same optimisation as `generate-hashes --modified-filepaths`). The claim widens it to any changed-file list fed to any selection.
- correction: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

## bazel-diff-content-hashes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Source files are hashed by their content. "Not its name or commit metadata" is the claim's restatement of that.

## launchable-model-inputs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is one item in a list that also includes test execution history, test characteristics, name and path similarity, and change characteristics.

## meta-predictive-selection-results
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is verbatim from the arXiv abstract, which also says the strategy is "learned from a large dataset of historical test outcomes".

## meta-build-deps-overselect
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source adds that build-dependency selection could exercise as many as a quarter of all tests per change to the mobile codebase.

## tap-affected-targets-rarely-fail
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The paper's dataset is "over 500K CLs, from Feb. 11, to Mar. 11, 2016, that affected more than 5.5 Million unique test targets".

## tap-all-affected-infeasible-per-change
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source only says that Google's churn rate rules out running all affected targets for each change, so TAP postpones them to milestones. Applying this to teams in general, and the phrase "rather than drop safety outright", are not in the source.
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## ekstazi-time-savings
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence ends ", compared to executing all tests". The evaluation covered 615 revisions of 32 open-source projects.

## gha-skipped-required-check-blocks
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says checks of a skipped workflow "will remain in a 'Pending' state". That matches the claim's "does not report its checks".
