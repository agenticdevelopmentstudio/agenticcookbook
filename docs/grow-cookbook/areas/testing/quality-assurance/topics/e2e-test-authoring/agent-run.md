# e2e-test-authoring: research agent run (fallback)

team_probe: researchteam not runnable (missing distributions: PyYAML, aiohttp, mcp, websockets); one fresh Opus
agent ran the filled research prompt. Its reply, verbatim:

I wrote both research files, and the validate line prints `Research passed.` Of the five existing rules, four are supported and one (`rationale-names-what-makes-assertion-correct`) is unsupported at the strength it states. Nothing is committed.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/e2e-test-authoring/research/research.md`

**Claims per question** (93 in total)

| Question | Claims |
|---|---|
| best-practices | 21 (includes the prior claim) |
| known-solutions | 36 |
| platform-guidelines | 22 |
| experts-view | 14 |

All of them are `single`, except the prior claim, which is `uncorroborated`. Each claim holds one quote, so where other sources agree, its trust basis names their claim ids.

**Verdicts**
- write-deterministic-specs — supported — bp-pw-wait-for-timeout-flaky, bp-pw-web-first-assertions, bp-pw-tests-fully-isolated, bp-cy-no-arbitrary-wait, ks-pw-auto-wait-actionability, ks-se-sleep-fails, ks-wdio-no-pause, pg-android-avoid-sleep, ev-fowler-nondeterminism-useless, ev-fowler-no-bare-sleeps
- rationale-cites-assertion-source — supported — bp-istqb-traceability, ks-pw-annotations
- rationale-names-what-makes-assertion-correct — unsupported — rationale-names-what-makes-assertion-correct-prior, bp-istqb-traceability
- hermetic-specs-mock-the-api — supported — bp-pw-only-test-what-you-control, bp-pw-use-network-api, ks-pw-mock-api, ks-pw-har-replay, ks-cy-stub-majority, ks-se-eliminate-external-services, pg-android-espresso-intents-hermetic, ev-fowler-test-double-remote
- no-credentials-or-real-user-data — supported — bp-asvs-no-secrets-in-repo, bp-pw-env-secrets, ks-pw-auth-gitignore, ks-pw-auth-state-sensitive, ks-cy-env-gitignore, bp-owasp-standard-test-secrets, bp-ico-synthetic-minimisation, ev-thoughtworks-prod-data, ev-thoughtworks-weak-test-security
- e2e-locators-user-facing-first — new — pg-pw-prioritize-user-facing, pg-pw-getbyrole, pg-tl-guiding-principle, pg-tl-byrole-top, ks-wdio-role-selector, pg-aria-accessibility-tree, pg-aria-accessible-name, bp-pw-test-user-visible-behavior, pg-apple-ui-test-as-person
- e2e-test-id-only-when-no-user-facing-locator — new — pg-tl-testid-last, pg-pw-testid-resilient, ks-cy-data-attributes, pg-apple-accessibility-identifier, pg-android-compose-semantics, pg-ms-automationid, pg-ms-automationid-scope
- e2e-avoid-dom-structure-locators — new — pg-pw-css-xpath-not-recommended, ks-cy-brittle-selectors, ev-fowler-po-brittle, ev-kcd-queryselector, ks-se-locator-preference
- e2e-wait-on-conditions-not-time — new — bp-pw-wait-for-timeout-flaky, bp-pw-web-first-assertions, bp-cy-no-arbitrary-wait, ks-wdio-no-pause, ks-wdio-auto-retry-assertions, ks-se-sleep-fails, ks-se-no-mix-waits, pg-android-avoid-sleep, pg-android-wait-until, pg-android-idling-resources, pg-android-espresso-sync, pg-apple-wait-for-existence, ev-fowler-no-bare-sleeps, ev-kcd-find-for-async
- e2e-isolate-test-state — new — bp-pw-tests-fully-isolated, bp-cy-tests-independent, bp-cy-clean-state-before, bp-pw-control-database-data, ks-pw-browser-context-isolation, ks-pw-fixtures-isolated, ks-pw-parallel-default, ks-se-no-shared-data, ks-se-new-driver-per-test, pg-android-uiautomator-clear-data, ev-fowler-isolated
- e2e-set-up-state-programmatically — new — bp-cy-programmatic-login, ks-se-api-login
- e2e-control-the-clock — new — bp-pw-clock-control, ev-fowler-wrap-clock
- e2e-retries-surface-flakiness — new — ks-pw-retries-flaky, pg-android-retries-fix, ev-fowler-nondeterminism-useless
- e2e-hermetic-by-default-live-for-critical-paths — new — ks-cy-stub-majority, ks-cy-real-server-critical-paths, ks-cy-stub-drift, bp-pw-use-network-api, bp-pw-stable-staging, ev-vocke-e2e-flaky
- e2e-select-live-specs-by-tag-or-project — new — ks-pw-tags-grep, ks-pw-projects-filter, ks-pw-projects-environments, ks-pw-env-staging-switch, ks-gha-secrets-forks
- e2e-credentials-from-environment — new — bp-pw-env-secrets, bp-asvs-no-secrets-in-repo, ks-cy-env-gitignore, ks-cy-env-values-exposed, ks-cy-session-no-passwords-in-id, ks-gha-dont-print
- e2e-stored-auth-state-git-ignored — new — ks-pw-auth-gitignore, ks-pw-auth-state-sensitive
- e2e-dedicated-test-accounts — new — bp-owasp-standard-test-secrets, bp-owasp-separate-prod-dev, ks-pw-account-per-worker
- e2e-trace-on-ci-failure — new — bp-pw-trace-viewer-on-ci
- e2e-page-objects-hold-no-assertions — new — ks-se-po-no-assertions, ev-fowler-po-no-assertions, ks-pw-fixtures-isolated
- e2e-do-not-repeat-lower-level-assertions — new — ev-vocke-no-retest-lower-level, ev-vocke-focus-uncovered

Each of the four bold research questions has at least one `new` verdict: selector strategy (the locator rules), hermetic vs live (the hermetic-by-default and live-selection rules), determinism (waiting, isolation and the clock), and secret handling (credentials, auth state and test accounts).

**Strength notes** (also stated in research.md)
- `rationale-names-what-makes-assertion-correct` says "is a fail", which makes it a MUST. The only support is ISTQB's traceability text, which is SHOULD strength.
- In `no-credentials-or-real-user-data`, the credentials half reaches MUST through OWASP ASVS 2.10.4. The real-user-data half rests on the data-minimisation principle and a Thoughtworks Hold, so it supports SHOULD only.
- Fixed sleeps reach MUST NOT. Playwright's API reference says "Never wait for timeout".

One quote came out before I wrote the final file. A Kent C. Dodds quote on role queries was not among the quotes I had fetched, so I replaced it with his fetched quote on `find*` queries (now `ev-kcd-find-for-async`). The open questions and limitations are recorded in research.json.
