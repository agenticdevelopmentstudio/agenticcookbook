# Write brief: e2e-test-authoring

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/e2e-test-authoring/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- write-deterministic-specs: supported (claims: bp-pw-wait-for-timeout-flaky, bp-pw-web-first-assertions, bp-pw-tests-fully-isolated, bp-cy-no-arbitrary-wait, ks-pw-auto-wait-actionability, ks-se-sleep-fails, ks-wdio-no-pause, pg-android-avoid-sleep, ev-fowler-nondeterminism-useless, ev-fowler-no-bare-sleeps)
- rationale-cites-assertion-source: supported (claims: bp-istqb-traceability, ks-pw-annotations)
- rationale-names-what-makes-assertion-correct: unsupported (claims: rationale-names-what-makes-assertion-correct-prior, bp-istqb-traceability)
- hermetic-specs-mock-the-api: supported (claims: bp-pw-only-test-what-you-control, bp-pw-use-network-api, ks-pw-mock-api, ks-pw-har-replay, ks-cy-stub-majority, ks-se-eliminate-external-services, pg-android-espresso-intents-hermetic, ev-fowler-test-double-remote)
- no-credentials-or-real-user-data: supported (claims: bp-asvs-no-secrets-in-repo, bp-pw-env-secrets, ks-pw-auth-gitignore, ks-pw-auth-state-sensitive, ks-cy-env-gitignore, bp-owasp-standard-test-secrets, bp-ico-synthetic-minimisation, ev-thoughtworks-prod-data, ev-thoughtworks-weak-test-security)
- e2e-locators-user-facing-first: new (claims: pg-pw-prioritize-user-facing, pg-pw-getbyrole, pg-tl-guiding-principle, pg-tl-byrole-top, ks-wdio-role-selector, pg-aria-accessibility-tree, pg-aria-accessible-name, bp-pw-test-user-visible-behavior, pg-apple-ui-test-as-person)
- e2e-test-id-only-when-no-user-facing-locator: new (claims: pg-tl-testid-last, pg-pw-testid-resilient, ks-cy-data-attributes, pg-apple-accessibility-identifier, pg-android-compose-semantics, pg-ms-automationid, pg-ms-automationid-scope)
- e2e-avoid-dom-structure-locators: new (claims: pg-pw-css-xpath-not-recommended, ks-cy-brittle-selectors, ev-fowler-po-brittle, ev-kcd-queryselector, ks-se-locator-preference)
- e2e-wait-on-conditions-not-time: new (claims: bp-pw-wait-for-timeout-flaky, bp-pw-web-first-assertions, bp-cy-no-arbitrary-wait, ks-wdio-no-pause, ks-wdio-auto-retry-assertions, ks-se-sleep-fails, ks-se-no-mix-waits, pg-android-avoid-sleep, pg-android-wait-until, pg-android-idling-resources, pg-android-espresso-sync, pg-apple-wait-for-existence, ev-fowler-no-bare-sleeps, ev-kcd-find-for-async)
- e2e-isolate-test-state: new (claims: bp-pw-tests-fully-isolated, bp-cy-tests-independent, bp-cy-clean-state-before, bp-pw-control-database-data, ks-pw-browser-context-isolation, ks-pw-fixtures-isolated, ks-pw-parallel-default, ks-se-no-shared-data, ks-se-new-driver-per-test, pg-android-uiautomator-clear-data, ev-fowler-isolated)
- e2e-set-up-state-programmatically: new (claims: bp-cy-programmatic-login, ks-se-api-login)
- e2e-control-the-clock: new (claims: bp-pw-clock-control, ev-fowler-wrap-clock)
- e2e-retries-surface-flakiness: new (claims: ks-pw-retries-flaky, pg-android-retries-fix, ev-fowler-nondeterminism-useless)
- e2e-hermetic-by-default-live-for-critical-paths: new (claims: ks-cy-stub-majority, ks-cy-real-server-critical-paths, ks-cy-stub-drift, bp-pw-use-network-api, bp-pw-stable-staging, ev-vocke-e2e-flaky)
- e2e-select-live-specs-by-tag-or-project: new (claims: ks-pw-tags-grep, ks-pw-projects-filter, ks-pw-projects-environments, ks-pw-env-staging-switch, ks-gha-secrets-forks)
- e2e-credentials-from-environment: new (claims: bp-pw-env-secrets, bp-asvs-no-secrets-in-repo, ks-cy-env-gitignore, ks-cy-env-values-exposed, ks-cy-session-no-passwords-in-id, ks-gha-dont-print)
- e2e-stored-auth-state-git-ignored: new (claims: ks-pw-auth-gitignore, ks-pw-auth-state-sensitive)
- e2e-dedicated-test-accounts: new (claims: bp-owasp-standard-test-secrets, bp-owasp-separate-prod-dev, ks-pw-account-per-worker)
- e2e-trace-on-ci-failure: new (claims: bp-pw-trace-viewer-on-ci)
- e2e-page-objects-hold-no-assertions: new (claims: ks-se-po-no-assertions, ev-fowler-po-no-assertions, ks-pw-fixtures-isolated)
- e2e-do-not-repeat-lower-level-assertions: new (claims: ev-vocke-no-retest-lower-level, ev-vocke-focus-uncovered)

Second-check corrections, refuted (criteria 3 applies to these claims):
- ks-wdio-role-selector: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- pg-aria-accessibility-tree: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- pg-aria-accessible-name: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- pg-apple-accessibility-identifier: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- pg-android-compose-semantics: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- bp-pw-web-first-assertions: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- bp-cy-no-arbitrary-wait: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- ks-wdio-no-pause: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- pg-apple-wait-for-existence: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- ks-pw-browser-context-isolation: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- ks-pw-fixtures-isolated: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- ks-pw-parallel-default: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- bp-pw-clock-control: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- ks-cy-real-server-critical-paths: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- ks-cy-stub-drift: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- ks-pw-tags-grep: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- ks-pw-projects-filter: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- ks-gha-secrets-forks: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- ks-cy-session-no-passwords-in-id: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- bp-owasp-standard-test-secrets: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- bp-owasp-separate-prod-dev: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST
- ks-pw-account-per-worker: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- ev-fowler-po-no-assertions: refuted (quote-found yes, supports-claim partly); trust 58 -> 38; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **rationale-names-what-makes-assertion-correct** — verdict `unsupported` (claims: rationale-names-what-makes-assertion-correct-prior, bp-istqb-traceability). Prior text, kept word for word: "The rationale names the feature doc, plan, or commit the new assertion derives from. A rationale that argues the assertion is sensible, without citing what makes it correct, is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Test cases are traced to the test-basis elements (requirements, plans) they derive from.

## Open questions

- Whether a rationale that does not cite its feature doc, plan or commit is a fail (MUST, as rationale-names-what-makes-assertion-correct states) or a SHOULD, which is what the ISTQB traceability text supports.
- Whether a test id may be a first-choice locator: Playwright calls test ids the most resilient way of testing, while Testing Library recommends them only when no role or text match fits; the owner decides which order the cookbook adopts.
- Whether hermetic is the default for every spec, and how many live or preview specs a suite keeps (Cypress suggests one true end-to-end test per feature with the rest stubbed); the count itself belongs to the test-pyramid topic.
- How live specs are selected and gated: by tag and grep, by a separate project or directory, or by an environment variable; the sources show all three and prefer none.
- Whether CI retries are allowed for E2E specs and how many; Playwright and Android both offer retries and both say a test that passes on retry is flaky and must be fixed.
- Whether the rule against real user data in a patch is kept at MUST strength: its credentials half rests on OWASP ASVS, its personal-data half on the data-minimisation principle and a Thoughtworks Hold rather than a test-specific requirement.
- Whether page objects are recommended, allowed or left to the team, given that Cypress lists sharing page objects as an anti-pattern while Selenium and Playwright's fixture guide build on them.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md`, `a-build-must-establish.md`, `a-complete-review-must-establish.md`: the rule `e2e-test-id-where-no-user-facing-locator` renames the verdict's rule `e2e-test-id-only-when-no-user-facing-locator`. Criterion 4 fixes the names the verdicts key on; it is the only verdict name that has no rule of that name (checked for all 21 verdicts). Fix: name the rule `e2e-test-id-only-when-no-user-facing-locator` in all three files.
- R1.2: Open question settled (owner-list.md: "Whether a test id may be a first-choice locator ... the owner decides which order the cookbook adopts"). The text adopts Testing Library's order in every place it talks about locator order: `rules.md` `e2e-locators-user-facing-first` ("first by user-facing attributes"); `rules.md` `e2e-test-id-where-no-user-facing-locator` ("Where no role or text match fits, a spec MAY"); `a-build-must-establish.md` line for that rule ("each test id locates an element no role or text match fits"); `what-a-reviewer-looks-for.md` ("with a test id only where nothing user-facing fits"); `writing-a-spec.md` step 2 ("Where nothing user-facing fits, add a test id"). The rationale then says the question is left open, which the rules contradict. `e2e-locators-user-facing-first` also drops part of the claim it cites: pg-pw-prioritize-user-facing recommends "user-facing attributes and explicit contracts", and Playwright's explicit contracts include test ids. Fix: say that user-facing locators and test ids are both preferred over structural locators, without ranking one above the other, in the rule, its build line, the reviewer text and step 2. Make the test-id rule a plain MAY with no "where nothing fits" condition. Keep the rationale's statement that the order is the owner's.
- R1.3: Rules and prose repeat what the second check refuted (second-check.md notes), so the text does not follow from the claims it cites. Every instance:
    (a) `e2e-dedicated-test-accounts` rests only on bp-owasp-standard-test-secrets. The second check says standard test secrets are there to cut secret-scanner false positives, "not to tell tests to use fake secrets instead of real ones", and the quote does not mention dedicated test accounts. The rule says what was refuted, and so do its build line, `writing-a-spec.md` step 7 ("Use dedicated test accounts"), `what-a-reviewer-looks-for.md` ("accounts are dedicated test accounts") and `rationale.md` ("OWASP's advice on standard test secrets is community guidance"). Fix: base the test-account half on claims that state it (ks-pw-account-per-worker's "multiple testing accounts", ks-pw-auth-state-sensitive's "your test account"). Reword the standard-test-secrets half to say what OWASP says, or drop it. Correct the rationale.
    (b) `e2e-gate-live-specs-needing-secrets` says "CI secrets" and that "the secrets are withheld". The second check says ks-gha-secrets-forks covers GitHub Actions only and leaves GITHUB_TOKEN out of the withholding. Fix: limit the rule to GitHub Actions and note the GITHUB_TOKEN exception. Add the exception to the matching rationale sentence.
    (c) `e2e-test-id-where-no-user-facing-locator` names "an `accessibilityIdentifier` on Apple platforms", but the second check says the page is UIKit's, not all Apple platforms. It names "a test tag in Compose", but pg-android-compose-semantics' quote does not mention test tags. The same wording is in `writing-a-spec.md` step 2 ("`accessibilityIdentifier` in UIKit or SwiftUI, a test tag in Compose"). Fix: write UIKit's `accessibilityIdentifier`, and drop the Compose test tag or describe it as finding a node in the semantics tree.
    (d) `e2e-hermetic-by-default-live-for-critical-paths` says real-server specs are "used sparingly, for the critical paths". The second check says the Cypress quote calls them "Great for" critical paths, not kept only for them; that "Use sparingly" is not in the quote; and that the source also recommends a test around each feature's happy path. "Most" and "sparingly" are also unanchored relative terms (behavioral-requirements `should-not-use-unanchored-relative-terms`). The same restriction is in the build line ("live specs cover critical paths"), `writing-a-spec.md` step 5 ("Keep a few specs against the real server for the critical paths") and `rationale.md` ("keeps real-server tests for the critical paths"). `rationale.md` also has "stubbed responses carry no guarantee ... so it keeps one true end-to-end test"; that "so" is the inference the second check refuted for ks-cy-stub-drift. Fix: say that specs stub the network in the main and that real-server specs suit the critical paths, with no "sparingly" or "only" (the count belongs to test-pyramid and the owner). Give drift as a downside Cypress lists, not as its reason.
    (e) `e2e-page-objects-hold-no-assertions` and its build line ("no page object makes a verification or assertion") are absolute. The second check records Selenium's exception (a page object may check that its page loaded) and Fowler's footnote (assertions on a page's invariants are fine). Fix: add that exception to the rule, the build line and the reviewer text.
    (f) `rationale.md` ("Testing Library's query priority and WebdriverIO's selector guide, which put role and accessible name first") and `writing-a-spec.md` ("WebdriverIO puts role plus accessible name first among its selectors"). The second check says the WebdriverIO page makes no such recommendation and rates `button=Submit` "Always / Best" and `aria/` only "Good". Fix: say only what ks-wdio-role-selector holds, that role plus name keeps matching through class, test-id and DOM changes.
    (g) `rationale.md`: "role locators rest on the accessibility tree and the accessible name WAI-ARIA defines". The second check says WAI-ARIA says nothing about role locators and never says they match on the accessible name. Fix: take the role-locator link from Playwright's `getByRole` (pg-pw-getbyrole) and Testing Library (pg-tl-byrole-top), and cite WAI-ARIA only for the definitions.
- R1.4: `rationale.md`, locator paragraph: "Several of the claims these rules cite were refuted in part by the second check, so none of the locator rules is a MUST." This is wrong for `e2e-test-what-the-user-sees`, `e2e-scope-automation-id-by-container`, `e2e-avoid-dom-structure-locators` and `e2e-prefer-unique-id-to-css-to-xpath`, none of which cites a refuted claim. Their SHOULD comes from the sources' recommending wording ("should", "recommend", "not recommended", "preferred"). The SHOULD rationale is therefore inaccurate (behavioral-requirements `must-explain-rationale-for-should-requirements`). Fix: give the actual reason for each SHOULD, and name the refuted claims only for the rules that cite them (`e2e-locators-user-facing-first`, `e2e-test-id-where-no-user-facing-locator`).
- R1.5: `rules.md` `e2e-trace-on-ci-failure`: "A failing E2E test on CI SHOULD be debugged from a recorded trace" governs how a person debugs, which no change or build can show (behavioral-requirements `must-be-independently-testable`, `must-describe-observable-behavior`). Its build line checks something else ("leaves a trace to debug from"). Fix: write the rule as the observable outcome the build line checks, for example "A suite SHOULD record a trace for each E2E test that fails on CI, to debug from instead of videos and screenshots", and keep the build line in step with it.
- R1.6: `artifact.json` `platforms` is `[]`, but the guideline's intro scopes it to the web, Apple platforms, Android and Windows, and its rules name Espresso, UIKit and Windows UI Automation. Criterion 6 asks for platforms that match the text, and template-conformance `must-make-platforms-a-sequence` asks for one or more canonical identifiers. Fix: set `platforms` to the cookbook's canonical names for the platforms covered, `web`, `ios`, `macos`, `android` and `windows` (drop `macos` if the Apple text stays UIKit-only).
- R1.7: Strength conflict with accepted guidelines (cookbook-compliance `must-be-at-least-as-strict-as-guideline-musts`), and the guidelines are not linked. `testing/properties-of-good-tests` has `must-be-isolated` and `must-be-deterministic`, and `testing/flaky-test-prevention` has `must-not-share-mutable-state`, `must-not-depend-on-execution-order` and `must-not-ignore-flaky-tests`, all MUST or MUST NOT. This guideline states the same things at SHOULD: `write-deterministic-specs`, `e2e-isolate-test-state`, `e2e-no-shared-test-data` and `e2e-fix-flaky-tests`. Neither guideline is in `related` or the intro's scope list. Fix for this topic: add `e5af9ba5-f484-40c3-9738-470090f5241c` (properties-of-good-tests) and `05d00147-5c49-42d8-bdbd-cf8fd7dc2379` (flaky-test-prevention) to `related`, and say in the Rationale that this guideline's research supports SHOULD where those guidelines state MUST. The orchestrator routes the strength question to properties-of-good-tests and flaky-test-prevention.

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
/lint-artifact result: guideline, checked against `tbd/compliance/artifact-formatting/guideline-formatting.md` on the compiled doc in the scratchpad. Pass 20, Warn 2, Fail 1.

- [FAIL] FM-03, index entry matches folder: `cookbook/index.json` has no entry for this id or path. Run `cookr update` to add it. Index drift is also reported for `guidelines/INDEX.md` and `index/triggers.yaml`.
- [WARN] GF-04: no Compliance section (optional; no other compliance check references this guideline).
- [WARN] research, owner-decides: `rationale-names-what-makes-assertion-correct` cites `rationale-names-what-makes-assertion-correct-prior`, which the research rules unsupported (the owner-list rule).
- PASS: FM-01, FM-02, FM-04 to FM-13 (including FM-11a, where all six related UUIDs resolve), GF-01 to GF-03, gf-triggers-field, gf-roled-parts, gf-named-rules, build-bar (44 lines matching 44 rules), gf-research-folder (93 claims, 21 verdicts), gf-rule-cites-research.
- The other `cookr validate` failures are outside this artifact: `frontmatter-present` in the `research/research.md` of exploratory-testing-charters, test-failure-triage and test-impact-analysis.

lint: fail 1
````

## Round 2 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R2.1: `writing-a-spec.md`, "How the tools compare" (text changed this round): two bullets now say more than the claims behind them. (1) The **Selenium** bullet says "Its own locator order (unique IDs, then CSS, then XPath) is for structural locators." ks-se-locator-preference says only that "If unique IDs are unavailable, a well-written CSS selector is the preferred method of locating an element". Selenium gives that order for locating elements in general and never limits it to structural locators. Limiting it to the structural fallback is this guideline's choice, which the Rationale states correctly ("kept for the structural locator a spec falls back to"). (2) The **Windows UI Automation** bullet says an AutomationId "needs container and scope information to be useful". pg-ms-automationid-scope's quote says it "typically needs" that information, and the Rationale quotes it with "typically". The bullet drops the hedge. Fix: in (1), say that Selenium ranks unique IDs, then a well-written CSS selector, above XPath, and that this guideline applies that order to the structural locator a spec falls back to. In (2), restore "typically".

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
The `/lint-artifact` result (run with this checkout's cookr; it compiled the folder to the scratchpad):

- Shared checks: FM-01, FM-02, FM-04 to FM-11, FM-11a, FM-12 and FM-13 PASS. FM-11a: all 8 `related` UUIDs and every in-text `cookbook:` link resolve.
- [FAIL] FM-03: Index entry matches folder. `eb82d5d7-4f42-4417-8104-a14f6a27899f` has no entry in `cookbook/index.json`.
- Guideline checks: GF-01, GF-02, GF-03, gf-frontmatter-complete, gf-triggers-field, gf-roled-parts, gf-named-rules (47 rules), gf-build-bar, gf-research-folder and gf-rule-cites-research PASS.
- [WARN] GF-04: no `## Compliance` section. It is optional.
- `cookr validate` lists this artifact in no failure. The `guidelines/INDEX.md` and `index/triggers.yaml` drift follows from the missing index entry.
- Summary: Pass 24, Warn 1, Fail 1. RESULT: NOT CLEAN, 1 failing check.

The author disputes FM-03 in disputes.md: the index entry is written by `cookr update` at integration, and the draft cannot add it. The lint still reports it as a failure, so it is counted below.

lint: fail 1
````

Disputes so far (disputes.md):

- R1.3(e): the exception added to `e2e-page-objects-hold-no-assertions`, its build line and the reviewer text is Fowler's (checks of a page's own invariants), which ev-fowler-po-no-assertions' record states; Selenium's "a page object may check that its page loaded" is only a note in second-check.md and in no claim of research.json (ks-se-po-no-assertions' quote is "Page objects themselves should never make verifications or assertions"), so adding it would put words in the rule no cited claim covers.
- R1.lint FM-03: the missing `cookbook/index.json` entry (and the `guidelines/INDEX.md` and `index/triggers.yaml` drift) is index state that `cookr update` writes at integration; the author may edit only draft.md (write brief: "Edit only the draft"), and no change to the draft can add an index entry. `cookr validate` on a scratch copy with this draft folded in reports no issue in this artifact beyond that drift and the expected owner-decides warning.

## Round 3 findings

Verdict: pass. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

none
