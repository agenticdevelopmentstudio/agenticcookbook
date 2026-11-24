# e2e-test-authoring: research

Researched 2026-11-24 against base commit `77a898dbc718928bbd96ef617723c83ec69cd549`. Every finding below names the claim in `research.json` that holds its source and its verbatim quote. The research covers how an end-to-end (E2E) spec is written: the locators it uses, how it waits, how it keeps state isolated, when it mocks the network and when it runs against a live environment, how it handles accounts and secrets, and how it states the rationale for what it asserts.

**Verdicts on the topic's existing rules, and the strength the sources support:**

- **write-deterministic-specs**: supported. The sources support SHOULD for determinism in general. For fixed waits they reach MUST NOT: Playwright says "Never wait for timeout" (bp-pw-wait-for-timeout-flaky), and Android, Selenium, WebdriverIO, Cypress and Fowler all reject sleeps.
- **rationale-cites-assertion-source**: supported at SHOULD. ISTQB calls traceability from test basis to test cases "important" (bp-istqb-traceability), and Playwright annotations can carry the link (ks-pw-annotations). No source supports the "one-paragraph" length.
- **rationale-names-what-makes-assertion-correct**: unsupported at the strength it states. "Is a fail" makes it a MUST, but the only support is ISTQB's SHOULD-strength traceability (bp-istqb-traceability). The prior text is recorded as rationale-names-what-makes-assertion-correct-prior. The sources would carry it as a SHOULD.
- **hermetic-specs-mock-the-api**: supported in its general form at SHOULD. A hermetic spec stubs the network through the tool's interception API: Playwright's Network API, route and HAR (bp-pw-use-network-api, ks-pw-mock-api, ks-pw-har-replay), Cypress stubs (ks-cy-stub-majority), Selenium (ks-se-eliminate-external-services) and a test double (ev-fowler-test-double-remote). Naming one tool's method is that tool's mechanism, not a sourced rule.
- **no-credentials-or-real-user-data**: supported. The credentials half reaches MUST through OWASP ASVS 2.10.4 (bp-asvs-no-secrets-in-repo). The real-user-data half rests on the data-minimisation principle (bp-ico-synthetic-minimisation) and a Thoughtworks Hold (ev-thoughtworks-prod-data, ev-thoughtworks-weak-test-security). That supports SHOULD, and MUST only by the owner's choice (see the open questions).

**New rules the sources support** (all verdict `new`):

- e2e-locators-user-facing-first (SHOULD)
- e2e-test-id-only-when-no-user-facing-locator (SHOULD; MAY use a test id where no role or text fits)
- e2e-avoid-dom-structure-locators (SHOULD NOT use CSS/XPath DOM paths)
- e2e-wait-on-conditions-not-time (MUST NOT use fixed sleeps)
- e2e-isolate-test-state (SHOULD; Selenium's "Do not share test data" is imperative)
- e2e-set-up-state-programmatically (SHOULD)
- e2e-control-the-clock (SHOULD)
- e2e-retries-surface-flakiness (SHOULD; Android says "always fix flaky tests")
- e2e-hermetic-by-default-live-for-critical-paths (SHOULD)
- e2e-select-live-specs-by-tag-or-project (MAY: the sources show tags, projects and environment variables and prefer none)
- e2e-credentials-from-environment (MUST, via ASVS; the tool docs say SHOULD)
- e2e-stored-auth-state-git-ignored (SHOULD)
- e2e-dedicated-test-accounts (SHOULD)
- e2e-trace-on-ci-failure (SHOULD; one tool owner only)
- e2e-page-objects-hold-no-assertions (SHOULD)
- e2e-do-not-repeat-lower-level-assertions (SHOULD; practitioner sources only)

## Best practices

- **Test what the user sees.** Playwright's best practices open with: "Automated tests should verify that the application code works for the end users" (bp-pw-test-user-visible-behavior).
- **Isolate every test.** "Each test should be completely isolated from another test and should run independently" (bp-pw-tests-fully-isolated). Cypress says tests "should always be able to run independently from one another and still pass" (bp-cy-tests-independent), and says to "Clean up state before tests run" rather than after (bp-cy-clean-state-before). When a database is involved, "make sure you control the data" (bp-pw-control-database-data).
- **Set up state programmatically.** Cypress: "programmatically log into your application, and take control of your application's state" (bp-cy-programmatic-login).
- **Don't depend on what you don't control.** Playwright: "Don't try to test links to external sites or third party servers that you do not control" (bp-pw-only-test-what-you-control). Instead, "use the Playwright Network API and guarantee the response needed" (bp-pw-use-network-api). A spec that does run against staging needs that environment kept stable: "make sure it doesn't change" (bp-pw-stable-staging).
- **Never wait for time.** Playwright's API reference marks `waitForTimeout` as discouraged: "Never wait for timeout in production. Tests that wait for time are inherently flaky" (bp-pw-wait-for-timeout-flaky). Cypress lists "Waiting for arbitrary time periods" as an anti-pattern (bp-cy-no-arbitrary-wait). What replaces the wait is an assertion that retries until its condition holds (bp-pw-web-first-assertions).
- **Control the clock.** Playwright calls simulating time "essential for verifying the correctness of applications" (bp-pw-clock-control).
- **Debug CI failures from traces.** "Use the Playwright trace viewer instead of videos and screenshots" (bp-pw-trace-viewer-on-ci).
- **Keep secrets out of the source.** Playwright: "pass secrets from outside" (bp-pw-env-secrets). OWASP ASVS 2.10.4 requires that keys be "not included in the source code or stored within source code repositories" (bp-asvs-no-secrets-in-repo). OWASP's cheat sheet says to create "standard test secrets" (bp-owasp-standard-test-secrets), and suggests keeping production and development secrets in separate stores (bp-owasp-separate-prod-dev).
- **Use synthetic data, not personal data.** The ICO says synthetic data "can help you comply with the data minimisation principle" (bp-ico-synthetic-minimisation). The page does not name testing, so the point is applied here, not stated there.
- **Trace each assertion to its basis.** ISTQB says traceability between "test basis elements" and test cases is "important" (bp-istqb-traceability). That is the source for a rationale that cites the feature doc or plan. It supports SHOULD, not a fail.

## Known solutions

- **Network mocking.**
  - Playwright mocks HTTP and HTTPS (ks-pw-mock-api) and replays recorded HAR files, matched strictly on URL and method (ks-pw-har-replay).
  - Cypress sets out the trade-off. Server responses are to be used "sparingly" and are "great for the critical paths" (ks-cy-real-server-critical-paths). Most tests stub, with "one true end-to-end test" kept live (ks-cy-stub-majority), because stubs carry "no guarantee" of matching the real server (ks-cy-stub-drift).
  - Selenium says removing external dependencies "will greatly improve the speed and stability" of tests (ks-se-eliminate-external-services).
- **Waiting.**
  - Playwright auto-waits for actionability before every action (ks-pw-auto-wait-actionability).
  - WebdriverIO calls fixed pauses "a bad idea" (ks-wdio-no-pause) and warns against assertions that do not wait (ks-wdio-auto-retry-assertions).
  - Selenium explains why sleeps fail: the code "can't know exactly how long it needs to wait" (ks-se-sleep-fails). It also says not to mix implicit and explicit waits (ks-se-no-mix-waits).
- **Isolation.**
  - Playwright gives each test its own storage and cookies through a fresh browser context (ks-pw-browser-context-isolation), and fixtures isolated between tests (ks-pw-fixtures-isolated). Its parallel-by-default runs make that isolation a precondition (ks-pw-parallel-default).
  - Selenium: "Do not share test data" (ks-se-no-shared-data) and "Create a new WebDriver instance per test" (ks-se-new-driver-per-test). It also recommends logging in by API rather than through the browser (ks-se-api-login).
- **Locators compared.**
  - Cypress recommends `data-*` attributes (ks-cy-data-attributes) and calls brittle selectors an anti-pattern (ks-cy-brittle-selectors).
  - WebdriverIO puts role plus name first, because it "keeps matching when class names, test ids or the DOM structure change" (ks-wdio-role-selector).
  - Selenium's older order puts IDs, then CSS, first (ks-se-locator-preference). It is the outlier against the user-facing-first order of Playwright, Testing Library and WebdriverIO.
- **Page objects.** Selenium: page objects "should never make verifications or assertions" (ks-se-po-no-assertions).
- **Retries.** Playwright reports a test that passed only on retry as "flaky" (ks-pw-retries-flaky), not as passed.
- **Separating live from hermetic runs.** Playwright offers three mechanisms:
  - tags filtered at run time (ks-pw-tags-grep)
  - projects that filter tests (ks-pw-projects-filter) and set per-environment options such as retries (ks-pw-projects-environments)
  - an environment variable that switches the target (ks-pw-env-staging-switch)

  Annotations can carry a link to the source of an assertion (ks-pw-annotations).
- **Accounts and secrets.**
  - Playwright recommends git-ignoring the stored auth directory (ks-pw-auth-gitignore), because the state file can "impersonate you or your test account" (ks-pw-auth-state-sensitive). Tests that change server state need "one per each parallel worker" accounts (ks-pw-account-per-worker).
  - Cypress says to git-ignore its env file (ks-cy-env-gitignore). It warns that values given to the browser are exposed to third-party scripts (ks-cy-env-values-exposed) and that passwords and tokens should stay out of the logged session id (ks-cy-session-no-passwords-in-id).
  - GitHub Actions withholds secrets from fork-triggered runs (ks-gha-secrets-forks) and warns against printing secrets in logs (ks-gha-dont-print). A live spec that needs secrets is therefore gated in CI by where the run comes from.

## Platform guidelines

- **Web: Playwright.** Its locator guide recommends "prioritizing user-facing attributes and explicit contracts" (pg-pw-prioritize-user-facing), led by `getByRole` (pg-pw-getbyrole). It says "CSS and XPath are not recommended as the DOM can often change" (pg-pw-css-xpath-not-recommended). It calls test ids "the most resilient way of testing" (pg-pw-testid-resilient) but lists them after the user-facing locators.
- **Web: Testing Library.** Its guiding principle is that a test "should resemble how users interact with your code" (pg-tl-guiding-principle). Role is the "top preference for just about everything" (pg-tl-byrole-top), and test ids are "only recommended for cases where you can't match by role or text" (pg-tl-testid-last). The two owners disagree on how far down test ids sit; that is recorded as an open question.
- **Web: W3C WAI-ARIA 1.2.** The accessibility tree is the "Tree of accessible objects that represents the structure of the user interface" (pg-aria-accessibility-tree). The accessible name "is the name of a user interface element" (pg-aria-accessible-name). Role locators rest on both.
- **Apple.**
  - XCUIAutomation drives views and controls "as if a person is interacting with your interface" (pg-apple-ui-test-as-person).
  - `accessibilityIdentifier` is Apple's test id: it "can be used to uniquely identify an element in the scripts you write" (pg-apple-accessibility-identifier).
  - Waiting is `waitForExistence(timeout:)` (pg-apple-wait-for-existence).
  - No Apple text was found on locator priority or on sleeps.
- **Android.**
  - Avoid "pausing your tests for an arbitrary period (sleep)" (pg-android-avoid-sleep); wait "until specific conditions have been met" (pg-android-wait-until).
  - "Add retrying mechanisms to big tests, but always fix flaky tests" (pg-android-retries-fix).
  - Espresso requires long-running work to be registered as idling resources (pg-android-idling-resources). That lets tests "leave your waits, syncs, sleeps, and polls behind" (pg-android-espresso-sync). Espresso-Intents stubs intents "for hermetic testing" (pg-android-espresso-intents-hermetic).
  - Compose finds nodes in the semantics tree (pg-android-compose-semantics).
  - UI Automator resets the app to "a fresh state" by clearing its data (pg-android-uiautomator-clear-data).
- **Windows.** In Microsoft UI Automation, `AutomationId` "uniquely identifies a UI Automation element from its siblings" (pg-ms-automationid). It is not unique across the tree and "typically needs container and scope information to be useful" (pg-ms-automationid-scope). A stable Windows locator is therefore an AutomationId scoped by its container. This is the Windows counterpart of a test id.
- **Databases and runtimes.** No database or runtime owner publishes E2E authoring guidance. The data guidance comes from the test tools (bp-pw-control-database-data) and from security and privacy owners (bp-asvs-no-secrets-in-repo, bp-ico-synthetic-minimisation).

## The expert's view

- **Treat non-determinism as an emergency.** Fowler calls non-deterministic tests "useless" and "a virulent infection that can completely ruin your entire test suite" (ev-fowler-nondeterminism-useless). E2E tests are where it shows: they are "notoriously flaky" (ev-vocke-e2e-flaky).
- **What to do:**
  - "use a callback or polling," never bare sleeps (ev-fowler-no-bare-sleeps)
  - use a waiting query for anything "that may not be available right away" (ev-kcd-find-for-async)
  - keep tests isolated (ev-fowler-isolated)
  - "Always wrap the system clock" (ev-fowler-wrap-clock)
  - reach for a test double against remote services (ev-fowler-test-double-remote)
- **What to avoid:**
  - manipulating HTML elements directly, which makes tests "brittle to changes in the UI" (ev-fowler-po-brittle)
  - querying with `querySelector`, which loses "a lot of that confidence" (ev-kcd-queryselector)
  - assertions in page objects (ev-fowler-po-no-assertions)
- **What people get wrong:**
  - Re-testing in E2E what unit tests already cover. Vocke: "You don't test all the conditional logic and edge cases that your lower-level tests already cover" (ev-vocke-no-retest-lower-level); focus on "the part that the lower-level tests couldn't cover" (ev-vocke-focus-uncovered).
  - Using production data. Thoughtworks puts production data in test environments on Hold: test systems protect private data less well (ev-thoughtworks-weak-test-security), and "Fake data is a safer approach" (ev-thoughtworks-prod-data).
