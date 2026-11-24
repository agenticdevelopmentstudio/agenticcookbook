## pg-pw-prioritize-user-facing
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Playwright locators page says it word for word ("we recommend prioritizing user-facing attributes and explicit contracts such as page.getByRole()").

## pg-pw-getbyrole
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is the first entry in the page's quick-guide list of recommended locators.

## pg-tl-guiding-principle
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It opens the "Priority" section of the Testing Library queries page.

## pg-tl-byrole-top
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence is about getByRole, which "can be used to query every element that is exposed in the accessibility tree".

## ks-wdio-role-selector
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote only says that role plus name keeps matching through class, test-id and DOM changes; it makes no recommendation. "Prefer the role selector" appears elsewhere, and only in contrast to `[role=button]`. The page's own selector table rates `button=Submit` "Always / Best" and `aria/` only "Good".
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## pg-aria-accessibility-tree
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: WAI-ARIA 1.2 does define the accessibility tree this way (the source writes "( UI)", a formatting difference only). It says nothing about role locators, so the claim's main point, that role locators rest on the tree, is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST

## pg-aria-accessible-name
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only the one-line definition. "Each platform accessibility API provides the accessible name property" is the next sentence and not part of the quote. The spec never says role locators match on the accessible name.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## bp-pw-test-user-visible-behavior
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quoted sentence goes on: "and avoid relying on implementation details such as ... the css class of some element", which covers the claim's "not implementation details" half.

## pg-apple-ui-test-as-person
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: I checked this in the XCUIAutomation overview text, read from Apple's documentation JSON because the HTML page is rendered by JavaScript.

## pg-tl-testid-last
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence continues "or it doesn't make sense (e.g. the text is dynamic)", which covers the claim's dynamic-text case.

## pg-pw-testid-resilient
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same paragraph adds that test ids are not user-facing, and that role or text locators are better when role or text matters.

## ks-cy-data-attributes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is labelled "Best Practice" under the "Selecting Elements" heading.

## pg-apple-accessibility-identifier
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote only says an identifier "can be used to uniquely identify an element" in UI Automation scripts. The contrast with the label is a separate next sentence ("avoid inappropriately setting or accessing an element's accessibility label"). The page is UIKit's, not all Apple platforms.
- correction: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST

## pg-android-compose-semantics
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says finders select nodes in the semantics tree. It does not mention finding by text, content description or test tag.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## pg-ms-automationid
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page is about using AutomationIdProperty to locate elements in the UI Automation tree. It is .NET Framework UI Automation documentation.

## pg-ms-automationid-scope
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source follows with the example of duplicate "Item1" ids under different top-level menus.

## pg-pw-css-xpath-not-recommended
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It appears in the "When to use this" note for CSS and XPath locators.

## ks-cy-brittle-selectors
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source labels the quoted text "Anti-Pattern:" under "Selecting Elements".

## ev-fowler-po-brittle
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is in the opening paragraph of Fowler's PageObject entry.

## ev-kcd-queryselector
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence goes on to say such tests are harder to read and break more often.

## ks-se-locator-preference
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote makes well-written CSS "the preferred method" when unique IDs are missing, which ranks it above XPath. The next sentence calls XPath complicated and slow.

## bp-pw-wait-for-timeout-flaky
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "In production" here means real test runs as opposed to debugging. The page says waitForTimeout "should only be used for debugging".

## bp-pw-web-first-assertions
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote only says web-first assertions wait until the expected condition is met. Nothing on the best-practices page says they replace manual waits; its "👎" contrast is a non-waiting `expect(await ...isVisible())` assertion, not a sleep.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## bp-cy-no-arbitrary-wait
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only the anti-pattern text. The half about guarding waits with "an explicit condition" comes from the separate "Best Practice" line beside it, which is not quoted.
- correction: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST

## ks-wdio-no-pause
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers "not resilient, flaky". "Wait for a condition instead" appears only in a code example (`waitForEnabled()`), not in the quoted text.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## ks-wdio-auto-retry-assertions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The ban on assertions that do not wait directly implies using ones that do. The next paragraph says the built-in assertions retry until they pass or time out.

## ks-se-sleep-fails
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is on Selenium's waits page; it uses a curly apostrophe, a formatting difference only.

## ks-se-no-mix-waits
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is a "Warning:" with the example that a 10s implicit wait plus a 15s explicit wait can time out at 20s.

## pg-android-avoid-sleep
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is a "Warning" on Android's big-test stability page.

## pg-android-wait-until
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page offers this as the "Solutions" approach for big tests, followed by Compose waitUntil APIs.

## pg-android-idling-resources
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source uses "must", and goes on to list Thread.sleep() as a bad workaround.

## pg-android-espresso-sync
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is on the Espresso overview page.

## pg-apple-wait-for-existence
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only the API abstract ("Waits the specified amount of time for an element to exist"). Neither it nor anything else on the page says to use it rather than sleeping.
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## ev-fowler-no-bare-sleeps
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source has the same "asynchonous" typo.

## ev-kcd-find-for-async
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source writes it as "find*" in code formatting; that is a formatting difference only.

## bp-pw-tests-fully-isolated
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence continues "with its own local storage, session storage, data, cookies etc."

## bp-cy-tests-independent
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is the best practice for the anti-pattern "Having tests rely on the state of previous tests".

## bp-cy-clean-state-before
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The section heading and its paired anti-pattern ("Using after or afterEach hooks to clean up state") give the "rather than after" contrast.

## bp-pw-control-database-data
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is under "Testing with a database".

## ks-pw-browser-context-isolation
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote defines test isolation (each test has its own storage and cookies). "Through a fresh browser context" is a separate next sentence ("Playwright achieves this using BrowserContexts"), not the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## ks-pw-fixtures-isolated
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the "environment each test needs" half. "Test fixtures are isolated between tests" is the next sentence and is not quoted.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## ks-pw-parallel-default
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source states only the parallel-by-default fact. It does not say this makes isolation a precondition; it adds that tests in one file run in order in the same worker.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## ks-se-no-shared-data
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is on Selenium's "Avoid Sharing State" page.

## ks-se-new-driver-per-test
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is on the same page.

## pg-android-uiautomator-clear-data
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is a code comment on `clearAppData("com.example.targetapp")` in UI Automator's app-control API, and it supports the capability claim.

## ev-fowler-isolated
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Fowler adds that he prefers rebuilding starting state from scratch over cleaning up afterwards.

## bp-cy-programmatic-login
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Its paired anti-pattern is "using your UI to log in", which gives the "instead of through the UI" contrast.

## ks-se-api-login
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The next sentence suggests "using an API to login and set a cookie".

## bp-pw-clock-control
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote only says simulating time-dependent behaviour is essential. Controlling the clock instead of real time is the next sentence ("manipulate and control time within tests ... without the delays and variability of real-time execution"), not the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## ev-fowler-wrap-clock
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is in the time section of the non-determinism article.

## ks-pw-retries-flaky
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Playwright lists "passed", "flaky" and "failed" as separate categories, so a test that passes on retry is reported as flaky, not passed.

## pg-android-retries-fix
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is a "Key point" on the stability page.

## ev-fowler-nondeterminism-useless
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is in "Why Non-deterministic Tests are a Problem".

## ks-cy-stub-majority
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The same "Suggested Use" list for stubbing says "Use for the vast majority of tests".

## ks-cy-real-server-critical-paths
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says real-server tests are "Great for" critical paths, not that they are kept only for them. "Use sparingly" is a separate bullet, not the quote. The list also says "Helpful to have one test around the happy path of a feature".
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## ks-cy-stub-drift
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source lists the drift risk as a downside of stubbing. The conclusion that some live coverage therefore remains is the researcher's inference, not the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## bp-pw-use-network-api
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Instead" refers to testing against "third party servers that you do not control" in the "Avoid testing third-party dependencies" section.

## bp-pw-stable-staging
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is under "Testing with a database".

## ev-vocke-e2e-flaky
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is in the end-to-end section of The Practical Test Pyramid.

## ks-pw-tags-grep
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers tagging and filtering by tag in the test report. Choosing which tests run by tag is the next sentence ("only run tests that have a certain tag"), not the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## ks-pw-projects-filter
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports projects with filters running a subset of tests. Running "live and hermetic specs separately" is an application of that and is not in the source; its example is a "smoke" project.
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## ks-pw-projects-environments
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is in "Configure projects for multiple environments". The full sentence covers staging with 2 retries and production with 0, set per project.

## ks-pw-env-staging-switch
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Now" refers to the config just before it, where `process.env.STAGING === '1'` picks the baseURL, so the switch is an environment variable.

## ks-gha-secrets-forks
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source covers GitHub Actions only, and exempts GITHUB_TOKEN ("With the exception of GITHUB_TOKEN"). The claim widens it to all "CI secrets" and leaves out the exception.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## bp-pw-env-secrets
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source uses `process.env.USERNAME` and `process.env.PASSWORD` as its example. Its wording is "usually a good idea", a SHOULD rather than a MUST.

## bp-asvs-no-secrets-in-repo
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is ASVS 4.0.3 requirement 2.10.4, which names passwords, integration secrets, seeds and API keys. It sits in the service-authentication section.

## ks-cy-env-gitignore
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is a "Caution" box on the Cypress environment-variables page.

## ks-cy-env-values-exposed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence is about values passed through `Cypress.expose()` into the browser context, which matches the claim's "values handed to the browser".

## ks-cy-session-no-passwords-in-id
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The advice covers only the cy.session id, because Cypress shows that id in the Command Log. The claim widens it to "anything written to the test log".
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## ks-gha-dont-print
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The warning sits under the gpg large-secrets workaround, where GitHub does not redact printed secrets. That is narrower than general logging, but it fits the claim.

## ks-pw-auth-gitignore
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is under "Core concepts" on Playwright's auth page.

## ks-pw-auth-state-sensitive
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source follows with "We strongly discourage checking them into private or public repositories."

## bp-owasp-standard-test-secrets
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is under "8.1 General detection approaches". Standard test secrets are meant to cut secret-scanner false positives, not to tell tests to use fake secrets instead of real ones.
- correction: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST

## bp-owasp-separate-prod-dev
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: OWASP says only "Consider" separate secret-management solutions, a weaker strength than the claim. It names production and development secrets, not test secrets.
- correction: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

## ks-pw-account-per-worker
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote states only that one account per worker is needed. The "tests that change server-side state" condition is in separate sentences of the section ("This is the recommended approach for tests that modify server-side state").
- correction: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST

## bp-pw-trace-viewer-on-ci
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is under "Debugging on CI".

## ks-se-po-no-assertions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Selenium makes one exception: a page object may check that its page loaded.

## ev-fowler-po-no-assertions
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Fowler gives a personal preference ("I favor"), sets out the opposing view, and says in footnote 3 that assertions checking a page's invariants are fine. The absolute "carry no assertions" goes further than that.
- correction: refuted (quote-found yes, supports-claim partly); trust 58 -> 38; a rule citing it cannot carry MUST

## ev-vocke-no-retest-lower-level
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source sentence ends "in the higher-level test again".

## ev-vocke-focus-uncovered
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is the sentence right after the previous claim's.
