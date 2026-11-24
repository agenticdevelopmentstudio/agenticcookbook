
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

