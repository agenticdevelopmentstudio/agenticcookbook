# Research brief: e2e-test-authoring

- **Area:** `testing/quality-assurance`
- **Topic:** `e2e-test-authoring` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/testing/quality-assurance/e2e-test-authoring`
- **Base commit:** `77a898dbc718928bbd96ef617723c83ec69cd549` (`base.txt`)
- **Research type:** Technology / software (intent Do; domain browser end-to-end testing; method tool documentation and practitioner sources).
- **Research bar:** Technology / software, no escalation (owner approval 2026-11-24, Owner question 1).

## The topic

How an end-to-end (E2E) spec is written so it tests what a user does and stays stable: the locators it uses (role, label, text, test id) and those it avoids, how it waits without fixed sleeps and keeps each test's state isolated, when it mocks the network (hermetic) and when it runs against a live or preview environment and how the two are kept apart, how it gets test accounts and secrets without committing them, and how it states the rationale for what it asserts.

The cookbook states general practice for any team that tests a product, not myagenticteams-qa-team's: the adh `e2e/` and `e2e/live/` layout, the `@smoke` tag, the LoginCard selectors and the `page.route` mocks of adh sites, the hub path for exploratory reports and charters, the JSON output contracts (fenced blocks, fingerprints, field names the team's runner parses), the team's step budgets and the site registry stay in the team and are not researched (owner ruling, 2026-11-21). No finding, claim or rule names any of them.

**Not this topic's:**

- That E2E runs at all, and which journeys it covers, is `cookbook/guidelines/testing/the-testing-workflow`'s (`should-verify-end-to-end`, `should-cover-critical-user-journeys-in-e2e`); this topic cites it and does not restate it.
- The tool choice for TypeScript is `cookbook/guidelines/implementing/testing/testing`'s (`should-use-playwright-for-end-to-end-tests`); how many E2E tests a suite holds is `cookbook/guidelines/planning/testing/test-pyramid`'s. Both are cited for scope.
- E2E as the costly alternative to contracts is `cookbook/guidelines/testing/contract-testing`'s; E2E against preview environments is `cookbook/guidelines/shipping/ephemeral-environments`'s. Cited where the hermetic-versus-live question touches them.
- Quarantining a flaky test is `cookbook/guidelines/testing/flaky-test-quarantine`'s; classifying a failed test is the sibling topic `test-failure-triage`'s.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the platforms are the web (Playwright, Cypress, WebdriverIO and Selenium/WebDriver, Testing Library, the W3C WAI-ARIA roles and the accessibility tree locators rest on), Apple (XCUITest / XCTest UI testing) and Android (Espresso, UI Automator, Compose testing). Windows desktop UI automation (WinAppDriver, UI Automation) is in scope only where its owner publishes guidance on stable locators; if none bears on this topic, say so in one line.

## Research questions (from the area plan, verbatim)

1. Best practice: how should a browser end-to-end spec be written so it tests what a user does, stays stable as the UI changes and states the rationale for what it checks?
2. Known solutions: how do Playwright, Cypress, WebdriverIO and Selenium compare on locators, auto-waiting, network mocking, tracing and parallel runs, and what do page objects and fixtures add?
3. Platform guidelines: what do Playwright's best-practices and locator guides, Testing Library's query priority, the WAI-ARIA roles the locators rest on, and Apple's XCUITest and Android's Espresso guides say about writing stable UI tests?
4. The expert's view: what do test engineers say teams get wrong with end-to-end specs (CSS-path selectors, fixed sleeps, shared state between tests, specs that duplicate unit tests), and what to do instead?
5. **E2E selector strategy**: find the locator priority the tool owners and Testing Library publish, and state which locators a spec uses first, when a test id is warranted, and which it never uses.
6. **Hermetic versus live E2E runs**: find how teams split mocked-network specs from specs against a live or preview environment, and state when a spec is hermetic, when it runs live, and how each is tagged and gated.
7. **E2E determinism**: find the tool owners' guidance on waiting, retries, test isolation, clocks and test data, and state the rules that keep a spec free of timing flakes.
8. **E2E secret handling**: find how the tool owners and security guidance provide test accounts and secrets to specs (environment variables, secret stores, stored auth state), and state how a spec gets credentials without committing them.

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`, using its source
  catalogue for the domain. Primary sources (specifications, standards, the tool and platform owners' own
  documentation, the published studies themselves) come before secondary ones (practitioner articles, books);
  use a secondary source only for what no primary source covers, and say so in the claim's trust basis.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`,
  `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in, as a claim to check,
  never as a source. Never restate or summarize a rule.
- `supported` means supported at the rule's stated strength. Every rule below is marked *no RFC keyword*: it
  states its obligation in plain words (a Verify clause reads as a check that must hold; a Worker Focus
  clause as what the worker attends to). Judge each at the strength its words carry, and say in research.md
  what strength (MUST, SHOULD or MAY) the sources support. Judge each as general practice: a word that
  names the team's own setting (a site, a cluster, a pass, a browser) stands for its general counterpart
  (the system under test, a group of failures, a session, the product's UI), and no claim, finding or new
  rule carries the team's word where the general one fits.
- A rule the research cannot support or finds against is recorded as its own `<rule-name>-prior` claim,
  `source_type` `prior cookbook text`, its one citation `title` `e2e-test-authoring (teams/myagenticteams-qa-team/specialities/testing/spec-authoring.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:15f998560f57f3d0604c04af9acee6cc59d0d5a5:teams/myagenticteams-qa-team/specialities/testing/spec-authoring.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/myagenticteams-qa-team/specialities/testing/spec-authoring.md` in the teams repo at commit `15f998560f57f3d0604c04af9acee6cc59d0d5a5` (myagenticteams-qa-team's
compiled speciality; the cookbook base commit is `77a898dbc718928bbd96ef617723c83ec69cd549`), as a claim to check, never as a source. Only the
file's general clauses are quoted; its team-specific clauses (named under *The topic*) are not this topic's
and are not quoted. The rules, one per clause, named here; the names are fixed from here on:

1. **write-deterministic-specs** (no RFC keyword; section *Worker Focus*): "You write or repair deterministic Playwright specs"
2. **rationale-cites-assertion-source** (no RFC keyword; section *Worker Focus*): "a one-paragraph rationale citing the feature docs / plan the assertion derives from"
3. **rationale-names-what-makes-assertion-correct** (no RFC keyword; section *Verify*): "The rationale names the feature doc, plan, or commit the new assertion derives from. A rationale that argues the assertion is sensible, without citing what makes it correct, is a fail."
4. **hermetic-specs-mock-the-api** (no RFC keyword; section *Verify*): "Hermetic specs mock the API through `page.route`."
5. **no-credentials-or-real-user-data** (no RFC keyword; section *Verify*): "The patch contains no credentials, tokens, or real user data — not in fixtures, not in comments, not in mocked responses."
