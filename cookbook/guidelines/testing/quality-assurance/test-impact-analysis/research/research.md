# Research: test-impact-analysis

Researched 2026-11-24 at base commit `77a898d`. Machine-readable record: `research.json`.

**Summary.** One of the five listed rules holds at its stated strength. **fail-closed-when-unsure** is supported at SHOULD: every safe selection tool read here selects everything when it cannot map a change. That covers Azure TIA, bazel-diff, Turborepo on a shallow checkout, GitHub Actions when the diff times out, and GitLab when there is no push event. The research literature defines a safe technique as one that selects all affected tests.

The other four rules state their checks as fails, i.e. MUST. The sources support them only at SHOULD, or not at all:

- Tools record why each test was selected: Develocity, Nx `--explain`, target-determinator `-verbose`.
- bazel-diff treats the changed-file list as a correctness contract.

But no source requires a written justification per selection, a written account of every changed path, or a statement of each fallback. Tools also select tests for reasons outside the diff: previously failing, new, changed or flaky tests. No source speaks to commit messages or branch names. Path-based mapping is standard (Nx inputs, GitHub Actions path filters, Android TEST_MAPPING), so "file names without their contents is a fail" has no support.

The topic is missing these rules:

- a change of unknown reach selects everything
- shared inputs, such as lockfiles and build configuration, select everything
- select along the dependency graph, not by paths alone
- diff against a known-good base
- run the full suite periodically or after merge
- always select new, changed and recently failing tests
- validate the selection against full runs
- record why each test was selected
- select from every changed file
- measure selection recall and savings against a named study
- path-skipped required checks must still resolve

Apple and Android bear only on running a subset while working and the full set before integrating. Windows has no bearing beyond Azure DevOps TIA.

**Verdicts and the strength the sources support.**

- **fail-closed-when-unsure**: supported at SHOULD (`azure-tia-safe-fallback`, `azure-tia-unknown-file-type-runs-all`, `bazel-diff-fallback-costs-speed`, `rts-safe-selects-all-affected`, `turborepo-shallow-checkout-all-changed`, `gha-diff-timeout-always-runs`, `gitlab-changes-true-without-push`). The tools fall back by design; none words it as a requirement on the user.
- **each-selection-justified-by-diff**: unsupported (`each-selection-justified-by-diff-prior`, `develocity-records-selection-reason`, `nx-explain-why-affected`, `target-determinator-verbose-explains`, `azure-tia-includes-failing-and-new`, `develocity-pts-always-chooses`). Recording a reason per selection holds at SHOULD, but tools legitimately select tests for non-diff reasons, so "justified by a path or hunk, or fail" is not supported.
- **every-changed-path-accounted-for**: unsupported (`every-changed-path-accounted-for-prior`, `bazel-diff-changed-list-is-correctness-contract`, `azure-tia-unknown-file-type-runs-all`). Every changed file must feed the selection and an unmappable one triggers the full run, but no source requires naming each path in the output.
- **fail-closed-is-stated**: unsupported (`fail-closed-is-stated-prior`, `bazel-diff-fallback-costs-speed`, `develocity-records-selection-reason`). Logging which path a run took holds at SHOULD; no source makes an unstated narrowing a fail.
- **reasoning-cites-diff-contents**: unsupported (`reasoning-cites-diff-contents-prior`, `bazel-diff-content-hashes`, `nx-selects-by-task-inputs`, `android-test-mapping-directory-rules`, `gha-paths-filter-any-match-runs`). bazel-diff hashes contents, but path-based selection is the platform norm, and no source addresses commit messages or branch names.
- **unknown-reach-selects-everything**: new, SHOULD (`azure-tia-safe-fallback`, `azure-tia-unknown-file-type-runs-all`, `bazel-diff-fallback-costs-speed`, `turborepo-shallow-checkout-all-changed`, `gha-diff-timeout-always-runs`, `gitlab-changes-true-without-push`, `rts-safe-selects-all-affected`).
- **shared-inputs-select-everything**: new, SHOULD (`nx-lockfile-affects-every-task`, `pants-lockfile-change-all-users`, `bazel-diff-hashes-all-inputs`, `hammant-resource-files-unmapped`).
- **select-by-dependency-graph-not-paths-alone**: new, SHOULD (`nx-selects-by-task-inputs`, `nx-dependson-not-affected`, `bazel-rdeps-operator`, `bazel-tests-operator`, `pants-changed-dependents`, `turborepo-affected`, `tap-affected-targets-reverse-dependencies`, `gradle-up-to-date-tests`, `gha-paths-filter-any-match-runs`, `mill-module-graph-granularity`, `single-language-rts-unsafe`, `rtslinux-ekstazi-misses-dependencies`, `hammant-coverage-builds-the-map`).
- **diff-against-a-known-good-base**: new, SHOULD (`nx-base-latest-successful-commit`, `gitlab-compare-to-base`, `target-determinator-changed-targets`, `turborepo-shallow-checkout-all-changed`).
- **run-the-full-suite-periodically**: new, SHOULD (`azure-tia-periodic-full-run`, `launchable-full-suite-later-in-pipeline`, `launchable-full-suite-nightly`, `develocity-remaining-tests-mode`, `develocity-pts-trades-comprehensiveness`, `mill-thorough-tests-after-merge`, `hammant-nightly-all-tests`, `tap-milestones-batch-commits`, `apple-test-plans-umbrella-full-run`, `android-test-mapping-directory-rules`).
- **always-select-new-changed-and-failing-tests**: new, SHOULD (`azure-tia-includes-failing-and-new`, `develocity-pts-always-chooses`).
- **validate-selection-against-full-runs**: new, SHOULD (`azure-tia-validate-against-all-tests`, `launchable-observation-mode`, `leong-selection-remains-open`, `meta-retrain-model`).
- **record-why-each-test-was-selected**: new, SHOULD (`develocity-records-selection-reason`, `nx-explain-why-affected`, `target-determinator-verbose-explains`, `azure-tia-reports-selection`, `bazel-diff-fallback-costs-speed`).
- **select-from-every-changed-file**: new, SHOULD (`bazel-diff-changed-list-is-correctness-contract`, `bazel-diff-content-hashes`, `launchable-model-inputs`, `azure-tia-unknown-file-type-runs-all`).
- **measure-selection-recall-and-savings**: new, SHOULD (`meta-predictive-selection-results`, `meta-build-deps-overselect`, `tap-affected-targets-rarely-fail`, `tap-all-affected-infeasible-per-change`, `ekstazi-time-savings`, `rtslinux-ekstazi-misses-dependencies`, `leong-selection-remains-open`).
- **path-skipped-required-checks-resolve**: new, SHOULD (`gha-skipped-required-check-blocks`, `gha-paths-filter-any-match-runs`).

## Best practices

- **Selection is judged on safety first.** A safe technique selects every affected test; a precise one selects no unaffected test (`rts-safe-selects-all-affected`).
- **Fall back to the full run rather than guess.** bazel-diff's design is that a fallback costs speed, never correctness, and its log says which path each run took (`bazel-diff-fallback-costs-speed`).
- **The changed-file list is a correctness contract.** A changed file left off it silently drops the targets it impacts (`bazel-diff-changed-list-is-correctness-contract`).
- **Affected means transitively dependent.** Google TAP treats as affected every test target that directly or indirectly depends on the modified files (`tap-affected-targets-reverse-dependencies`).
- **Keep a full run behind the subset.** Run the full suite later in the pipeline (`launchable-full-suite-later-in-pipeline`) and keep the nightly full run (`launchable-full-suite-nightly`).
- **The four Verify rules as written rest on prior cookbook text only.** No research source requires them at fail strength: `each-selection-justified-by-diff-prior`, `every-changed-path-accounted-for-prior`, `fail-closed-is-stated-prior`, `reasoning-cites-diff-contents-prior`.

## Known solutions

- **Build-graph queries (Bazel).** `rdeps` gives the reverse dependencies of a changed set within a universe (`bazel-rdeps-operator`), and `tests` narrows that to test rules (`bazel-tests-operator`).
- **Changed-target tools for Bazel.**
  - target-determinator computes the targets changed between two commits (`target-determinator-changed-targets`) and can explain why each target runs (`target-determinator-verbose-explains`).
  - bazel-diff hashes every attribute and input of a target (`bazel-diff-hashes-all-inputs`), and hashes source files by content (`bazel-diff-content-hashes`).
- **Monorepo tools.**
  - Pants runs only directly changed files unless asked for dependents (`pants-changed-dependents`).
  - Turborepo's `--affected` runs only the packages affected on the branch (`turborepo-affected`).
- **Dependency selection over-selects.** At Meta it said "impacted" more often than necessary (`meta-build-deps-overselect`). At Google, only 63K of 5.5 million affected test targets ever failed over a month of 500K+ changes (`tap-affected-targets-rarely-fail`). Google batches commits into milestones rather than run every affected target per change (`tap-milestones-batch-commits`).
- **Predictive (learned) selection.**
  - Meta's deployed model halved testing cost while still reporting over 95% of individual test failures and over 99.9% of faulty changes (`meta-predictive-selection-results`).
  - Launchable learns from the historical link between changed files and failed tests (`launchable-model-inputs`). It offers an observation mode to compare the subset against the full run (`launchable-observation-mode`).
  - Develocity always selects tests that are recently new, changed, failed or flaky (`develocity-pts-always-chooses`). It concedes that it trades comprehensiveness for speed (`develocity-pts-trades-comprehensiveness`). It pairs selection with a remaining-tests mode so all tests are eventually run (`develocity-remaining-tests-mode`). It records the reason for every selected and unselected test (`develocity-records-selection-reason`).
- **Dynamic file-dependency selection.**
  - Ekstazi cut end-to-end test time by 32% on average, and 54% on longer suites, across 615 revisions of 32 Java projects (`ekstazi-time-savings`).
  - Single-language tracers are unsafe for multilingual projects (`single-language-rts-unsafe`): Ekstazi collected only 16.99% of the dependencies an OS-level monitor found (`rtslinux-ekstazi-misses-dependencies`).

## Platform guidelines

- **Web and JavaScript monorepos (Nx, Turborepo).**
  - Nx selects a task when the change touches one of its declared inputs (`nx-selects-by-task-inputs`). A `dependsOn` edge alone does not make a task affected (`nx-dependson-not-affected`). A lockfile change affects every task by default (`nx-lockfile-affects-every-task`).
  - Nx recommends diffing against the latest successful commit on main (`nx-base-latest-successful-commit`). It can explain why each task was affected (`nx-explain-why-affected`).
  - Turborepo treats every package as changed when the checkout is too shallow (`turborepo-shallow-checkout-all-changed`).
- **Python and polyglot (Pants).** A change to any dependency in a lockfile is treated as changing every user of any dependency (`pants-lockfile-change-all-users`).
- **Windows and .NET (Azure DevOps TIA).**
  - TIA falls back to all tests for any commit it cannot understand (`azure-tia-safe-fallback`) and for any unknown file type (`azure-tia-unknown-file-type-runs-all`).
  - Microsoft recommends a periodic full run as the means to regulate selection (`azure-tia-periodic-full-run`). TIA includes previously failing and newly added tests (`azure-tia-includes-failing-and-new`).
  - To validate the selection, run the TIA-selected tests, then all tests (`azure-tia-validate-against-all-tests`). TIA reports its selection in the test summary and details (`azure-tia-reports-selection`).
- **CI services.**
  - A GitHub Actions path filter runs a workflow on any matching path (`gha-paths-filter-any-match-runs`) and always runs it when the diff times out (`gha-diff-timeout-always-runs`). A path-skipped workflow blocks a pull request that requires its checks (`gha-skipped-required-check-blocks`).
  - GitLab's `rules:changes` is true when there is no push event (`gitlab-changes-true-without-push`). GitLab has the team name a base with `compare_to` (`gitlab-compare-to-base`).
- **JVM (Gradle).** In a well-defined build, tests rerun only when the tests or the production code change (`gradle-up-to-date-tests`).
- **Android.** TEST_MAPPING maps a directory, optionally narrowed by file patterns, to the presubmit tests that run when files in it change (`android-test-mapping-directory-rules`).
- **Apple.** Xcode test plans run a target's own tests for fast feedback and the full umbrella scheme before integrating (`apple-test-plans-umbrella-full-run`). Apple gives no change-based selection guidance.

## The expert's view

- **Know where the map comes from.** Coverage or instrumentation recorded while tests run builds it (`hammant-coverage-builds-the-map`). Non-code resource files are its blind spot (`hammant-resource-files-unmapped`).
- **Granularity limits precision.** Dependency selection is only as fine as the module graph (`mill-module-graph-granularity`).
- **Keep a heuristic-free run behind any heuristic.** Run thoroughly after merge (`mill-thorough-tests-after-merge`), and keep the nightly all-tests job (`hammant-nightly-all-tests`).
- **Retrain a learned selector.** A model left alone drifts from the code it predicts (`meta-retrain-model`).
- **Running every affected target per change stops scaling.** At Google's churn it is infeasible, which is why TAP batches (`tap-all-affected-infeasible-per-change`).
- **Do not trust reported selection results without replaying them on your own history.** Google's replay found that history-based algorithms underperformed earlier reports, and selection remains largely open (`leong-selection-remains-open`).
