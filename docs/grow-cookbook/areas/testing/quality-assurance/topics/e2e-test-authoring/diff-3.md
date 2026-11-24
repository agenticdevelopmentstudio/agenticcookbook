--- draft-2.md
+++ draft.md
@@ -184,10 +184,10 @@
 - **Playwright** auto-waits before actions, has web-first assertions that wait for their condition, gives each test its own storage and cookies, runs tests in parallel by default, mocks HTTP and HTTPS and replays HAR files matched strictly on URL and method, controls the clock, tags tests, splits tests into projects with filters and their own settings, reports a test that passed only on retry as flaky, and records traces.
 - **Cypress** stubs responses with `cy.intercept`, recommends `data-*` attributes as selectors, lists arbitrary waits and brittle selectors as anti-patterns, keeps its env file out of git, and shows a session's id in its Command Log.
 - **WebdriverIO** notes that a role plus a name keeps matching when class names, test ids or the DOM structure change, calls fixed pauses a bad idea, and retries its assertions.
-- **Selenium** offers implicit and explicit waits, recommends a new driver per test, no shared test data, logging in by API and mocking external services, and keeps assertions out of page objects. Its own locator order (unique IDs, then CSS, then XPath) is for structural locators.
+- **Selenium** offers implicit and explicit waits, recommends a new driver per test, no shared test data, logging in by API and mocking external services, and keeps assertions out of page objects. It ranks unique IDs, then a well-written CSS selector, above XPath; this guideline applies that order to the structural locator a spec falls back to.
 - **Apple XCUIAutomation** drives the interface as a person would and waits with `waitForExistence(timeout:)`; UIKit's `accessibilityIdentifier` identifies an element for UI automation.
 - **Android** Espresso synchronises with the UI through idling resources, Espresso-Intents stubs intents for hermetic testing, Compose finders select nodes in the semantics tree, and UI Automator resets an app by clearing its data.
-- **Windows UI Automation** identifies an element among its siblings by AutomationId, which needs container and scope information to be useful.
+- **Windows UI Automation** identifies an element among its siblings by AutomationId, which typically needs container and scope information to be useful.
 
 ## Examples
 
