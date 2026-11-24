---
id: eb82d5d7-4f42-4417-8104-a14f6a27899f
title: End-to-End Test Authoring
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-24
modified: 2026-11-24
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Writing E2E specs that test what a user does and stay stable: user-facing locators, condition waits, isolated state, hermetic networks, secrets kept out."
platforms: []
tags:
  - e2e-testing
  - locators
  - test-isolation
  - network-mocking
  - test-secrets
depends-on: []
related:
  - 8ab7452a-09b8-4f4e-abfc-f7fd700765db
  - a8f9c003-e970-4f28-bb7d-30a23b891b3f
  - 42220186-4305-45cd-8e7d-a8d1172b6fbd
  - abdcd282-5b81-4ab2-ab1e-3ed288a4aee5
  - 0de6da80-6793-4ef5-afd3-c7663da1d952
  - 4f5fe9ef-1bf8-4354-92c7-92d9e28673b8
references:
  - https://playwright.dev/docs/best-practices
  - https://playwright.dev/docs/api/class-page
  - https://playwright.dev/docs/actionability
  - https://playwright.dev/docs/locators
  - https://playwright.dev/docs/mock
  - https://playwright.dev/docs/browser-contexts
  - https://playwright.dev/docs/test-fixtures
  - https://playwright.dev/docs/clock
  - https://playwright.dev/docs/test-retries
  - https://playwright.dev/docs/test-annotations
  - https://playwright.dev/docs/test-projects
  - https://playwright.dev/docs/test-parameterize
  - https://playwright.dev/docs/auth
  - https://docs.cypress.io/app/core-concepts/best-practices
  - https://docs.cypress.io/app/guides/network-requests
  - https://docs.cypress.io/app/guides/environment-variables
  - https://docs.cypress.io/api/commands/session
  - https://webdriver.io/docs/selectors/
  - https://webdriver.io/docs/bestpractices/
  - https://www.selenium.dev/documentation/test_practices/encouraged/locators/
  - https://www.selenium.dev/documentation/webdriver/waits/
  - https://www.selenium.dev/documentation/test_practices/encouraged/avoid_sharing_state/
  - https://www.selenium.dev/documentation/test_practices/encouraged/generating_application_state/
  - https://www.selenium.dev/documentation/test_practices/encouraged/mock_external_services/
  - https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
  - https://testing-library.com/docs/queries/about/
  - https://www.w3.org/TR/wai-aria-1.2/
  - https://developer.apple.com/documentation/xcuiautomation
  - https://developer.apple.com/documentation/uikit/uiaccessibilityidentification/accessibilityidentifier
  - https://developer.apple.com/documentation/xcuiautomation/xcuielement/waitforexistence(timeout:)
  - https://developer.android.com/training/testing/instrumented-tests/stability
  - https://developer.android.com/training/testing/espresso/idling-resource
  - https://developer.android.com/training/testing/espresso
  - https://developer.android.com/develop/ui/compose/testing/apis
  - https://developer.android.com/training/testing/other-components/ui-automator
  - https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/use-the-automationid-property
  - https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
  - https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
  - https://raw.githubusercontent.com/OWASP/ASVS/v4.0.3/4.0/en/0x11-V2-Authentication.md
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data
  - https://martinfowler.com/articles/nonDeterminism.html
  - https://martinfowler.com/bliki/PageObject.html
  - https://martinfowler.com/articles/practical-test-pyramid.html
  - https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
  - https://www.thoughtworks.com/radar/techniques/production-data-in-test-environments
approved-by: ""
approved-date: ""
triggers:
  - writing-tests
  - pre-pr
---

# End-to-End Test Authoring

Write each end-to-end (E2E) spec to test what a user sees and does, locating elements by role, name, label or text, and never waiting a fixed time: wait on a condition instead. Keep every test's state isolated and set up programmatically, stub the network for most specs and keep live runs for the critical paths, and never commit credentials or tokens; take secrets from outside the source, use synthetic data and test accounts, and trace each assertion to the feature doc or plan it derives from.

This guideline covers how an E2E spec is written, for any team that tests a product through its user interface on the web, Apple platforms, Android or Windows: the locators it uses and avoids, how it waits, how it keeps each test's state isolated, when it stubs the network and when it runs against a live environment and how the two are kept apart, how it gets test accounts and secrets, and how it states the rationale for what it asserts. It does not cover whether E2E runs at all and which journeys it covers, which belong to the testing workflow; which E2E tool a TypeScript project uses, which belongs to comprehensive unit testing; how many E2E tests a suite holds, which belongs to the test pyramid; contracts between services, which belong to contract testing; preview environments, which belong to ephemeral preview environments; quarantining a flaky test, which belongs to flaky test quarantine; or classifying a failed test, which belongs to test failure triage. Following it means keeping every MUST and MUST NOT rule below, and keeping each SHOULD and SHOULD NOT rule or stating why a spec departs from it.

## Rules

### Determinism and waiting

- **write-deterministic-specs**: An E2E spec SHOULD be deterministic, so that it does not pass on some runs and fail on others. (claims: ev-fowler-nondeterminism-useless, bp-pw-wait-for-timeout-flaky, ks-se-sleep-fails, bp-pw-tests-fully-isolated)
- **e2e-wait-on-conditions-not-time**: An E2E spec MUST NOT wait a fixed time, such as a sleep, a pause or a wait for a timeout, for the application to be ready. (claims: bp-pw-wait-for-timeout-flaky, ev-fowler-no-bare-sleeps)
- **e2e-wait-for-a-condition**: Where a spec has to wait, it SHOULD wait until a specific condition is met, through an action that auto-waits for actionability, an assertion that retries until its condition holds, or an explicit wait for an element or state. (claims: pg-android-wait-until, pg-android-avoid-sleep, ks-pw-auto-wait-actionability, bp-pw-web-first-assertions, ks-wdio-auto-retry-assertions, ks-wdio-no-pause, bp-cy-no-arbitrary-wait, pg-apple-wait-for-existence, pg-android-espresso-sync, ev-kcd-find-for-async)
- **e2e-register-long-running-work**: A suite that uses Espresso MUST register each long-running operation of the app that Espresso does not know of as an idling resource. (claim: pg-android-idling-resources)
- **e2e-no-mixed-waits**: Where the tool has both implicit and explicit waits, as Selenium WebDriver does, a spec SHOULD NOT mix them. (claim: ks-se-no-mix-waits)
- **e2e-control-the-clock**: A spec that tests time-dependent behaviour SHOULD control the clock, through the tool's clock API or a wrapped system clock, rather than depend on real time. (claims: bp-pw-clock-control, ev-fowler-wrap-clock)

### Test state

- **e2e-isolate-test-state**: Each E2E test SHOULD run independently of every other test and still pass, relying on no state another test left, so that tests can run in parallel. (claims: bp-pw-tests-fully-isolated, bp-cy-tests-independent, ev-fowler-isolated, ks-pw-parallel-default)
- **e2e-fresh-browser-session-per-test**: Each test SHOULD get its own browser session, such as a new browser context or a new driver instance, with its own storage and cookies. (claims: ks-pw-browser-context-isolation, ks-se-new-driver-per-test)
- **e2e-no-shared-test-data**: Tests SHOULD NOT share test data. (claim: ks-se-no-shared-data)
- **e2e-control-database-data**: A spec that works with a database SHOULD control the data in it. (claim: bp-pw-control-database-data)
- **e2e-reset-state-before-each-test**: State SHOULD be reset before each test runs, such as by clearing the app's data, rather than cleaned up after it. (claims: bp-cy-clean-state-before, pg-android-uiautomator-clear-data)
- **e2e-set-up-state-programmatically**: A spec SHOULD log in and set up the application's state programmatically, such as through an API, rather than through the browser. (claims: bp-cy-programmatic-login, ks-se-api-login)
- **e2e-fixtures-give-only-what-test-needs**: Where a suite uses fixtures, each fixture SHOULD give the test everything it needs and nothing else. (claim: ks-pw-fixtures-isolated)

### Retries, flakiness and traces

- **e2e-retries-surface-flakiness**: Where a run retries failed E2E tests, a test that failed first and passed on retry SHOULD be reported as flaky, not as passed. (claim: ks-pw-retries-flaky)
- **e2e-fix-flaky-tests**: A flaky E2E test SHOULD be fixed, even where retries let the run pass. (claims: pg-android-retries-fix, ev-fowler-nondeterminism-useless)
- **e2e-trace-on-ci-failure**: A failing E2E test on CI SHOULD be debugged from a recorded trace rather than from videos and screenshots. (claim: bp-pw-trace-viewer-on-ci)

### Locators

- **e2e-test-what-the-user-sees**: An E2E spec SHOULD verify what the end user sees and does, interacting with the product as a person would, not its implementation details. (claims: bp-pw-test-user-visible-behavior, pg-tl-guiding-principle, pg-apple-ui-test-as-person)
- **e2e-locators-user-facing-first**: A spec SHOULD locate an element first by user-facing attributes: its role and accessible name, then its label or text. (claims: pg-pw-prioritize-user-facing, pg-pw-getbyrole, pg-tl-byrole-top, ks-wdio-role-selector, pg-aria-accessibility-tree, pg-aria-accessible-name)
- **e2e-test-id-where-no-user-facing-locator**: Where no role or text match fits, a spec MAY locate the element by a test id: a `data-*` attribute on the web, an `accessibilityIdentifier` on Apple platforms, a test tag in Compose or an AutomationId on Windows. (claims: pg-tl-testid-last, pg-pw-testid-resilient, ks-cy-data-attributes, pg-apple-accessibility-identifier, pg-android-compose-semantics, pg-ms-automationid)
- **e2e-scope-automation-id-by-container**: A Windows UI Automation locator that uses an AutomationId SHOULD scope it by the element's container. (claims: pg-ms-automationid-scope, pg-ms-automationid)
- **e2e-avoid-dom-structure-locators**: A spec SHOULD NOT locate elements by CSS or XPath selectors that depend on the DOM structure, or by manipulating HTML elements directly. (claims: pg-pw-css-xpath-not-recommended, ks-cy-brittle-selectors, ev-fowler-po-brittle, ev-kcd-queryselector)
- **e2e-prefer-unique-id-to-css-to-xpath**: Where a spec falls back to a structural locator, it SHOULD prefer a unique ID, then a well-written CSS selector, to XPath. (claim: ks-se-locator-preference)

### Hermetic and live specs

- **hermetic-specs-mock-the-api**: A hermetic spec SHOULD guarantee the responses it needs by stubbing the network through the test tool's interception API, such as route mocks or HAR replay, or through a test double. (claims: bp-pw-use-network-api, ks-pw-mock-api, ks-pw-har-replay, ks-cy-stub-majority, ks-se-eliminate-external-services, pg-android-espresso-intents-hermetic, ev-fowler-test-double-remote)
- **e2e-do-not-test-what-you-do-not-control**: An E2E spec SHOULD NOT exercise external sites or third-party servers the team does not control. (claims: bp-pw-only-test-what-you-control, ks-se-eliminate-external-services)
- **e2e-hermetic-by-default-live-for-critical-paths**: Most E2E specs SHOULD stub the network, with specs against the real server used sparingly, for the critical paths. (claims: ks-cy-stub-majority, ks-cy-real-server-critical-paths, ks-cy-stub-drift, ev-vocke-e2e-flaky)
- **e2e-live-environment-held-stable**: A spec that runs against a live staging environment SHOULD run against one that is kept from changing. (claim: bp-pw-stable-staging)
- **e2e-select-live-specs-by-tag-or-project**: A suite MAY keep its live specs apart from its hermetic ones by a tag filtered at run time, by a project with its own test filter and settings, or by an environment variable that switches the target. (claims: ks-pw-tags-grep, ks-pw-projects-filter, ks-pw-projects-environments, ks-pw-env-staging-switch)
- **e2e-gate-live-specs-needing-secrets**: A suite MAY gate a live spec that needs CI secrets by where the run comes from, so it does not run on a workflow triggered from a forked repository, where the secrets are withheld. (claim: ks-gha-secrets-forks)

### Secrets

- **no-credentials-or-real-user-data**: A change to E2E specs MUST NOT contain credentials, tokens or API keys: not in fixtures, not in comments, not in mocked responses. (claim: bp-asvs-no-secrets-in-repo)
- **e2e-credentials-from-environment**: A spec SHOULD get the secrets it needs from outside the source code, such as from environment variables or the CI's secret store. (claims: bp-pw-env-secrets, bp-asvs-no-secrets-in-repo)
- **e2e-env-file-git-ignored**: A local environment file that holds sensitive values SHOULD be git-ignored. (claim: ks-cy-env-gitignore)
- **e2e-stored-auth-state-git-ignored**: Stored authentication state, such as a saved browser-state file, SHOULD be kept in a git-ignored directory. (claims: ks-pw-auth-gitignore, ks-pw-auth-state-sensitive)
- **e2e-secrets-kept-from-browser**: A spec SHOULD NOT hand a secret to the browser as a configuration value. (claim: ks-cy-env-values-exposed)
- **e2e-secrets-out-of-logs**: A spec SHOULD keep passwords, tokens and other secrets out of the test log and the CI log, including the ids under which sessions are cached. (claims: ks-cy-session-no-passwords-in-id, ks-gha-dont-print)

### Accounts and test data

- **e2e-synthetic-data-not-real-user-data**: The fixtures, comments and mocked responses of a change to E2E specs SHOULD hold synthetic or fake data in place of real user data. (claims: bp-ico-synthetic-minimisation, ev-thoughtworks-prod-data, ev-thoughtworks-weak-test-security)
- **e2e-dedicated-test-accounts**: Specs SHOULD use dedicated test accounts and standard test secrets rather than real ones. (claim: bp-owasp-standard-test-secrets)
- **e2e-account-per-worker**: Tests that change server-side state SHOULD use one test account per parallel worker. (claim: ks-pw-account-per-worker)
- **e2e-separate-production-secrets**: A team MAY keep its production secrets in a separate secret-management solution from its development and test secrets. (claim: bp-owasp-separate-prod-dev)

### What a spec asserts

- **e2e-page-objects-hold-no-assertions**: Where a suite uses page objects, the page objects SHOULD make no verifications or assertions; the test makes them. (claims: ks-se-po-no-assertions, ev-fowler-po-no-assertions)
- **e2e-do-not-repeat-lower-level-assertions**: An E2E spec SHOULD NOT re-test the conditional logic and edge cases that lower-level tests already cover. (claim: ev-vocke-no-retest-lower-level)
- **e2e-focus-on-what-lower-levels-miss**: An E2E spec SHOULD focus on the part of the behaviour that lower-level tests could not cover. (claim: ev-vocke-focus-uncovered)
- **rationale-cites-assertion-source**: A spec's rationale SHOULD cite the feature doc or plan that each of its assertions derives from. (claim: bp-istqb-traceability)
- **rationale-names-what-makes-assertion-correct**: A spec's rationale MUST keep this true: The rationale names the feature doc, plan, or commit the new assertion derives from. A rationale that argues the assertion is sensible, without citing what makes it correct, is a fail. (claim: rationale-names-what-makes-assertion-correct-prior)
- **e2e-link-assertion-source-in-annotation**: A test MAY carry the link to the source of its assertions as an annotation, so that the link appears in the test report. (claim: ks-pw-annotations)

## Writing a spec

This section is informative: it shows one way to keep the rules, not a required method.

1. Start from the behaviour the user sees, and from the feature doc or plan that says what it should be. Leave the conditional logic and edge cases to the unit and integration tests that already cover them; the E2E spec covers what those tests could not.
2. Locate each element the way a user finds it. In Playwright that is `getByRole` with a name, then `getByLabel` or `getByText`; in Testing Library the `*ByRole` queries come first. Where nothing user-facing fits, add a test id to the element: a `data-testid` or other `data-*` attribute on the web, `accessibilityIdentifier` in UIKit or SwiftUI, a test tag in Compose, or an AutomationId on Windows, scoped by its container.
3. Wait on conditions. Playwright's actions auto-wait for actionability and its web-first assertions retry until they hold; WebdriverIO's assertions retry the same way. Testing Library's `find*` queries wait for an element that may not be there yet. On Apple platforms use `waitForExistence(timeout:)`; with Espresso, register the app's long-running work as idling resources; on Android generally, wait until a specific condition is met. In Selenium pick explicit waits or implicit waits, not both.
4. Give each test a fresh session and its own data. Playwright gives each test a new browser context; Selenium creates a new WebDriver instance per test. Reset state before the test, not after it, and log in through an API or a saved, git-ignored auth state rather than through the login form, except in the spec that tests the login form.
5. Stub what the spec does not own. Playwright's `page.route` and `routeFromHAR`, Cypress's `cy.intercept` stubs, Espresso-Intents and a test double for remote services all guarantee the response the spec needs. Keep a few specs against the real server for the critical paths, and run them against a staging environment that is kept from changing.
6. Keep live specs apart from hermetic ones by a tag and `--grep`, by a separate project with its own filter and retries, or by an environment variable that selects the target; the sources prefer none of these.
7. Take credentials from environment variables or the CI's secret store, keep any local env file and stored auth state out of git, and keep secrets out of logs and out of values handed to the browser. Use dedicated test accounts, one per parallel worker where tests change server-side state, and synthetic data in fixtures and mocked responses.
8. Turn on traces for CI failures, and debug from the trace.

How the tools compare:

- **Playwright** auto-waits before actions, retries web-first assertions, isolates each test in a browser context, runs tests in parallel by default, mocks HTTP and HTTPS and replays HAR files matched strictly on URL and method, controls the clock, tags tests and selects them with `--grep`, splits tests into projects with their own settings, reports a test that passed only on retry as flaky, and records traces.
- **Cypress** stubs responses with `cy.intercept`, recommends `data-*` attributes as selectors, lists arbitrary waits and brittle selectors as anti-patterns, and keeps its env file out of git.
- **WebdriverIO** puts role plus accessible name first among its selectors, calls fixed pauses a bad idea, and retries its assertions.
- **Selenium** offers implicit and explicit waits, recommends a new driver per test, no shared test data, logging in by API and mocking external services, and keeps assertions out of page objects. Its own locator order (unique IDs, then CSS, then XPath) predates the user-facing-first order of the other tools.
- **Apple XCUIAutomation** drives the interface as a person would, identifies elements by `accessibilityIdentifier` and waits with `waitForExistence(timeout:)`.
- **Android** Espresso synchronises with the UI through idling resources, Espresso-Intents stubs intents for hermetic testing, Compose finds nodes in the semantics tree, and UI Automator resets an app by clearing its data.
- **Windows UI Automation** identifies an element among its siblings by AutomationId, which needs its container to be unique.

## Examples

This section is informative; the entries below are illustrations, not a format the guideline requires.

A Playwright spec that keeps the rules:

```typescript
import { test, expect } from '@playwright/test';

test('a signed-in user sees their saved address at checkout', {
  annotation: { type: 'source', description: 'docs/features/checkout.md#saved-addresses' },
}, async ({ page }) => {
  // Hermetic: the address API returns synthetic data.
  await page.route('**/api/addresses', route =>
    route.fulfill({ json: [{ id: 'a1', line1: '1 Test Street', city: 'Exampleton' }] }));

  await page.goto('/checkout');
  await page.getByRole('button', { name: 'Use saved address' }).click();

  // A web-first assertion waits until the text appears; no fixed timeout.
  await expect(page.getByText('1 Test Street')).toBeVisible();
});
```

The same wait, written against the rules and then kept:

| Breaks a rule | Keeps it |
|---|---|
| `await page.waitForTimeout(2000)` | `await expect(page.getByRole('alert')).toHaveText('Saved')` |
| `page.locator('div.form > div:nth-child(3) > button')` | `page.getByRole('button', { name: 'Save' })` |
| `const password = 'hunter2'` | `const password = process.env.TEST_USER_PASSWORD` |

A rationale for a new assertion:

> Asserts that the saved address is offered at checkout, as `docs/features/checkout.md#saved-addresses` specifies for signed-in users.

## What a reviewer looks for

Checks that no spec waits a fixed time and that every wait is on a condition, that a suite using Espresso registers the app's long-running work as idling resources, that Selenium specs do not mix implicit and explicit waits, and that time-dependent behaviour runs on a controlled clock. Checks that each test runs alone and in parallel, with its own browser session and its own data, its state reset before it runs and set up programmatically, and its fixtures giving it only what it needs. Checks that locators face the user first, by role and accessible name, then label or text, with a test id only where nothing user-facing fits, an AutomationId scoped by its container, and no CSS or XPath paths through the DOM. Checks that hermetic specs stub the network through the tool's interception API or a test double, that no spec exercises a third party the team does not control, that live specs are few, kept for the critical paths, run against a stable environment and kept apart from hermetic ones. Above all, checks that the change contains no credentials, tokens or API keys anywhere, fixtures, comments and mocked responses included; that secrets come from outside the source and stay out of logs and out of the browser; that env files and stored auth state are git-ignored; that data is synthetic and accounts are dedicated test accounts; and that each new assertion's rationale names the feature doc, plan or commit it derives from. Checks too that page objects hold no assertions, that the E2E spec does not repeat what lower-level tests cover, that a test passing only on retry is reported as flaky and fixed, and that CI failures come with a trace.

## A complete review must establish

- Each MUST and MUST NOT rule is kept, with no exception: `e2e-wait-on-conditions-not-time`: no spec waits a fixed time for the application to be ready; `e2e-register-long-running-work`: a suite that uses Espresso registers each long-running operation Espresso does not know of as an idling resource; `no-credentials-or-real-user-data`: the change holds no credentials, tokens or API keys in its fixtures, comments or mocked responses; `rationale-names-what-makes-assertion-correct`: each new assertion's rationale names the feature doc, plan or commit it derives from.
- Each SHOULD and SHOULD NOT rule is kept or its departure is stated: `write-deterministic-specs`, `e2e-wait-for-a-condition`, `e2e-no-mixed-waits`, `e2e-control-the-clock`, `e2e-isolate-test-state`, `e2e-fresh-browser-session-per-test`, `e2e-no-shared-test-data`, `e2e-control-database-data`, `e2e-reset-state-before-each-test`, `e2e-set-up-state-programmatically`, `e2e-fixtures-give-only-what-test-needs`, `e2e-retries-surface-flakiness`, `e2e-fix-flaky-tests`, `e2e-trace-on-ci-failure`, `e2e-test-what-the-user-sees`, `e2e-locators-user-facing-first`, `e2e-scope-automation-id-by-container`, `e2e-avoid-dom-structure-locators`, `e2e-prefer-unique-id-to-css-to-xpath`, `hermetic-specs-mock-the-api`, `e2e-do-not-test-what-you-do-not-control`, `e2e-hermetic-by-default-live-for-critical-paths`, `e2e-live-environment-held-stable`, `e2e-credentials-from-environment`, `e2e-env-file-git-ignored`, `e2e-stored-auth-state-git-ignored`, `e2e-secrets-kept-from-browser`, `e2e-secrets-out-of-logs`, `e2e-synthetic-data-not-real-user-data`, `e2e-dedicated-test-accounts`, `e2e-account-per-worker`, `e2e-page-objects-hold-no-assertions`, `e2e-do-not-repeat-lower-level-assertions`, `e2e-focus-on-what-lower-levels-miss`, `rationale-cites-assertion-source`.
- Each MAY rule is noted where it was used: `e2e-test-id-where-no-user-facing-locator`, `e2e-select-live-specs-by-tag-or-project`, `e2e-gate-live-specs-needing-secrets`, `e2e-separate-production-secrets`, `e2e-link-assertion-source-in-annotation`.

## A build must establish

- `write-deterministic-specs`: each spec passes or fails the same way on every run of the same code.
- `e2e-wait-on-conditions-not-time`: no spec waits a fixed time for the application to be ready.
- `e2e-wait-for-a-condition`: every wait in a spec is on a specific condition.
- `e2e-register-long-running-work`: in a suite that uses Espresso, each long-running operation Espresso does not know of is registered as an idling resource.
- `e2e-no-mixed-waits`: no spec mixes implicit and explicit waits.
- `e2e-control-the-clock`: each spec of time-dependent behaviour runs on a controlled clock.
- `e2e-isolate-test-state`: each test passes when run alone and relies on no state another test left.
- `e2e-fresh-browser-session-per-test`: each test runs in its own browser session, with its own storage and cookies.
- `e2e-no-shared-test-data`: no two tests share test data.
- `e2e-control-database-data`: each spec that works with a database controls the data in it.
- `e2e-reset-state-before-each-test`: state is reset before each test runs.
- `e2e-set-up-state-programmatically`: login and application state are set up programmatically, not through the browser.
- `e2e-fixtures-give-only-what-test-needs`: where fixtures are used, each gives the test what it needs and nothing else.
- `e2e-retries-surface-flakiness`: where retries run, a test that passed only on retry is reported as flaky.
- `e2e-fix-flaky-tests`: each flaky test found is fixed, not left passing on retry.
- `e2e-trace-on-ci-failure`: a failing E2E test on CI leaves a trace to debug from.
- `e2e-test-what-the-user-sees`: each spec checks what the end user sees and does.
- `e2e-locators-user-facing-first`: each locator uses role and accessible name, label or text where one fits.
- `e2e-test-id-where-no-user-facing-locator`: where used, each test id locates an element no role or text match fits.
- `e2e-scope-automation-id-by-container`: each AutomationId locator is scoped by its container.
- `e2e-avoid-dom-structure-locators`: no locator is a CSS or XPath path through the DOM structure.
- `e2e-prefer-unique-id-to-css-to-xpath`: each structural fallback locator is a unique ID, else a CSS selector, before XPath.
- `hermetic-specs-mock-the-api`: each hermetic spec stubs its network responses through the tool's interception API or a test double.
- `e2e-do-not-test-what-you-do-not-control`: no spec exercises an external site or third-party server the team does not control.
- `e2e-hermetic-by-default-live-for-critical-paths`: most specs stub the network, and live specs cover critical paths.
- `e2e-live-environment-held-stable`: each live spec runs against an environment kept from changing.
- `e2e-select-live-specs-by-tag-or-project`: where used, live specs are selected by a tag, a project or an environment variable.
- `e2e-gate-live-specs-needing-secrets`: where used, live specs that need CI secrets do not run on fork-triggered workflows.
- `no-credentials-or-real-user-data`: the change holds no credentials, tokens or API keys, in fixtures, comments or mocked responses.
- `e2e-credentials-from-environment`: each secret a spec uses comes from outside the source code.
- `e2e-env-file-git-ignored`: each local env file holding sensitive values is git-ignored.
- `e2e-stored-auth-state-git-ignored`: stored authentication state lives in a git-ignored directory.
- `e2e-secrets-kept-from-browser`: no secret is handed to the browser as a configuration value.
- `e2e-secrets-out-of-logs`: no password, token or other secret appears in the test or CI log.
- `e2e-synthetic-data-not-real-user-data`: fixtures, comments and mocked responses hold synthetic data, not real user data.
- `e2e-dedicated-test-accounts`: specs use dedicated test accounts and standard test secrets.
- `e2e-account-per-worker`: tests that change server-side state use one test account per parallel worker.
- `e2e-separate-production-secrets`: where used, production secrets sit in a separate secret store.
- `e2e-page-objects-hold-no-assertions`: no page object makes a verification or assertion.
- `e2e-do-not-repeat-lower-level-assertions`: no E2E spec re-tests logic and edge cases lower-level tests cover.
- `e2e-focus-on-what-lower-levels-miss`: each E2E spec covers behaviour lower-level tests could not.
- `rationale-cites-assertion-source`: each spec's rationale cites the feature doc or plan its assertions derive from.
- `rationale-names-what-makes-assertion-correct`: each new assertion's rationale names the feature doc, plan or commit it derives from.
- `e2e-link-assertion-source-in-annotation`: where used, each test's annotation links to the source of its assertions.

## Rationale

This section is informative.

Non-deterministic tests are useless, in Fowler's words, and E2E tests are where non-determinism shows: Vocke calls them notoriously flaky. Waiting on time is the commonest cause. Playwright's API reference says never to wait for timeout, because tests that wait for time are inherently flaky, and Fowler says never to use bare sleeps; those two sources are why the fixed-wait rule is a MUST NOT. Android, Selenium, WebdriverIO and Cypress reject sleeps too, but in recommending words, so the rule that says what to wait on instead is a SHOULD. Selenium explains the failure: the code cannot know how long it needs to wait. Espresso is the one platform that requires a mechanism: its documentation says each long-running operation it does not know of must be registered as an idling resource, which is why that rule alone among the waiting rules is a MUST.

Isolation lets tests run alone and in parallel, which Playwright does by default. Playwright, Cypress, Selenium and Fowler all ask for it in recommending words. Setting state up through an API instead of the browser, Cypress and Selenium say, makes tests faster and more stable. Retries are offered by Playwright and Android, and both treat a test that passes on retry as flaky rather than passed; Android adds that flaky tests are always fixed. Quarantining a flaky test belongs to flaky test quarantine.

The locator rules rest on Playwright's locator guide, Testing Library's query priority and WebdriverIO's selector guide, which put role and accessible name first; role locators rest on the accessibility tree and the accessible name WAI-ARIA defines. Playwright says CSS and XPath are not recommended because the DOM changes, and Fowler and Kent C. Dodds say tests that reach into HTML or query by selector are brittle and lose confidence. Selenium's older order, unique IDs then CSS then XPath, is the outlier; it is kept only for the fallback a spec uses when nothing user-facing or test-id-based fits. Apple, Android and Microsoft each publish an identifier for automation, and Microsoft notes an AutomationId is unique only among its siblings. Several of the claims these rules cite were refuted in part by the second check, so none of the locator rules is a MUST.

Stubbing the network is how Playwright, Cypress, Selenium, Android and Fowler make a spec deterministic against servers it does not control. Cypress sets out the trade-off: stubbed responses carry no guarantee of matching the real server, so it keeps one true end-to-end test and stubs the rest, and keeps real-server tests for the critical paths. The tools show three ways to separate live from hermetic runs and prefer none, so that rule is a MAY. GitHub Actions withholds secrets from runs triggered from forks, which is the reason to gate a live spec that needs them.

Keeping credentials out of the repository is a MUST because OWASP ASVS 2.10.4 requires that passwords, secrets and API keys not be included in source code or stored in source repositories; fixtures, comments and mocked responses are all in the repository. The rule keeps its prior name, `no-credentials-or-real-user-data`, because rule names stay stable, but its real-user-data half is now `e2e-synthetic-data-not-real-user-data`, at SHOULD: it rests on the ICO's data-minimisation guidance, which does not name testing, and on Thoughtworks' Hold on production data in test environments, not on a test-specific requirement. Playwright and Cypress pass secrets in from environment variables and git-ignore stored auth state and env files, in recommending words, so those rules are SHOULD. OWASP's advice on standard test secrets is community guidance, and its advice to separate production secrets says only "consider", so that rule is a MAY.

Page objects that make no assertions come from Selenium, which says they never should, and from Fowler, who states it as his preference. Not repeating lower-level assertions in E2E comes from Vocke's practical test pyramid, a practitioner source; how many E2E tests a suite holds belongs to the test pyramid.

Tracing an assertion to the feature doc or plan it derives from rests on ISTQB, which calls traceability between the test basis and test cases important; that supports a SHOULD, and `rationale-cites-assertion-source` says so. The rule `rationale-names-what-makes-assertion-correct` keeps its prior text, which makes an untraced rationale a fail; no source makes it one, and whether it stays a MUST or becomes a SHOULD is the owner's decision.

Several other questions are the owner's and are left open here: whether a test id may be a first-choice locator, since Playwright calls test ids the most resilient way of testing while Testing Library recommends them only when no role or text match fits; whether hermetic is the default for every spec and how many live specs a suite keeps; how live specs are selected and gated; whether CI retries are allowed for E2E specs and how many; whether keeping real user data out of a change is a MUST; and whether page objects are recommended, allowed or left to the team, since Cypress lists sharing page objects as an anti-pattern while Selenium and Playwright's fixture guide build on them.

No published study was found that measures flake rates by locator type or waiting strategy; the stability rules rest on the tool owners' documentation and practitioner experience. Apple publishes no text on locator priority or on fixed sleeps beyond `waitForExistence(timeout:)`.

## References

This section is informative; every reference below is informative, and none is normative.

- Playwright, *Best Practices*, *Page* (`waitForTimeout`), *Auto-waiting*, *Locators*, *Mock APIs*, *Isolation*, *Fixtures*, *Clock*, *Retries*, *Annotations*, *Projects*, *Parameterize tests* and *Authentication*: https://playwright.dev/docs/best-practices, https://playwright.dev/docs/api/class-page, https://playwright.dev/docs/actionability, https://playwright.dev/docs/locators, https://playwright.dev/docs/mock, https://playwright.dev/docs/browser-contexts, https://playwright.dev/docs/test-fixtures, https://playwright.dev/docs/clock, https://playwright.dev/docs/test-retries, https://playwright.dev/docs/test-annotations, https://playwright.dev/docs/test-projects, https://playwright.dev/docs/test-parameterize, https://playwright.dev/docs/auth
- Cypress, *Best Practices*, *Network Requests*, *Environment Variables* and *session*: https://docs.cypress.io/app/core-concepts/best-practices, https://docs.cypress.io/app/guides/network-requests, https://docs.cypress.io/app/guides/environment-variables, https://docs.cypress.io/api/commands/session
- WebdriverIO, *Selectors* and *Best Practices*: https://webdriver.io/docs/selectors/, https://webdriver.io/docs/bestpractices/
- Selenium, *Tips on working with locators*, *Waiting Strategies*, *Avoid Sharing State*, *Generating application state*, *Mock External Services* and *Page object models*: https://www.selenium.dev/documentation/test_practices/encouraged/locators/, https://www.selenium.dev/documentation/webdriver/waits/, https://www.selenium.dev/documentation/test_practices/encouraged/avoid_sharing_state/, https://www.selenium.dev/documentation/test_practices/encouraged/generating_application_state/, https://www.selenium.dev/documentation/test_practices/encouraged/mock_external_services/, https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
- Testing Library, *About Queries*: https://testing-library.com/docs/queries/about/
- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*: https://www.w3.org/TR/wai-aria-1.2/
- Apple Developer Documentation, *XCUIAutomation*, *accessibilityIdentifier* and *waitForExistence(timeout:)*: https://developer.apple.com/documentation/xcuiautomation, https://developer.apple.com/documentation/uikit/uiaccessibilityidentification/accessibilityidentifier, https://developer.apple.com/documentation/xcuiautomation/xcuielement/waitforexistence(timeout:)
- Android Developers, *Big test stability*, *Espresso idling resources*, *Espresso*, *Testing APIs (Compose)* and *UI Automator*: https://developer.android.com/training/testing/instrumented-tests/stability, https://developer.android.com/training/testing/espresso/idling-resource, https://developer.android.com/training/testing/espresso, https://developer.android.com/develop/ui/compose/testing/apis, https://developer.android.com/training/testing/other-components/ui-automator
- Microsoft Learn, *Use the AutomationID Property*: https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/use-the-automationid-property
- GitHub Docs, *Using secrets in GitHub Actions*: https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1*, section 1.4.4: https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- OWASP, *Application Security Verification Standard 4.0.3*, requirement 2.10.4, and *Secrets Management Cheat Sheet*: https://raw.githubusercontent.com/OWASP/ASVS/v4.0.3/4.0/en/0x11-V2-Authentication.md, https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- ICO, *Synthetic data*: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data
- Martin Fowler, *Eradicating Non-Determinism in Tests* and *PageObject*: https://martinfowler.com/articles/nonDeterminism.html, https://martinfowler.com/bliki/PageObject.html
- Ham Vocke, *The Practical Test Pyramid*: https://martinfowler.com/articles/practical-test-pyramid.html
- Kent C. Dodds, *Common mistakes with React Testing Library*: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- Thoughtworks Technology Radar, *Production data in test environments*: https://www.thoughtworks.com/radar/techniques/production-data-in-test-environments

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-24 | Mike Fullerton | Initial creation, written from research |
