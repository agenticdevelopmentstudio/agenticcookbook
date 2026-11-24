
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

