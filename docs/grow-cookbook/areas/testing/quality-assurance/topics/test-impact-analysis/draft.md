---
id: e981def5-83d1-4c99-a5f3-3566270f618d
title: Test Impact Analysis
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Choosing the tests to run for a change: select along the dependency graph, run everything when unsure, keep a full run behind it, and record why."
platforms: []
tags:
  - testing
  - ci
  - test-selection
  - test-impact-analysis
  - monorepo
depends-on: []
related:
  - 4f5fe9ef-1bf8-4354-92c7-92d9e28673b8
  - a8f9c003-e970-4f28-bb7d-30a23b891b3f
  - 4825088c-7d3a-4ef3-8c1b-c5b70b88da0d
references:
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis
  - https://nx.dev/ci/features/affected
  - https://turborepo.dev/docs/reference/run
  - https://bazel.build/query/language
  - https://github.com/bazel-contrib/target-determinator
  - https://github.com/Tinder/bazel-diff
  - https://www.pantsbuild.org/stable/docs/using-pants/advanced-target-selection
  - https://docs.develocity.ai/predictive-test-selection/
  - https://docs.gradle.org/current/userguide/java_testing.html
  - https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  - https://docs.gitlab.com/ci/yaml/
  - https://source.android.com/docs/core/tests/development/test-mapping
  - https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback
  - https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/
  - https://arxiv.org/abs/1810.05286
  - https://web.eecs.umich.edu/~xwangsd/courses/w23/readings/googletest.pdf
  - https://mpapad.github.io/publications/pdfs/ICSE-SEIP2019.pdf
  - https://users.ece.utexas.edu/~gligoric/papers/abstracts/GligoricETAL15Ekstazi.txt
  - https://par.nsf.gov/servlets/purl/10055460
  - https://help.launchableinc.com/features/predictive-test-selection/use-cases-for-predictive-test-selection/
  - https://help.launchableinc.com/features/predictive-test-selection/how-launchable-selects-tests/
  - https://help.launchableinc.com/features/predictive-test-selection/observing-subset-behavior/
  - https://martinfowler.com/articles/rise-test-impact-analysis.html
  - https://mill-build.org/blog/3-selective-testing.html
approved-by: ""
approved-date: ""
triggers:
  - pre-pr
  - configuration
---

# Test Impact Analysis

When a change runs only the tests it can affect, choose them along the dependency graph from every file that changed against a known-good base, and run everything whenever the analysis cannot tell what a change reaches. Always add recently new, changed and failing tests, keep a full run behind the subset, and record why each test was or was not selected, so the selection can be checked against full runs and measured on the team's own history.

This guideline covers how any team that tests a product chooses which tests or test targets to run for a change: the selection methods (build-graph affected-target queries, coverage-based mapping, path filters and predictive selection), how a selection fails safe when it cannot map a change, which changes select everything, the full run kept behind a selection, and what a selection records so it can be checked. Excluding quarantined tests from the gating job is a selection by tag, not by change, and belongs to [adc.guideline.testing.flaky-test-quarantine](cookbook:4f5fe9ef-1bf8-4354-92c7-92d9e28673b8); how many tests a suite holds at each level belongs to [adc.guideline.planning.testing.test-pyramid](cookbook:a8f9c003-e970-4f28-bb7d-30a23b891b3f); classifying a selected test that failed belongs to [adc.guideline.testing.quality-assurance.test-failure-triage](cookbook:4825088c-7d3a-4ef3-8c1b-c5b70b88da0d). Following this guideline means keeping every MUST rule below, keeping each SHOULD rule or stating why a selection departs from it, and using each MAY rule where it helps.

## Rules

- **fail-closed-when-unsure**: When a selection is unsure which tests a changed path can affect, it SHOULD include every test the path might affect. (claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, rts-safe-selects-all-affected, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push)
- **each-selection-justified-by-diff**: This MUST hold: Every included site is justified in the prose by a named path or hunk from the commit range. A site in the list with no stated reason is a fail. (claim: each-selection-justified-by-diff-prior)
- **every-changed-path-accounted-for**: This MUST hold: Every residue path handed to the analysis is accounted for: either attributed to sites, or named as unattributable with its candidate sites included anyway. A residue path that goes unmentioned is a fail. (claim: every-changed-path-accounted-for-prior)
- **fail-closed-is-stated**: This MUST hold: Fail-closed is visible in the output: where the analysis was unsure, the prose says so and the sites are included. An answer that narrows the list on a judgment call it does not state is a fail. (claim: fail-closed-is-stated-prior)
- **reasoning-cites-diff-contents**: This MUST hold: The reasoning cites the diff. A judgment resting only on commit messages, branch names, or file names without their contents is a fail. (claim: reasoning-cites-diff-contents-prior)
- **unknown-reach-selects-everything**: A change whose reach the selection cannot determine, such as a commit or a file type it cannot map, a checkout too shallow to diff, a diff that times out or a pipeline with no push to diff, SHOULD select every test. (claims: azure-tia-safe-fallback, azure-tia-unknown-file-type-runs-all, bazel-diff-fallback-costs-speed, turborepo-shallow-checkout-all-changed, gha-diff-timeout-always-runs, gitlab-changes-true-without-push, rts-safe-selects-all-affected)
- **shared-inputs-select-everything**: A change to an input that many tests share, and that the selection cannot trace to particular tests, SHOULD select every test that may use that input. (claims: nx-lockfile-affects-every-task, pants-lockfile-change-all-users, bazel-diff-hashes-all-inputs, hammant-resource-files-unmapped)
- **select-by-dependency-graph-not-paths-alone**: A selection SHOULD choose the tests that directly or indirectly depend on what changed, from the build's declared dependencies and inputs or from coverage recorded while the tests ran, rather than from path patterns alone. (claims: nx-selects-by-task-inputs, nx-dependson-not-affected, bazel-rdeps-operator, bazel-tests-operator, pants-changed-dependents, turborepo-affected, tap-affected-targets-reverse-dependencies, gradle-up-to-date-tests, gha-paths-filter-any-match-runs, mill-module-graph-granularity, single-language-rts-unsafe, rtslinux-ekstazi-misses-dependencies, hammant-coverage-builds-the-map)
- **diff-against-a-known-good-base**: A selection SHOULD compute what changed between two named revisions, taking as its base a known-good one such as the latest commit on the main branch whose CI run succeeded. (claims: nx-base-latest-successful-commit, gitlab-compare-to-base, target-determinator-changed-targets, turborepo-shallow-checkout-all-changed)
- **select-from-every-changed-file**: The list of changed files a selection works from SHOULD include every file that actually changed. (claims: bazel-diff-changed-list-is-correctness-contract, launchable-model-inputs, azure-tia-unknown-file-type-runs-all)
- **decide-change-by-content**: A selection MAY decide that a source file changed from a hash of its content rather than from its name or the commit metadata. (claim: bazel-diff-content-hashes)
- **always-select-new-changed-and-failing-tests**: A selection SHOULD always include the tests that are recently new, recently changed, recently failed or recently flaky, whatever the change-based analysis selects. (claims: azure-tia-includes-failing-and-new, develocity-pts-always-chooses)
- **run-the-full-suite-periodically**: A team that runs a selected subset SHOULD also run the full suite at some later point in its pipeline or on a schedule, such as after merge, nightly or before release, so that every test is eventually run. (claims: azure-tia-periodic-full-run, launchable-full-suite-later-in-pipeline, launchable-full-suite-nightly, develocity-remaining-tests-mode, develocity-pts-trades-comprehensiveness, mill-thorough-tests-after-merge, hammant-nightly-all-tests, tap-milestones-batch-commits, apple-test-plans-umbrella-full-run, android-test-mapping-directory-rules)
- **validate-selection-against-full-runs**: Before relying on a selection, a team SHOULD compare it with full runs of the same changes and confirm that the full runs report no failure the selection missed. (claims: azure-tia-validate-against-all-tests, launchable-observation-mode, leong-selection-remains-open)
- **retrain-a-learned-selector**: A team that selects tests with a learned model SHOULD retrain it regularly on recent test results. (claims: meta-retrain-model, launchable-full-suite-nightly)
- **record-why-each-test-was-selected**: A selection SHOULD record which tests it selected and which it did not, with the reason for each. (claims: develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-reports-selection)
- **log-each-fallback**: A selection SHOULD log, for each run, whether it selected incrementally or fell back to a full computation. (claim: bazel-diff-fallback-costs-speed)
- **measure-selection-recall-and-savings**: A team SHOULD measure, on its own change history, the share of test failures and faulty changes its selection still reports and the testing time or cost it saves. (claims: meta-predictive-selection-results, meta-build-deps-overselect, tap-affected-targets-rarely-fail, tap-all-affected-infeasible-per-change, ekstazi-time-savings, rtslinux-ekstazi-misses-dependencies, leong-selection-remains-open)
- **path-skipped-required-checks-resolve**: Where a path filter can skip a workflow whose checks a pull request requires, the team SHOULD make sure those required checks still resolve, so a skipped workflow does not block the merge. (claims: gha-skipped-required-check-blocks, gha-paths-filter-any-match-runs)

## Selecting tests for a change

This section is informative: it shows one way to keep the rules, not a required method.

1. Fix the two revisions. Diff the head against a known-good base. Nx recommends the latest commit on `main` whose CI run succeeded; GitLab's `rules:changes:compare_to` names the branch to compare against where a pipeline has no natural base; Target Determinator computes the Bazel targets changed between two Git commits.
2. Fetch enough history. Turborepo needs the whole history between base and head, and treats every package as changed when the checkout is too shallow.
3. Take every changed file. bazel-diff treats its list of modified paths as a correctness contract: a truly changed file left off it has its impacted targets missed. bazel-diff hashes source files by content, and hashes every attribute and input of a target, so any change to a target's inputs marks it impacted.
4. Walk the graph from the changed set to the tests:
   - Bazel: `rdeps(universe, changed)` gives the reverse dependencies, and `tests(...)` narrows them to test rules.
   - Nx: a task is affected when the change touches one of its declared inputs; a `dependsOn` edge alone does not make a task affected, so declare inputs accurately.
   - Pants: `--changed-since` runs only the directly changed files unless `--changed-dependents` adds the targets that depend on them.
   - Turborepo: `--affected` runs only the packages affected by changes on the current branch.
   - Gradle: in a well-defined build the test task reruns only when the tests or the production code change.
   - Coverage-based tools build the map from tests to production code by recording coverage or instrumentation while each test runs. A tracer inside one language runtime misses dependencies that cross languages or processes.
5. Fall back to everything when the map runs out. Azure DevOps Test Impact Analysis runs all tests for any commit it cannot understand and for any unknown file type, such as HTML or CSS. GitHub Actions runs a path-filtered workflow whenever generating the diff times out. GitLab's `rules:changes` is true for new-branch pipelines and pipelines with no push event unless `compare_to` names a base.
6. Treat shared inputs as reaching everything that uses them. By default Nx treats a lockfile change as affecting every task, and Pants treats a change to any dependency in a lockfile as changing all users of any dependency. This guideline does not yet settle which shared inputs select everything (lockfiles, build and CI configuration, toolchains, shared fixtures); the tools differ.
7. Add the tests history marks. Azure TIA adds previously failing and newly added tests; Develocity Predictive Test Selection always chooses recently new, changed, failed or flaky tests.
8. Record the selection. Develocity build scans list which tests were selected and which were not, with the reason; Nx's `--explain` shows why tasks are affected; Target Determinator's `-verbose` explains why each target runs; bazel-diff's log says whether each run was incremental or a fallback.
9. Keep a full run behind the subset, later in the pipeline or on a schedule: Azure TIA's configured periodic full run, Launchable's later and nightly full runs, Develocity's remaining-tests mode in nightly and pre-release stages, a heuristic-free run after merge, Google TAP's milestones, Android's postsubmit groups, Xcode's umbrella scheme before integrating.
10. Check the selection before trusting it. Run the selected tests and then all tests and confirm the same failures (Azure TIA), or use Launchable's observation mode, which runs the full suite and records what the subset would have run.

A GitHub Actions workflow skipped by a `paths` filter does not report its checks, so a pull request that requires them stays blocked; a path filter also selects whole workflows by pattern with no knowledge of dependencies.

## Examples

This section is informative; the record below is an illustration, not a required format.

A selection record for one change:

```text
Base: 4e1f0a2 (latest main commit with a green CI run)   Head: 9c7d3b1
Changed files (3): lib/pricing/discount.ts, lib/pricing/discount.test.ts, package-lock.json
Fallback: yes. package-lock.json is a shared input the graph cannot trace to tests,
  so every test that uses an npm dependency is selected.
Selected by graph: pricing:test (input lib/pricing/discount.ts), checkout:test
  (depends on pricing), cart:test (depends on pricing)
Selected by history: search:test (failed on the previous run)
Not selected: tools:test (uses no npm dependency and has no path to a changed file)
Full suite: runs after merge to main
```

## What a reviewer looks for

Checks that the selection worked from every file changed between two named revisions, with a known-good base, and walked the dependency graph or recorded coverage to the tests rather than path patterns alone. Checks that every change of unknown reach, and every change to a shared input the selection cannot trace, selected everything, and that each judgment the analysis was unsure of included the tests it might affect and said so. Checks that each selected test is justified by a path or hunk of the diff, that every changed path is attributed or named as unattributable, that the reasoning cites the diff's contents, and that recently new, changed and failing tests were added. Checks that the selection records what it selected, what it did not and why, and whether it fell back; that a full run stands behind the subset; that the selection has been compared with full runs and measured on the team's history; that a learned selector is retrained; and that a path-skipped required check cannot block a merge.

## A complete review must establish

- Each MUST rule is kept, with no exception: `each-selection-justified-by-diff`, `every-changed-path-accounted-for`, `fail-closed-is-stated`, `reasoning-cites-diff-contents`.
- Each SHOULD rule is kept or its departure is stated: `fail-closed-when-unsure`, `unknown-reach-selects-everything`, `shared-inputs-select-everything`, `select-by-dependency-graph-not-paths-alone`, `diff-against-a-known-good-base`, `select-from-every-changed-file`, `always-select-new-changed-and-failing-tests`, `run-the-full-suite-periodically`, `validate-selection-against-full-runs`, `retrain-a-learned-selector`, `record-why-each-test-was-selected`, `log-each-fallback`, `measure-selection-recall-and-savings`, `path-skipped-required-checks-resolve`.
- Each MAY rule is noted where it was used: `decide-change-by-content`.

## A build must establish

- `fail-closed-when-unsure`: each changed path the selection was unsure of has every test it might affect included.
- `each-selection-justified-by-diff`: each included site is justified by a named path or hunk from the commit range.
- `every-changed-path-accounted-for`: each residue path is attributed to sites or named as unattributable with its candidate sites included.
- `fail-closed-is-stated`: each place the analysis was unsure is stated, with its sites included.
- `reasoning-cites-diff-contents`: the reasoning cites the diff, not only commit messages, branch names or file names.
- `unknown-reach-selects-everything`: each change of unknown reach selected every test.
- `shared-inputs-select-everything`: each change to an untraceable shared input selected every test that may use it.
- `select-by-dependency-graph-not-paths-alone`: the tests were chosen from declared dependencies and inputs or recorded coverage, not path patterns alone.
- `diff-against-a-known-good-base`: the changes were computed between two named revisions with a known-good base.
- `select-from-every-changed-file`: the changed-file list holds every file that changed.
- `decide-change-by-content`: where used, a file's change is decided from a hash of its content.
- `always-select-new-changed-and-failing-tests`: recently new, changed, failed and flaky tests are selected.
- `run-the-full-suite-periodically`: a full-suite run is set later in the pipeline or on a schedule.
- `validate-selection-against-full-runs`: the selection has been compared with full runs of the same changes, with no missed failure.
- `retrain-a-learned-selector`: a learned selection model is retrained on recent test results.
- `record-why-each-test-was-selected`: the selected and unselected tests are recorded with the reason for each.
- `log-each-fallback`: each run logs whether it was incremental or a full fallback.
- `measure-selection-recall-and-savings`: the failures still reported and the time or cost saved are measured on the team's history.
- `path-skipped-required-checks-resolve`: no required check is left unresolved by a path-skipped workflow.

## Rationale

This section is informative.

A selection is judged first on safety, selecting every affected test, and then on precision, selecting no unaffected one. Every safe selection tool read falls back to running everything when it cannot map a change: Azure DevOps TIA for commits and file types it cannot understand, which Microsoft calls good from a safety perspective; bazel-diff, whose fallback costs speed but never correctness; Turborepo on a shallow checkout; GitHub Actions when the diff times out; GitLab when there is no push event. That is why unsure and unknown changes select widely. The tools fall back by design, and none words it as a requirement on the user, so the rules are recommendations.

Affected means transitively dependent: Google's TAP treats as affected every test target that directly or indirectly depends on the modified files, and Bazel, Nx, Pants and Turborepo all compute it from the build graph. Path filters select whole workflows by pattern with no knowledge of dependencies, Nx carries a change only through declared inputs, and dependency selection is only as fine as the module graph it walks. Coverage maps have blind spots too: Ekstazi, a JVM-level tracer, collected only 16.99% of the file dependencies an OS-level monitor found on the same projects (Celik et al., ESEC/FSE 2017, the authors comparing their own tool with an earlier one from their group), and in the Testar tool Hammant describes, a resource file the user does not list re-runs all tests. Nx's and Pants' lockfile defaults show how tools treat a shared input they cannot trace; Pants' documentation states it as a limit of its own tool, and the research holds the claim at reduced trust.

Dependency selection over-selects, which is the cost the full run and measurement keep in view. At Meta it marked tests as impacted more often than necessary; at Google only 63K of 5.5 million affected test targets ever failed over 500K changes in a month (Memon et al., ICSE-SEIP 2017). Google's churn rules out running every affected target per change, so TAP batches commits into milestones. Ekstazi cut end-to-end test time by 32% on average and 54% on longer suites across 615 revisions of 32 Java projects (Gligoric et al., ISSTA 2015). Meta's predictive selection halved testing infrastructure cost while still reporting over 95% of individual test failures and over 99.9% of faulty changes (Machalica et al., arXiv preprint, owner-reported and not replicated). Leong et al. replayed Google's history and found history-based algorithms performed worse than earlier reports suggested, which is why a team measures and validates on its own history rather than adopting a published figure.

A full run stays behind the subset in every source that selects: Microsoft recommends a periodic full run as the means to regulate selection, Launchable advises a later full run and keeping the nightly one, Develocity concedes that predictive selection trades comprehensiveness for speed and pairs it with a remaining-tests mode, and Mill's author runs a heuristic-free suite after merge. Hammant mentions a nightly all-tests job only as something teams might choose and criticises it as delaying bad news; the research holds that claim at low trust. Apple's guidance is to run one target's tests while working and the full umbrella scheme before integrating, and Android's TEST_MAPPING splits presubmit from postsubmit groups. Azure TIA and Develocity both add tests selected for reasons outside the diff: previously or recently failing, newly added, recently changed or flaky. Develocity, Nx and Target Determinator record or explain why each test or target was selected; Azure TIA reports its selection in the run's test summary and details, though the research does not establish what fields that report carries. Launchable and Meta retrain their learned models on recent results.

The four Verify checks are kept as the owner's text at must-hold strength, which the research could not support. Tools record a reason per selection and treat every changed file as an input, which supports recording and completeness at SHOULD, but no source requires a written justification per selection, a written account of every changed path or a statement of each fallback, and tools select tests for reasons outside the diff. No source speaks to judgments resting on commit messages or branch names, and path-based mapping (Nx inputs, GitHub Actions path filters, Android TEST_MAPPING) is the platform norm. Left to the owner: the cadence and place of the full run; whether predictive selection may gate a merge on its own; whether the four checks keep their strength; whether a test selected for a reason outside the diff counts as justified; which file classes a team may declare unable to affect tests, and who approves that list; and which shared inputs select everything.

## References

This section is informative; every reference below is informative, and none is normative.

- Microsoft, *Test Impact Analysis* (Azure Pipelines): https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis
- Nx, *Affected*: https://nx.dev/ci/features/affected
- Turborepo, *run* reference: https://turborepo.dev/docs/reference/run
- Bazel, *Query language*: https://bazel.build/query/language
- Target Determinator: https://github.com/bazel-contrib/target-determinator
- bazel-diff: https://github.com/Tinder/bazel-diff
- Pants, *Advanced target selection*: https://www.pantsbuild.org/stable/docs/using-pants/advanced-target-selection
- Develocity, *Predictive Test Selection*: https://docs.develocity.ai/predictive-test-selection/
- Gradle, *Testing in Java & JVM projects*: https://docs.gradle.org/current/userguide/java_testing.html
- GitHub Actions, *Workflow syntax*: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- GitLab, *CI/CD YAML syntax reference*: https://docs.gitlab.com/ci/yaml/
- Android, *Test mapping*: https://source.android.com/docs/core/tests/development/test-mapping
- Apple, *Organizing tests to improve feedback*: https://developer.apple.com/documentation/xcode/organizing-tests-to-improve-feedback
- Meta Engineering, *Predictive test selection*: https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/
- Machalica et al., *Predictive Test Selection* (arXiv 1810.05286): https://arxiv.org/abs/1810.05286
- Memon et al., *Taming Google-Scale Continuous Testing* (ICSE-SEIP 2017): https://web.eecs.umich.edu/~xwangsd/courses/w23/readings/googletest.pdf
- Leong et al., *Assessing Transition-based Test Selection Algorithms at Google* (ICSE-SEIP 2019): https://mpapad.github.io/publications/pdfs/ICSE-SEIP2019.pdf
- Gligoric, Eloussi and Marinov, *Practical Regression Test Selection with Dynamic File Dependencies* (ISSTA 2015): https://users.ece.utexas.edu/~gligoric/papers/abstracts/GligoricETAL15Ekstazi.txt
- Celik et al., *Regression Test Selection Across JVM Boundaries* (ESEC/FSE 2017): https://par.nsf.gov/servlets/purl/10055460
- Launchable, *Use cases*, *How Launchable selects tests* and *Observing subset behavior*: https://help.launchableinc.com/features/predictive-test-selection/use-cases-for-predictive-test-selection/, https://help.launchableinc.com/features/predictive-test-selection/how-launchable-selects-tests/, https://help.launchableinc.com/features/predictive-test-selection/observing-subset-behavior/
- Paul Hammant, *The Rise of Test Impact Analysis*: https://martinfowler.com/articles/rise-test-impact-analysis.html
- Mill, *Selective testing*: https://mill-build.org/blog/3-selective-testing.html

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
