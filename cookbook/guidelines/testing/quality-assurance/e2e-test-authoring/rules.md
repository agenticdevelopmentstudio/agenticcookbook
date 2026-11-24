
### Determinism and waiting

- **write-deterministic-specs**: An E2E spec SHOULD be deterministic, so that it does not pass on some runs and fail on others. (claims: ev-fowler-nondeterminism-useless, bp-pw-wait-for-timeout-flaky, ks-se-sleep-fails, bp-pw-tests-fully-isolated)
- **e2e-wait-on-conditions-not-time**: An E2E spec MUST NOT wait a fixed time, such as a sleep, a pause or a wait for a timeout, for the application to be ready. (claims: bp-pw-wait-for-timeout-flaky, ev-fowler-no-bare-sleeps)
- **e2e-wait-for-a-condition**: Where a spec has to wait, it SHOULD wait until a specific condition is met, through an action that auto-waits for actionability, an assertion that retries until its condition holds, or an explicit wait for an element or state. (claims: pg-android-wait-until, pg-android-avoid-sleep, ks-pw-auto-wait-actionability, bp-pw-web-first-assertions, ks-wdio-auto-retry-assertions, ks-wdio-no-pause, bp-cy-no-arbitrary-wait, pg-apple-wait-for-existence, pg-android-espresso-sync, ev-kcd-find-for-async)
- **e2e-register-long-running-work**: A suite that uses Espresso MUST register each long-running operation of the app that Espresso does not know of as an idling resource. (claim: pg-android-idling-resources)
- **e2e-no-mixed-waits**: Where the tool has both implicit and explicit waits, as Selenium WebDriver does, a spec SHOULD NOT mix them. (claim: ks-se-no-mix-waits)
- **e2e-control-the-clock**: A spec that tests time-dependent behaviour SHOULD control the clock, through the tool's clock API or a wrapped system clock, rather than depend on real time. (claims: bp-pw-clock-control, ev-fowler-wrap-clock)

### Test state

- **e2e-isolate-test-state**: Each E2E test SHOULD run independently of every other test and still pass, relying on no state another test left. (claims: bp-pw-tests-fully-isolated, bp-cy-tests-independent, ev-fowler-isolated, ks-pw-parallel-default)
- **e2e-fresh-browser-session-per-test**: Each test SHOULD get its own browser session, such as a new browser context or a new driver instance, with its own storage and cookies. (claims: ks-pw-browser-context-isolation, ks-se-new-driver-per-test)
- **e2e-no-shared-test-data**: Tests SHOULD NOT share test data. (claim: ks-se-no-shared-data)
- **e2e-control-database-data**: A spec that works with a database SHOULD control the data in it. (claim: bp-pw-control-database-data)
- **e2e-reset-state-before-each-test**: State SHOULD be reset before each test runs, such as by clearing the app's data, rather than cleaned up after it. (claims: bp-cy-clean-state-before, pg-android-uiautomator-clear-data)
- **e2e-set-up-state-programmatically**: A spec SHOULD log in and set up the application's state programmatically, such as through an API, rather than through the browser. (claims: bp-cy-programmatic-login, ks-se-api-login)
- **e2e-fixtures-give-only-what-test-needs**: Where a suite uses fixtures, each fixture SHOULD give the test everything it needs and nothing else. (claim: ks-pw-fixtures-isolated)

### Retries, flakiness and traces

- **e2e-retries-surface-flakiness**: Where a run retries failed E2E tests, a test that failed first and passed on retry SHOULD be reported as flaky, not as passed. (claim: ks-pw-retries-flaky)
- **e2e-fix-flaky-tests**: A flaky E2E test SHOULD be fixed, even where retries let the run pass. (claims: pg-android-retries-fix, ev-fowler-nondeterminism-useless)
- **e2e-trace-on-ci-failure**: A suite SHOULD record a trace for each E2E test that fails on CI, to debug the failure from instead of videos and screenshots. (claim: bp-pw-trace-viewer-on-ci)

### Locators

- **e2e-test-what-the-user-sees**: An E2E spec SHOULD verify what the end user sees and does, interacting with the product as a person would, not its implementation details. (claims: bp-pw-test-user-visible-behavior, pg-tl-guiding-principle, pg-apple-ui-test-as-person)
- **e2e-locators-user-facing-first**: A spec SHOULD locate an element by a user-facing attribute, such as its role and accessible name, its label or its text, or by an explicit contract, such as a test id, in preference to a locator that depends on the DOM structure. (claims: pg-pw-prioritize-user-facing, pg-pw-getbyrole, pg-tl-byrole-top, pg-pw-testid-resilient, ks-wdio-role-selector, pg-aria-accessibility-tree, pg-aria-accessible-name, pg-pw-css-xpath-not-recommended)
- **e2e-locate-by-test-id**: A spec MAY locate an element by a test id: a `data-*` attribute on the web, UIKit's `accessibilityIdentifier` or an AutomationId in Windows UI Automation. (claims: pg-pw-testid-resilient, pg-tl-testid-last, ks-cy-data-attributes, pg-apple-accessibility-identifier, pg-ms-automationid)
- **e2e-compose-finders-over-semantics-tree**: A Compose UI test MAY select the nodes it acts on or asserts on with finders over the semantics tree. (claim: pg-android-compose-semantics)
- **e2e-scope-automation-id-by-container**: A Windows UI Automation locator that uses an AutomationId SHOULD scope it by the element's container. (claims: pg-ms-automationid-scope, pg-ms-automationid)
- **e2e-avoid-dom-structure-locators**: A spec SHOULD NOT locate elements by CSS or XPath selectors that depend on the DOM structure, or by manipulating HTML elements directly. (claims: pg-pw-css-xpath-not-recommended, ks-cy-brittle-selectors, ev-fowler-po-brittle, ev-kcd-queryselector)
- **e2e-prefer-unique-id-to-css-to-xpath**: Where a spec falls back to a structural locator, it SHOULD prefer a unique ID, then a well-written CSS selector, to XPath. (claim: ks-se-locator-preference)

### Hermetic and live specs

- **hermetic-specs-mock-the-api**: A hermetic spec SHOULD guarantee the responses it needs by stubbing the network through the test tool's interception API, such as route mocks or HAR replay, or through a test double. (claims: bp-pw-use-network-api, ks-pw-mock-api, ks-pw-har-replay, ks-cy-stub-majority, ks-se-eliminate-external-services, pg-android-espresso-intents-hermetic, ev-fowler-test-double-remote)
- **e2e-do-not-test-what-you-do-not-control**: An E2E spec SHOULD NOT exercise external sites or third-party servers the team does not control. (claims: bp-pw-only-test-what-you-control, ks-se-eliminate-external-services)
- **e2e-hermetic-by-default-live-for-critical-paths**: A suite SHOULD stub the network in the main, mixed with true end-to-end specs against the real server, which suit the critical paths of the application. (claims: ks-cy-stub-majority, ks-cy-real-server-critical-paths, ks-cy-stub-drift, bp-pw-use-network-api, ev-vocke-e2e-flaky)
- **e2e-live-environment-held-stable**: A spec that runs against a live staging environment SHOULD run against one that is kept from changing. (claim: bp-pw-stable-staging)
- **e2e-select-live-specs-by-tag-or-project**: A suite MAY keep its live specs apart from its hermetic ones by a tag filtered at run time, by a project with its own test filter and settings, or by an environment variable that switches the target. (claims: ks-pw-tags-grep, ks-pw-projects-filter, ks-pw-projects-environments, ks-pw-env-staging-switch)
- **e2e-gate-live-specs-needing-secrets**: A suite run on GitHub Actions MAY gate a live spec that needs repository secrets by where the run comes from, so that it does not run on a workflow triggered from a forked repository, which is passed no secrets other than `GITHUB_TOKEN`. (claim: ks-gha-secrets-forks)

### Secrets

- **no-credentials-or-real-user-data**: A change to E2E specs MUST NOT contain credentials, tokens or API keys: not in fixtures, not in comments, not in mocked responses. (claim: bp-asvs-no-secrets-in-repo)
- **e2e-credentials-from-environment**: A spec SHOULD get the secrets it needs from outside the source code, such as from environment variables or the CI's secret store. (claims: bp-pw-env-secrets, bp-asvs-no-secrets-in-repo)
- **e2e-env-file-git-ignored**: A local environment file that holds sensitive values SHOULD be git-ignored. (claim: ks-cy-env-gitignore)
- **e2e-stored-auth-state-git-ignored**: Stored authentication state, such as a saved browser-state file, SHOULD be kept in a git-ignored directory. (claims: ks-pw-auth-gitignore, ks-pw-auth-state-sensitive)
- **e2e-secrets-kept-from-browser**: A spec SHOULD NOT hand a secret to the browser as a configuration value. (claim: ks-cy-env-values-exposed)
- **e2e-secrets-out-of-ci-logs**: A spec SHOULD keep its secrets from being printed in the CI log. (claim: ks-gha-dont-print)
- **e2e-no-secrets-in-session-id**: A Cypress spec SHOULD keep passwords, tokens and other sensitive data out of the id of a `cy.session`, which Cypress shows in its Command Log. (claim: ks-cy-session-no-passwords-in-id)

### Accounts and test data

- **e2e-synthetic-data-not-real-user-data**: The fixtures, comments and mocked responses of a change to E2E specs SHOULD hold synthetic or fake data in place of real user data. (claims: bp-ico-synthetic-minimisation, ev-thoughtworks-prod-data, ev-thoughtworks-weak-test-security)
- **e2e-dedicated-test-accounts**: A spec that signs in SHOULD sign in as a test account. (claims: ks-pw-account-per-worker, ks-pw-auth-state-sensitive)
- **e2e-account-per-worker**: Tests that change server-side state SHOULD use one test account per parallel worker. (claim: ks-pw-account-per-worker)
- **e2e-standard-test-secrets**: An organisation MAY create standard test secrets and use them universally across the organisation. (claim: bp-owasp-standard-test-secrets)
- **e2e-separate-production-secrets**: A team MAY keep its production secrets in a separate secret-management solution from its development secrets. (claim: bp-owasp-separate-prod-dev)

### What a spec asserts

- **e2e-page-objects-hold-no-assertions**: Where a suite uses page objects, the page objects SHOULD make no verifications or assertions other than checks of their page's own invariants; the test makes them. (claims: ks-se-po-no-assertions, ev-fowler-po-no-assertions)
- **e2e-do-not-repeat-lower-level-assertions**: An E2E spec SHOULD NOT re-test the conditional logic and edge cases that lower-level tests already cover. (claim: ev-vocke-no-retest-lower-level)
- **e2e-focus-on-what-lower-levels-miss**: An E2E spec SHOULD focus on the part of the behaviour that lower-level tests could not cover. (claim: ev-vocke-focus-uncovered)
- **rationale-cites-assertion-source**: A spec's rationale SHOULD cite the feature doc or plan that each of its assertions derives from. (claim: bp-istqb-traceability)
- **rationale-names-what-makes-assertion-correct**: A spec's rationale MUST keep this true: The rationale names the feature doc, plan, or commit the new assertion derives from. A rationale that argues the assertion is sensible, without citing what makes it correct, is a fail. (claim: rationale-names-what-makes-assertion-correct-prior)
- **e2e-link-assertion-source-in-annotation**: A test MAY carry the link to the source of its assertions as an annotation, so that the link appears in the test report. (claim: ks-pw-annotations)

