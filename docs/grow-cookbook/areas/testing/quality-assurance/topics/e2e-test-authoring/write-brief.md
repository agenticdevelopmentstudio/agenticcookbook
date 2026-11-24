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
