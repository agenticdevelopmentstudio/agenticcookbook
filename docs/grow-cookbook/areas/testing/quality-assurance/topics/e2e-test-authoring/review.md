# Review: e2e-test-authoring

## Findings

- `writing-a-spec.md`, "How the tools compare" (text changed this round): two bullets now say more than the claims behind them. (1) The **Selenium** bullet says "Its own locator order (unique IDs, then CSS, then XPath) is for structural locators." ks-se-locator-preference says only that "If unique IDs are unavailable, a well-written CSS selector is the preferred method of locating an element". Selenium gives that order for locating elements in general and never limits it to structural locators. Limiting it to the structural fallback is this guideline's choice, which the Rationale states correctly ("kept for the structural locator a spec falls back to"). (2) The **Windows UI Automation** bullet says an AutomationId "needs container and scope information to be useful". pg-ms-automationid-scope's quote says it "typically needs" that information, and the Rationale quotes it with "typically". The bullet drops the hedge. Fix: in (1), say that Selenium ranks unique IDs, then a well-written CSS selector, above XPath, and that this guideline applies that order to the structural locator a spec falls back to. In (2), restore "typically".

## Checked

- The guideline folder matches draft.md: all 47 rules in `rules.md` are identical to the draft's rules.
- Every rule ends with its citation. Every cited claim exists in research.json, and each one is named by some verdict. Every verdict's rule name has a rule of that name. Every rule appears in both `a-build-must-establish.md` and `a-complete-review-must-establish.md`. I checked these with a script.
- `cookr roles check` passes: 47 rules, no findings, and all four skills compile.
- `summary` is 155 characters and describes the new text. `platforms` is now `web`, `ios`, `macos`, `android` and `windows`. Keeping `macos` is right because the XCUIAutomation claims (pg-apple-ui-test-as-person, pg-apple-wait-for-existence) are not UIKit-only. `related` adds properties-of-good-tests and flaky-test-prevention, and the intro's scope list names both.
- No "dedicated test accounts", "sparingly", SwiftUI, Compose "test tag", "secrets are withheld", "puts role ... first", "WAI-ARIA defines" or "none of the locator rules is a MUST" is left anywhere in the guideline.
- The new rules follow from their claims at their stated strength:
  - `e2e-compose-finders-over-semantics-tree` (MAY): pg-android-compose-semantics, finders over the semantics tree.
  - `e2e-secrets-out-of-ci-logs` (SHOULD): ks-gha-dont-print, "Be careful".
  - `e2e-no-secrets-in-session-id` (SHOULD): ks-cy-session-no-passwords-in-id, limited to `cy.session` ids as the second check requires.
  - `e2e-standard-test-secrets` (MAY): bp-owasp-standard-test-secrets' quote, word for word, at community-guidance strength.
  - `e2e-separate-production-secrets` (MAY): now "development secrets", which is what bp-owasp-separate-prod-dev's "Consider" quote says.
- Changed rule `e2e-isolate-test-state` drops "so that tests can run in parallel". The Rationale now takes parallelism from ks-se-new-driver-per-test ("makes parallelization simpler") and ks-pw-parallel-default.
- Each claim the Rationale now calls "refuted in part" is recorded as refuted in its `trust.basis`:
  - the waiting rule: bp-pw-web-first-assertions, bp-cy-no-arbitrary-wait, ks-wdio-no-pause, pg-apple-wait-for-existence;
  - the clock rule: bp-pw-clock-control;
  - isolation: ks-pw-browser-context-isolation, ks-pw-fixtures-isolated;
  - the hermetic rule: ks-cy-real-server-critical-paths, ks-cy-stub-drift;
  - accounts: ks-pw-account-per-worker;
  - page objects: ev-fowler-po-no-assertions;
  - Compose: pg-android-compose-semantics;
  - test ids: pg-apple-accessibility-identifier.
- The Rationale's quoted source wording matches the claim quotes: "should verify", "not recommended", "the preferred method" and "typically needs container and scope information to be useful".
- The Rationale's Cypress paragraph matches ks-cy-stub-majority ("typically have one true end-to-end test"), ks-cy-real-server-critical-paths ("Great for the critical paths"; the happy-path point comes from the second check's note) and ks-cy-stub-drift. Drift is now given as a downside, not as Cypress's reason.
- The `rationale-names-what-makes-assertion-correct` prior text and its lead-in still match owner-list.md word for word. The Rationale still leaves the test-id-order question open as the owner's, and its own rules no longer settle it.

## Rulings

- R1.1: fixed. The rule is named `e2e-test-id-only-when-no-user-facing-locator` in `rules.md`, `a-build-must-establish.md` and `a-complete-review-must-establish.md`, and no verdict name is left without a rule.
- R1.2: fixed. `e2e-locators-user-facing-first` now prefers a user-facing attribute or an explicit contract such as a test id to DOM-structure locators, citing pg-pw-testid-resilient and pg-pw-css-xpath-not-recommended. The test-id rule is a plain MAY. The build line, the reviewer text ("with no ranking between the two"), step 2 ("left to the owner"), the intro and the example table rank neither above the other. The Rationale keeps the order as the owner's.
- R1.3: fixed. Sub-item (e) is a dispute I accept; the rest are fixed:
  - (a) `e2e-dedicated-test-accounts` now cites ks-pw-account-per-worker and ks-pw-auth-state-sensitive. Standard test secrets are a separate MAY in OWASP's own words, and the Rationale places them among detection approaches. The build line, step 7 and the reviewer text are corrected.
  - (b) The rule, build line, step 6 and Rationale are limited to GitHub Actions, with the `GITHUB_TOKEN` exception.
  - (c) The text says UIKit's `accessibilityIdentifier`, drops the Compose test tag, and gives Compose finders their own rule.
  - (d) The rule, build line, step 5, reviewer text and Rationale say the network is stubbed in the main, with real-server specs that suit the critical paths. Neither "sparingly" nor "only" remains, and drift is given as a downside.
  - (e) disputed-accepted. The exception added is Fowler's page-invariant check, which ev-fowler-po-no-assertions' `trust.basis` records. Selenium's page-loaded exception appears only in a second-check note, and ks-se-po-no-assertions' quote has no exception, so no cited claim covers it.
  - (f) The Rationale and tools comparison say only what ks-wdio-role-selector holds.
  - (g) The role-locator link now comes from pg-pw-getbyrole and pg-tl-byrole-top, and WAI-ARIA is cited only for its definitions.
- R1.4: fixed. The Rationale names the four locator rules that cite no refuted claim and gives their sources' recommending wording as the reason for SHOULD. It names the refuted claims only for `e2e-locators-user-facing-first`, `e2e-test-id-only-when-no-user-facing-locator` and `e2e-compose-finders-over-semantics-tree`.
- R1.5: fixed. `e2e-trace-on-ci-failure` now reads "A suite SHOULD record a trace for each E2E test that fails on CI, to debug the failure from instead of videos and screenshots", and the build line matches it.
- R1.6: fixed. `platforms` is `web`, `ios`, `macos`, `android` and `windows`. `macos` stays because the XCUIAutomation text is not UIKit-only.
- R1.7: fixed. `related` holds e5af9ba5-f484-40c3-9738-470090f5241c and 05d00147-5c49-42d8-bdbd-cf8fd7dc2379. The intro names both topics, and the Rationale says this guideline's research supports SHOULD where those guidelines state MUST. The strength question itself is the orchestrator's to route to properties-of-good-tests and flaky-test-prevention.

## Lint

The `/lint-artifact` result (run with this checkout's cookr; it compiled the folder to the scratchpad):

- Shared checks: FM-01, FM-02, FM-04 to FM-11, FM-11a, FM-12 and FM-13 PASS. FM-11a: all 8 `related` UUIDs and every in-text `cookbook:` link resolve.
- [FAIL] FM-03: Index entry matches folder. `eb82d5d7-4f42-4417-8104-a14f6a27899f` has no entry in `cookbook/index.json`.
- Guideline checks: GF-01, GF-02, GF-03, gf-frontmatter-complete, gf-triggers-field, gf-roled-parts, gf-named-rules (47 rules), gf-build-bar, gf-research-folder and gf-rule-cites-research PASS.
- [WARN] GF-04: no `## Compliance` section. It is optional.
- `cookr validate` lists this artifact in no failure. The `guidelines/INDEX.md` and `index/triggers.yaml` drift follows from the missing index entry.
- Summary: Pass 24, Warn 1, Fail 1. RESULT: NOT CLEAN, 1 failing check.

The author disputes FM-03 in disputes.md: the index entry is written by `cookr update` at integration, and the draft cannot add it. The lint still reports it as a failure, so it is counted below.

lint: fail 1

verdict: fail
