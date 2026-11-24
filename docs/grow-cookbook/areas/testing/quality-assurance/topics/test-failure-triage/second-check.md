## bp-triage-acts-on-verdict
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The Chromium page has "Disable the test: Prefix DISABLED_ to the name of the crashing/timing out test" and a "File a bug" step. The Azure page lists "Resolution - Manual bug-creation or manual marking and unmarking test as flaky based on your analysis" word for word.

## bp-gardener-owns-new-failures
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: gardener.md says "In priority order, gardeners need to ensure that" the tree is open, new test failures are not introduced and existing ones are repaired. It also gives the gardener authority to "Revert changes that you know or suspect are causing breakages" and describes identifying a culprit CL and reverting it.

## pg-playwright-trace-on-first-retry
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The trace viewer page also covers the rest of the claim: the Actions tab shows "what locator was used for every action", the Console tab shows "console logs from the browser as well as from your test", and the screenshots option "records a screencast".

## pg-firebase-artifacts
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote sits under "Partitioned instrumentation test results". The same page says "Tests run on physical devices also return performance metrics".

## pg-gitlab-failure-history-and-screenshots
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: All three fragments appear verbatim on the GitLab unit test reports page.

## pg-xcode-test-report-insights
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both sentences are in Apple's JSON doc. The second is the definition of the "Insights" term.

## bp-failure-record-copies-log
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Chromium adds "it is not sufficient to give a URL to the bot log, as the logs eventually get deleted". Mozilla says "you shall open the log and copy the relevant lines for the failure", which is a requirement in both cases.

## ks-rootfinder-compares-pass-fail-logs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence appears verbatim in the Lam et al. ISSTA 2019 PDF.

## pg-android-orchestrator-isolates-crashes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists "Minimal shared state: Each test runs in its own Instrumentation instance" and "Crashes are isolated", followed by the quoted text.

## bp-rerun-same-code-separates-flake
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Luo et al. call this "the most common approach", which supports the claim's "common way".

## pg-github-rerun-same-sha-debug
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page says you can re-run "all failed jobs in a workflow run", that `--debug` turns on diagnostic and debug logging, and that the re-run uses the same GITHUB_SHA and GITHUB_REF.

## pg-ci-flaky-same-code-history
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Each source holds its own segment of the quote verbatim: CircleCI the 14-day same-commit rule, Azure the rerun rule, and Firebase the "flaky" outcome definition.

## pg-pytest-rerun-mitigates
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The pytest-rerunfailures README also documents `--only-rerun` (rerun failures that match an expression) and `--rerun-except` (rerun failures that do not match).

## pg-xcode-repeat-tests
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is under the heading "Run testing repeatedly to determine reliability". The page mentions "whether to restart the test runner for each repetition" and the xcodebuild `-test-repetitions` option.

## ev-ignoring-flaky-hides-bugs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Lam et al. (Microsoft) hold the first sentence and Luo et al. (Illinois) the second, both verbatim.

## ev-flaky-fixes-fix-cut-bugs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Finding F.12 appears verbatim in the Luo et al. PDF.

## ev-rerun-delays-root-cause
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence just before it reads "you can limit the impact of flaky tests by automatically rerunning them when they fail".

## ev-flaky-erodes-trust
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: SWE at Google ch. 11 and Fowler each hold their sentence verbatim.

## ev-reruns-may-not-manifest
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Parry et al. attribute the 10,000-reruns finding to FlakeFlagger's motivating study, which covered 24 Java projects. That fits the claim's "in one study".

## ks-git-bisect-finds-culprit
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both sentences appear verbatim in the git-bisect documentation.

## bp-sheriffs-review-every-failure
- quote-found: no
- supports-claim: partly
- citation 1: lacks-quote
- result: refuted
- note: The source reads "and determines if the failure is a regression or an intermittent failure", not "determine". It also limits the review to tier 1 and 2 tasks shown by default on pushes to named sheriffed trees, not every failure on the trees.
- correction: refuted (quote-found no, supports-claim partly); trust 72 -> 32; a rule citing it cannot carry MUST

## ks-buildkite-notify-responsible-team
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page also says "workflow monitors identify tests whose results indicate flakiness. Labels then make these tests easy to find" and that the engine will "notify the teams responsible for fixing them".

## pg-firebase-inconclusive-vs-failure
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: OutcomeSummary lists "inconclusive" separately from "failure". The FAQ says inconclusive outcomes come from canceled runs or infrastructure errors "caused by internal Test Lab issues".

## ks-treeherder-infra-classify-many
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Pinboard section continues: "It can save time to pin them all at once and apply a single classification to them all with a single click."

## pg-gradle-maxfailures-stops-retry
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The README goes on to say "the plugin can be configured to stop retrying after a certain number of total test failures", and its example uses `maxFailures = 20`.

## ev-infrastructure-flakiness-share
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Parry et al. report 22,352 projects, each suite run 200 times in original order and 200 times in random order, with the 28/59/13% split quoted verbatim.

## ev-larger-tests-flakier
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both fragments appear verbatim in SWE at Google ch. 14.

## bp-failure-classes-flaky-bug-obsolete
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The paper covers 61 projects that use Travis CI, and its title names Java projects. The percentages match the quote.

## bp-tests-change-only-on-behavior-change
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both sentences appear verbatim in SWE at Google ch. 12.

## pg-jest-snapshot-bug-or-update
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both sentences appear verbatim on Jest's Snapshot Testing page.

## ev-regenerating-instead-of-examining
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence appears verbatim on Jest's Snapshot Testing page.

## ks-trunk-broken-vs-flaky
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page ranks the states Broken, then Flaky, then Healthy. It says "If a test triggers both a broken monitor and a flaky monitor simultaneously, it shows as Broken."

## ks-meta-pfs-broken-vs-flaky
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The post says the model "correctly captures the case where a perfectly deterministic test breaks", and in that case PFS is "close to zero, despite many observed failures".

## pg-playwright-flaky-status
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both definitions appear verbatim on the Playwright Retries page.

## ev-ci-only-flakiness
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both sentences appear verbatim in the Lam et al. PDF.

## ev-get-data-first
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Wheeler lists the rules "Make it fail" and "Quit thinking and look (get data first, don't just do complicated repairs based on guessing)", plus the quoted sentence.

## bp-explain-uncertainty-and-gaps
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: curl got a 403 but WebFetch got the PDF. Standard (2) holds all three sentences verbatim, including "the analyst's confidence in the basis for this judgment". The claim's "has" matches the source's "should".

## bp-separate-information-from-judgment
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Standard (3), "Properly distinguishes between underlying intelligence information and analysts' assumptions and judgments", holds both sentences verbatim.

## ks-meta-pfs-posterior-uncertainty
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The post says "instead of producing point estimates of the PFS, our model yields an entire posterior distribution". It calls a wide or multi-modal distribution "a sign that our model cannot confidently estimate flakiness of a particular test".

## ev-every-test-flaky-to-some-degree
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Meta says "Software engineering practice, however, shows that all real-world tests are flaky to some extent". Lam et al. hold the "calls to adopt the position" sentence verbatim.

## ks-luo-flaky-root-causes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: All five fragments appear verbatim in the Luo et al. PDF.

## ks-datadog-flaky-categories
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Once decompressed, the page says AI assigns "a root cause category to each flaky test based on execution patterns and error signals". Its table includes Concurrency, Randomness, Timeout, Order Dependency, Asynchronous Wait, Network, Time, Environment Dependency and "Unknown: Test is flaky for an unknown reason", along with others.

## pg-pytest-xfail-strict-reason
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The pytest skipping page holds all three fragments under its reason and raises parameter sections.

## pg-playwright-test-fail-annotation
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page also says "test.fixme() marks the test as failing. Playwright will not run this test, as opposed to the fail annotation."

## ks-treeherder-classification-set
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The fixture file lists exactly those eight classification names.
