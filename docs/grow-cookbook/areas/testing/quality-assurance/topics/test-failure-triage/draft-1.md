---
id: 4825088c-7d3a-4ef3-8c1b-c5b70b88da0d
title: Test Failure Triage
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Triaging a failed test: gather the evidence, give each failure one disposition from a fixed set, and state what was observed and how sure the verdict is."
platforms: []
tags:
  - testing
  - triage
  - flaky
  - ci
  - failure-classification
depends-on: []
related:
  - 4f5fe9ef-1bf8-4354-92c7-92d9e28673b8
  - 05d00147-5c49-42d8-bdbd-cf8fd7dc2379
  - 3d9f5176-afaa-47a2-8a89-fc0402f3dff2
  - 2041fbd9-d210-485e-9a3a-b2d8295ed924
  - f77eeffe-2699-4028-9195-4bfc23c75e91
references:
  - https://playwright.dev/docs/test-retries
  - https://playwright.dev/docs/trace-viewer
  - https://playwright.dev/docs/test-annotations
  - https://docs.pytest.org/en/stable/how-to/skipping.html
  - https://docs.pytest.org/en/stable/explanation/flaky.html
  - https://github.com/pytest-dev/pytest-rerunfailures
  - https://maven.apache.org/surefire/maven-surefire-plugin/examples/rerun-failing-tests.html
  - https://github.com/gradle/test-retry-gradle-plugin
  - https://developer.apple.com/tutorials/data/documentation/xcode/running-tests-and-interpreting-results.json
  - https://developer.android.com/training/testing/instrumented-tests/androidx-test-libraries/runner
  - https://firebase.google.com/docs/test-lab/reference/toolresults/rest/v1beta3/OutcomeSummary
  - https://firebase.google.com/docs/test-lab/troubleshooting?hl=en
  - https://firebase.google.com/docs/test-lab/android/analyzing-results
  - https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
  - https://docs.gitlab.com/ci/testing/unit_test_reports/
  - https://learn.microsoft.com/en-us/azure/devops/pipelines/test/flaky-test-management?view=azure-devops
  - https://circleci.com/docs/guides/insights/insights-tests/
  - https://buildkite.com/docs/test-engine/flaky-test-management
  - https://docs.datadoghq.com/tests/flaky_management/
  - https://docs.trunk.io/flaky-tests/detection
  - https://jestjs.io/docs/snapshot-testing
  - https://git-scm.com/docs/git-bisect
  - https://raw.githubusercontent.com/mozilla/treeherder/master/treeherder/model/fixtures/failure_classification.json
  - https://firefox-source-docs.mozilla.org/testing/sheriffed-intermittents/index.html
  - https://wiki.mozilla.org/Sheriffing/How_To/Intermittent_bugs
  - https://wiki.mozilla.org/Sheriffing/How_To/Treeherder
  - https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
  - https://www.chromium.org/developers/tree-sheriffs/handling-a-failing-test/
  - https://chromium.googlesource.com/chromium/src/+/HEAD/docs/gardener.md
  - https://engineering.fb.com/2020/12/10/developer-tools/probabilistic-flakiness/
  - https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf
  - https://www.cs.ubc.ca/~rtholmes/papers/fse_2017_labuschange.pdf
  - https://www.microsoft.com/en-us/research/wp-content/uploads/2019/11/LamETAL19RootFinder.pdf
  - https://eprints.whiterose.ac.uk/id/eprint/230095/1/parry2021.pdf
  - https://archive.dni.gov/files/documents/ICD/ICD-203.pdf
  - https://abseil.io/resources/swe-book/html/ch11.html
  - https://abseil.io/resources/swe-book/html/ch12.html
  - https://abseil.io/resources/swe-book/html/ch14.html
  - https://martinfowler.com/articles/nonDeterminism.html
  - https://dwheeler.com/essays/debugging-agans.html
approved-by: ""
approved-date: ""
triggers: []
---

# Test Failure Triage

Before anyone fixes a failed automated test, gather its evidence and give the failure exactly one disposition from a fixed set: a product bug, a flake, an environment fault, a test made stale by an intended behavior change, or uncertain. Each verdict states what was observed and where, cites the signal its disposition rests on, and says how confident it is. A pass on retry marks a test flaky but does not clear the product of a bug, and a failure the evidence cannot settle stays uncertain rather than being forced into a class.

This guideline covers how any team that tests a product triages a failed automated test: who triages it, what evidence is gathered first, which disposition the failure is given, what separates each disposition from the others, and how the verdict states its evidence and its confidence. What happens to a test once it is known to be flaky (quarantine, the retry rule, the fix-or-delete lifecycle) belongs to [adc.guideline.testing.flaky-test-quarantine](cookbook:4f5fe9ef-1bf8-4354-92c7-92d9e28673b8) and [adc.guideline.testing.flaky-test-prevention](cookbook:05d00147-5c49-42d8-bdbd-cf8fd7dc2379); production incidents belong to [adc.guideline.shipping.incident-response](cookbook:2041fbd9-d210-485e-9a3a-b2d8295ed924); tracking the bug a triage turns up belongs to [adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91). Following this guideline means keeping every MUST rule below, keeping each SHOULD rule or stating why a triage departs from it, and using each MAY rule where it helps.

## Rules

- **every-failure-gets-one-disposition**: Every failure put to triage MUST receive exactly one disposition: no failure is left without one, and no disposition is given for a failure that was not in the input. (claims: ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete)
- **disposition-from-fixed-set**: Each disposition MUST be one value from a fixed set that covers a product bug, a flake, an environment fault, a test made stale by an intended behavior change, and uncertain. (claims: ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete, pg-firebase-inconclusive-vs-failure, ks-trunk-broken-vs-flaky)
- **never-force-a-verdict**: Where the evidence does not settle which disposition a failure has, the triager SHOULD give it the uncertain disposition rather than force it into another. (claims: bp-rerun-same-code-separates-flake, ks-treeherder-classification-set, ks-datadog-flaky-categories, ks-meta-pfs-posterior-uncertainty, bp-explain-uncertainty-and-gaps)
- **evidence-states-what-was-observed**: A verdict's evidence MUST state what was observed and where, kept apart from what is inferred from it; an argument from what is likely is not evidence. (claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log, bp-separate-information-from-judgment, ev-get-data-first)
- **bug-names-observed-misbehavior**: A product-bug verdict MUST name the misbehavior observed, the actual result against the expected one, and where in the system under test it was observed. (claims: bp-bug-report-observed-vs-expected, bp-failure-message-desired-actual)
- **flake-cites-history-or-race**: A flake verdict MUST cite the test's outcome history on unchanged code, such as a pass on retry or both a failure and a pass on the same revision, or a race visible in the error; that a failure seems intermittent is not a flake verdict. (claims: pg-ci-flaky-same-code-history, pg-playwright-flaky-status, pg-surefire-flaky-counted, bp-rerun-same-code-separates-flake, ks-luo-flaky-root-causes, ks-datadog-flaky-categories)
- **environment-cites-cross-test-signal**: This MUST hold: An **environment** verdict cites a signal spanning unrelated sites or tests, or a probe/status observation. A single failing test never establishes it. (claim: environment-cites-cross-test-signal-prior)
- **spec-rot-names-new-assertion**: This MUST hold: A **spec-rot** verdict carries a non-empty `suggested_fix` naming what the spec should assert now. A suggested_fix that restates the failure, or says the spec needs updating without saying to what, is a fail. (claim: spec-rot-names-new-assertion-prior)
- **uncertain-names-missing-evidence**: This MUST hold: An **uncertain** verdict names what evidence is missing and what would settle it. Bare "insufficient evidence" is a fail. (claim: uncertain-names-missing-evidence-prior)
- **high-confidence-needs-reproduction-and-mechanism**: This MUST hold: `confidence` is 1-10. A 9 or 10 appears only where the evidence describes an actual reproduction *and* states the mechanism. (claim: high-confidence-needs-reproduction-and-mechanism-prior)
- **triage-changes-nothing**: This MUST hold: No finding files, closes, or comments on an issue, edits a spec, or claims to have changed anything — the disposition is the whole output. (claim: triage-changes-nothing-prior)
- **gather-failure-artifacts-before-classifying**: Before giving a failure a disposition, the triager SHOULD gather the evidence the runner and the CI system keep for it: the relevant log lines and stack trace, the screenshots, trace or video, the test's recent failure history, and the results of the rest of the run. (claims: pg-playwright-trace-on-first-retry, pg-firebase-artifacts, pg-gitlab-failure-history-and-screenshots, pg-xcode-test-report-insights, bp-failure-record-copies-log, ks-rootfinder-compares-pass-fail-logs, pg-android-orchestrator-isolates-crashes)
- **rerun-on-same-revision-before-calling-flake**: Before calling a failure a flake, the triager SHOULD rerun the failing test on the same revision and in the same configuration. (claims: bp-rerun-same-code-separates-flake, pg-github-rerun-same-sha-debug, pg-ci-flaky-same-code-history, pg-pytest-rerun-mitigates, pg-xcode-repeat-tests)
- **pass-on-retry-does-not-clear-a-bug**: A triager SHOULD NOT take a pass on retry as showing that the product code is free of the fault the failure exposed. (claims: ev-ignoring-flaky-hides-bugs, ev-flaky-fixes-fix-cut-bugs, ev-rerun-delays-root-cause, ev-flaky-erodes-trust, ev-reruns-may-not-manifest)
- **find-the-change-that-introduced-the-failure**: When a test that passed on an earlier revision fails on a later one, the triager SHOULD identify the change that introduced the failure. (claims: ks-git-bisect-finds-culprit, bp-gardener-owns-new-failures, pg-gitlab-failure-history-and-screenshots)
- **named-triage-rotation-owns-failures**: A team SHOULD name who triages the failures on the branches it watches: a person, a rotation or the team responsible for the test. (claims: bp-sheriffs-review-every-failure, bp-gardener-owns-new-failures, ks-buildkite-notify-responsible-team)
- **separate-infrastructure-outcomes-from-test-failures**: A failure the test infrastructure caused, such as a canceled run, an infrastructure error or many unrelated tests failing at once, SHOULD be given the environment disposition, kept apart from product bugs and from flakes in the test itself. (claims: pg-firebase-inconclusive-vs-failure, ks-treeherder-infra-classify-many, pg-gradle-maxfailures-stops-retry, ev-infrastructure-flakiness-share, ev-larger-tests-flakier)
- **stale-test-distinguished-by-intended-behavior-change**: A failure SHOULD be given the stale-test disposition only when the change it failed on was meant to change the behavior the test checks. (claims: bp-failure-classes-flaky-bug-obsolete, bp-tests-change-only-on-behavior-change, pg-jest-snapshot-bug-or-update, ev-regenerating-instead-of-examining)
- **distinguish-broken-from-flaky-by-failure-pattern**: A test that fails on every run of the same revision SHOULD be treated as failing deterministically, not as a flake, however many failures it has had. (claims: ks-trunk-broken-vs-flaky, ks-meta-pfs-broken-vs-flaky, pg-playwright-flaky-status)
- **reproduce-in-the-failing-environment**: A triager SHOULD try to reproduce a failure in the environment where it failed, such as the CI pipeline, and not only on a local machine. (claims: ev-ci-only-flakiness, ev-reruns-may-not-manifest, pg-xcode-repeat-tests, ev-get-data-first)
- **verdict-states-confidence-and-its-basis**: A verdict SHOULD state how confident it is, the evidence that confidence rests on, and the gaps that limit it. (claims: bp-explain-uncertainty-and-gaps, bp-separate-information-from-judgment, ks-meta-pfs-posterior-uncertainty, ev-every-test-flaky-to-some-degree)
- **record-flake-cause-category**: A flake verdict MAY record the cause category the evidence points to, such as asynchronous wait, concurrency or test order dependency, or unknown where none is evident. (claims: ks-luo-flaky-root-causes, ks-datadog-flaky-categories)
- **known-failure-marked-expected-with-reason**: A test whose failure is already known MAY be marked as expected to fail, with the reason recorded beside the mark. (claims: pg-pytest-xfail-strict-reason, pg-playwright-test-fail-annotation, ks-treeherder-classification-set)

## Triaging a failed test

This section is informative: it shows one way to keep the rules, not a required method.

1. Know who triages. Mozilla's sheriffs review the failures their trees show and decide whether each is a regression or intermittent; Chromium's gardener keeps new failures out, repairs existing ones and identifies the culprit change; Buildkite Test Engine can notify the team responsible for a flaky test.
2. Gather the evidence first. Copy the relevant failure lines from the log into the record rather than only linking the log, since logs are eventually deleted. Collect what the runner keeps:
   - Playwright records a trace on the first retry in CI, with the actions and locators used, a DOM snapshot per action, the network requests, the browser and test console logs, and a screencast.
   - Xcode's test report brings forward the failure information and screenshots, and its Insights show failure patterns across configurations and run destinations.
   - Firebase Test Lab gives each instrumentation test a report page with stack traces, logs and video.
   - GitLab shows how often a failing test failed on the default branch in the last 14 days, which tests newly failed against the target branch, and screenshot attachments.
   - Android Test Orchestrator runs each test in its own Instrumentation instance, so one crash does not hide the rest of the suite's results.
3. Rerun on the same revision. GitHub Actions reruns only the failed jobs, on the same commit SHA and ref, with debug logging if asked. Xcode repeats a test until its first failure, until its first pass, or a fixed number of times. pytest-rerunfailures, Maven Surefire's `rerunFailingTestsCount` and Gradle's test-retry plugin rerun failures and report a test that passes on a rerun separately as flaky.
4. Read the rerun one way only. A pass shows the test is flaky. Continued failure leaves it either a deterministic failure or a flake that did not show; a few reruns can miss a flake whose chance of changing outcome is low.
5. Reproduce where it failed. Rerun in CI, or in an environment set up like it, before concluding from a local run.
6. Tell the dispositions apart:
   - **Product bug**: the system under test misbehaved; name the actual result against the expected one and where it was seen.
   - **Flake**: the outcome differs on unchanged code; cite the history or the race. Hand the test to the flaky-test lifecycle in [adc.guideline.testing.flaky-test-quarantine](cookbook:4f5fe9ef-1bf8-4354-92c7-92d9e28673b8).
   - **Environment fault**: the infrastructure failed, not the test; many jobs failing at once, a canceled run or an infrastructure error point here. Gradle's test-retry plugin stops retrying once too many tests fail, and Firebase Test Lab reports an inconclusive outcome, separate from failure, for a likely Test Lab problem.
   - **Stale test**: the behavior the test checks was changed on purpose. For a snapshot test, fix any bug before regenerating the snapshot, so the buggy behavior is not recorded; see [adc.guideline.testing.snapshot-testing](cookbook:3d9f5176-afaa-47a2-8a89-fc0402f3dff2).
   - **Uncertain**: the evidence does not settle it; say what is missing.
7. For a new failure, find the change that introduced it. `git bisect` binary-searches between a known good and a known bad revision; its run mode lets a script mark an untestable revision (exit code 125) so it is skipped.
8. Where the failure is known and accepted, mark it expected. pytest's `xfail` takes a `reason`, and its `raises` parameter reports any other exception as a regular failure. Playwright's `test.fail` runs the test and complains if it passes.
9. State the verdict: the disposition, the observed evidence apart from the inference, the confidence, what it rests on and what would change it.

Tools that classify failures: Mozilla's Treeherder gives each failure one value from a fixed list (not classified, fixed by commit, expected fail, intermittent, infra and variants) and lets sheriffs pin many failed jobs and classify them together. Trunk Flaky Tests labels each test broken, flaky or healthy, with broken taking precedence over flaky. Meta's probabilistic flakiness score measures how likely a test is to fail when it could have passed on the same code, and reports when it cannot confidently estimate a test's flakiness. Datadog Flaky Test Management sorts flaky tests into cause categories, with an Unknown category. Microsoft's RootFinder diffs the logs of passing and failing runs to locate a flake's cause.

## Examples

This section is informative; the verdicts below are illustrations, not a required format.

A flake verdict:

```text
Disposition: flake
Observed: checkout total test failed on revision a1b2c3d with "expected 3 items, got 2"
  (log lines copied below); the same test passed on rerun of a1b2c3d in the same CI job.
History: failed 4 times and passed 120 times on the main branch in the last 14 days, all on unchanged code.
Cause category: asynchronous wait (the assertion runs before the cart update request completes).
Confidence: likely. Rests on the same-revision pass and the history; not yet reproduced
  on demand, so a product-side race in the cart update is not ruled out.
```

An uncertain verdict:

```text
Disposition: uncertain
Observed: login test timed out once on revision 9f8e7d6; no trace was recorded and the rerun passed.
Missing: a trace or screenshot of the failing run, and whether other tests on the same runner
  failed in that window. Either would separate a flake from an environment fault.
```

## What a reviewer looks for

Checks that every failure has exactly one disposition from the fixed set, and that a failure the evidence does not settle is uncertain rather than forced. Checks that each verdict's evidence states what was observed and where, apart from inference, with the log lines copied in; that a product-bug verdict names the actual and expected result and where it was seen; that a flake verdict cites same-revision history or a visible race; that an environment verdict cites a signal across unrelated tests or an infrastructure observation; and that a stale-test verdict rests on an intended behavior change and names what the test should assert now. Checks that an uncertain verdict names the missing evidence, that confidence stays within the stated scale and its top values, and that the verdict states the basis and gaps of its confidence. Checks that the evidence was gathered and the test rerun on the same revision, in the failing environment, before a flake was called; that a pass on retry was not taken to clear the product; that a new failure's introducing change was sought; that someone is named to triage; and that the triage changed nothing outside its disposition.

## A complete review must establish

- Each MUST rule is kept, with no exception: `every-failure-gets-one-disposition`, `disposition-from-fixed-set`, `evidence-states-what-was-observed`, `bug-names-observed-misbehavior`, `flake-cites-history-or-race`, `environment-cites-cross-test-signal`, `spec-rot-names-new-assertion`, `uncertain-names-missing-evidence`, `high-confidence-needs-reproduction-and-mechanism`, `triage-changes-nothing`.
- Each SHOULD rule is kept or its departure is stated: `never-force-a-verdict`, `gather-failure-artifacts-before-classifying`, `rerun-on-same-revision-before-calling-flake`, `pass-on-retry-does-not-clear-a-bug`, `find-the-change-that-introduced-the-failure`, `named-triage-rotation-owns-failures`, `separate-infrastructure-outcomes-from-test-failures`, `stale-test-distinguished-by-intended-behavior-change`, `distinguish-broken-from-flaky-by-failure-pattern`, `reproduce-in-the-failing-environment`, `verdict-states-confidence-and-its-basis`.
- Each MAY rule is noted where it was used: `record-flake-cause-category`, `known-failure-marked-expected-with-reason`.

## A build must establish

- `every-failure-gets-one-disposition`: each failure in the input has exactly one disposition, and no disposition names a failure outside it.
- `disposition-from-fixed-set`: each disposition is one value of the fixed set.
- `never-force-a-verdict`: each failure the evidence does not settle is uncertain.
- `evidence-states-what-was-observed`: each verdict states what was observed and where, apart from inference.
- `bug-names-observed-misbehavior`: each product-bug verdict names the actual and expected result and where it was seen.
- `flake-cites-history-or-race`: each flake verdict cites outcome history on unchanged code or a race in the error.
- `environment-cites-cross-test-signal`: each environment verdict cites a signal across unrelated tests or a probe or status observation.
- `spec-rot-names-new-assertion`: each spec-rot verdict's `suggested_fix` names what the spec should assert now.
- `uncertain-names-missing-evidence`: each uncertain verdict names the missing evidence and what would settle it.
- `high-confidence-needs-reproduction-and-mechanism`: each confidence is 1-10, and each 9 or 10 rests on a described reproduction and a stated mechanism.
- `triage-changes-nothing`: no finding files, closes or comments on an issue, edits a spec, or claims a change.
- `gather-failure-artifacts-before-classifying`: the log lines, artifacts, history and run results were gathered before the disposition.
- `rerun-on-same-revision-before-calling-flake`: each flake was rerun on the same revision and configuration first.
- `pass-on-retry-does-not-clear-a-bug`: no verdict treats a pass on retry as clearing the product code.
- `find-the-change-that-introduced-the-failure`: each new failure names the change that introduced it, or says why it is not yet known.
- `named-triage-rotation-owns-failures`: a person, rotation or responsible team is named to triage.
- `separate-infrastructure-outcomes-from-test-failures`: each infrastructure-caused failure is an environment fault, not a bug or flake.
- `stale-test-distinguished-by-intended-behavior-change`: each stale-test verdict rests on a change meant to alter the checked behavior.
- `distinguish-broken-from-flaky-by-failure-pattern`: no test failing on every run of one revision is called a flake.
- `reproduce-in-the-failing-environment`: reproduction was tried in the environment where the failure happened.
- `verdict-states-confidence-and-its-basis`: each verdict states its confidence, its basis and its gaps.
- `record-flake-cause-category`: where used, each flake's cause category is recorded.
- `known-failure-marked-expected-with-reason`: where used, each expected-failure mark carries its reason.

## Rationale

This section is informative.

A failed test is either a fault in the product, a fault in the test or a fault in what runs it, and acting on the wrong one wastes the fix or ships the bug. In Labuschagne et al.'s study of 61 Java projects on Travis CI, 18% of test-suite executions failed, 13% of those failures were flaky, and of the rest 74% were bugs in the system under test and 26% incorrect or obsolete tests. Treeherder, Firebase Test Lab and Trunk each ship a fixed set of outcomes, which is why every failure gets exactly one disposition from a fixed set. Luo et al. report, from a personal communication, that 4.56% of Google TAP's daily test failures were caused by flaky tests; how they were classified is not disclosed, so the figure shows only that a flaky-versus-other split is used at scale.

The rules on evidence come from bug-writing and analytic practice: Mozilla's guidelines require the observed and expected result with facts kept apart from speculation, Chromium and Mozilla both have the triager copy the failure lines from the log, Software Engineering at Google wants a failure to state the desired and actual outcome, and ICD 203 separates information from judgment. Agans's rules, as Wheeler reviews them, are to make the failure happen and look rather than fix on a guess.

A flake is defined by its history on unchanged code in every runner and CI system read: Playwright, Maven Surefire, Azure DevOps, CircleCI and Firebase Test Lab. The rerun separates the classes one way only, as Luo et al. note, which is why a failing rerun does not settle the class and why an unsettled failure stays uncertain: Treeherder keeps "not classified", Datadog keeps "Unknown", and Meta's model reports when it cannot confidently estimate a test's flakiness. A pass on retry still does not clear the product: ignoring flaky failures is dangerous because they may be real faults, 24% of the flaky-test fixes in Luo et al.'s sample changed the code under test and 94% of those fixed a bug there, rerunning only delays the root cause, and once failures are ignored engineers stop reacting to tests. At Microsoft, Lam et al. found 86% of flaky tests rerun 100 times locally were flaky only in CI, which is why reproduction is tried where the failure happened.

Infrastructure produces failures of its own. Larger tests are flakier because they use more infrastructure; in Gruber et al.'s Python study, as Parry et al. report it, 28% of 7,571 flaky tests were infrastructure flakiness. A stale test is told apart by intent: existing tests are expected to change only when the system's behavior is meant to change, and Jest warns against regenerating snapshots instead of examining the failure.

Most new rules are recommendations because their sources are single publishers' guidance or a standard from outside software: a team may depart from one where it states why, for example a team with no CI history to cite or no way to reproduce in CI. The cause category and the expected-failure mark are options, used where a team's tooling records them.

Five prior rules are kept as the owner's text, which the research could not support at their stated strength or found against, and several questions are left to the owner. The research supports a SHOULD for an environment verdict citing a signal across tests, but no source says a single test never establishes one, and Gruber et al. classify infrastructure flakiness from one test's pattern across runs. No source requires a stale-test verdict to carry the new assertion, and the name of that disposition is open. ICD 203 supports naming the missing evidence at SHOULD, not as a must-hold check. No source sets a 1-10 confidence scale or ties its top values to a reproduction and a mechanism. In published triage the triager acts on the verdict, filing bugs, disabling tests and reverting culprits, so whether triage changes nothing is open. Whether a flake disposition also opens an investigation of the product code, or leaves that to the flaky-test lifecycle, is open too.

No source found treats an agent as the triager; every procedure read assigns triage to people or to tools that label flakiness, and the rules are stated for whoever triages.

## References

This section is informative; every reference below is informative, and none is normative.

- Playwright, *Retries*, *Trace viewer* and *Annotations*: https://playwright.dev/docs/test-retries, https://playwright.dev/docs/trace-viewer, https://playwright.dev/docs/test-annotations
- pytest, *How to use skip and xfail* and *Flaky tests*: https://docs.pytest.org/en/stable/how-to/skipping.html, https://docs.pytest.org/en/stable/explanation/flaky.html
- pytest-rerunfailures: https://github.com/pytest-dev/pytest-rerunfailures
- Maven Surefire, *Rerun failing tests*: https://maven.apache.org/surefire/maven-surefire-plugin/examples/rerun-failing-tests.html
- Gradle test-retry plugin: https://github.com/gradle/test-retry-gradle-plugin
- Apple, *Running tests and interpreting results*: https://developer.apple.com/tutorials/data/documentation/xcode/running-tests-and-interpreting-results.json
- Android, *AndroidJUnitRunner*: https://developer.android.com/training/testing/instrumented-tests/androidx-test-libraries/runner
- Firebase Test Lab, *OutcomeSummary*, *Troubleshooting* and *Analyzing results*: https://firebase.google.com/docs/test-lab/reference/toolresults/rest/v1beta3/OutcomeSummary, https://firebase.google.com/docs/test-lab/troubleshooting?hl=en, https://firebase.google.com/docs/test-lab/android/analyzing-results
- GitHub Actions, *Re-running workflows and jobs*: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
- GitLab, *Unit test reports*: https://docs.gitlab.com/ci/testing/unit_test_reports/
- Azure DevOps, *Manage flaky tests*: https://learn.microsoft.com/en-us/azure/devops/pipelines/test/flaky-test-management?view=azure-devops
- CircleCI, *Test insights*: https://circleci.com/docs/guides/insights/insights-tests/
- Buildkite Test Engine, *Flaky test management*: https://buildkite.com/docs/test-engine/flaky-test-management
- Datadog, *Flaky Test Management*: https://docs.datadoghq.com/tests/flaky_management/
- Trunk, *Flaky test detection*: https://docs.trunk.io/flaky-tests/detection
- Jest, *Snapshot testing*: https://jestjs.io/docs/snapshot-testing
- Git, *git-bisect*: https://git-scm.com/docs/git-bisect
- Mozilla Treeherder failure classifications: https://raw.githubusercontent.com/mozilla/treeherder/master/treeherder/model/fixtures/failure_classification.json
- Mozilla sheriffing: https://firefox-source-docs.mozilla.org/testing/sheriffed-intermittents/index.html, https://wiki.mozilla.org/Sheriffing/How_To/Intermittent_bugs, https://wiki.mozilla.org/Sheriffing/How_To/Treeherder
- Mozilla, *Bug writing guidelines*: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html
- Chromium, *Handling a failing test* and *Gardener*: https://www.chromium.org/developers/tree-sheriffs/handling-a-failing-test/, https://chromium.googlesource.com/chromium/src/+/HEAD/docs/gardener.md
- Meta Engineering, *Probabilistic flakiness*: https://engineering.fb.com/2020/12/10/developer-tools/probabilistic-flakiness/
- Luo et al., *An Empirical Analysis of Flaky Tests* (FSE 2014): https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf
- Labuschagne et al., *Measuring the cost of regression testing in practice* (ESEC/FSE 2017): https://www.cs.ubc.ca/~rtholmes/papers/fse_2017_labuschange.pdf
- Lam et al., *Root causing flaky tests in a large-scale industrial setting* (ISSTA 2019): https://www.microsoft.com/en-us/research/wp-content/uploads/2019/11/LamETAL19RootFinder.pdf
- Parry et al., *A Survey of Flaky Tests* (TOSEM 2022): https://eprints.whiterose.ac.uk/id/eprint/230095/1/parry2021.pdf
- ODNI, *ICD 203 Analytic Standards*: https://archive.dni.gov/files/documents/ICD/ICD-203.pdf
- *Software Engineering at Google*, chapters 11, 12 and 14: https://abseil.io/resources/swe-book/html/ch11.html, https://abseil.io/resources/swe-book/html/ch12.html, https://abseil.io/resources/swe-book/html/ch14.html
- Martin Fowler, *Eradicating Non-Determinism in Tests*: https://martinfowler.com/articles/nonDeterminism.html
- David A. Wheeler, review of Agans's *Debugging*: https://dwheeler.com/essays/debugging-agans.html

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
