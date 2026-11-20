# Devteam text move, batch 3

All 18 topics are done and committed one each. `roles gaps` reports 0 lacking for every file. `roles check` and
`roles lossless` exit 0, and `approve.py` printed `RESULT: APPROVED` for each.

**Base note.** `roles lossless --base 0005775` fails for topics that moved folders since that commit (for example
`data/backup-and-recovery`, formerly `shipping/backup-and-recovery`: "is not in 0005775"). For all 18 topics I ran
lossless with the base recorded in each topic's own `lossless.json`. All passed.

**Not placed:** none, for any topic.
**Contradictions (R4):** none found, for any topic.

Topics with one placed sentence and no new rule, except as noted below, took their sentence verbatim under the named rule it concerns.

## data/backup-and-recovery, data/naming-conventions, data/sync-protocol
- Each placed 1 sentence, 0 new rules: "A review passes when it establishes every item above." Placed in `a-complete-review-must-establish.md` under `should-have-tested-recovery-path`, `should-prefix-named-objects-by-type` and `must-be-correct-under-network-failure` respectively. No rule concerns it.
- reader-specific (process): "A review passes when it establishes every item above."

## networking/error-responses (4 sentences, 1 new rule)
- new rule: `must-not-show-raw-status-codes`: "Clients MUST NOT show raw HTTP status codes to the user." From "no raw status codes shown to user;". Keyword MUST NOT ("no" wording). Added a line to `a-build-must-establish.md` and `look-for.md`.
- The `errors[]` sentences went under `may-add-extension-fields`.

## networking/offline-and-connectivity (2 sentences, 0 new rules)
Under `should-detect-conflicts-with-versions` and `should-roll-back-failed-optimistic-updates`.

## networking/rate-limiting (13 sentences, 0 new rules)
All under the existing rate-limiting rules. "429 responses are handled by waiting and retrying, never by an immediate or tight-loop retry;" went under `should-handle-429-gracefully`.

## networking/real-time-communication (3 sentences, 1 new rule)
- new rule: `must-reconnect-with-backoff`: "Persistent connections (SSE, WebSocket) MUST reconnect with backoff, never in an immediate retry loop." From "reconnection with backoff required for persistent connections". Keyword MUST ("required"). Added to `a-build-must-establish.md`. Both review parts already carry devteam's sentence for it.

## networking/retry-and-resilience (5 sentences, 0 new rules)
Under the existing retry rules. Possible tension, not a contradiction: "circuit breaker present or explicitly scoped out" and "circuit breaker or similar prevents cascading" against `should-use-a-circuit-breaker` (SHOULD), left as moved.

## security/cors (1 sentence), security/privacy (3 fragments)
- privacy: the three fragments were one sentence, so I placed it whole, once, under `should-support-apple-privacy-features`: "platform-specific privacy controls are honored (Apple usage-description keys and tracking/privacy APIs; Android scoped storage and pre-request rationale; web CSP, HttpOnly cookies and Do Not Track; Windows minimal manifest capabilities and DPAPI)."
- The opt-in sentence went under `should-require-opt-in-for-non-essential-data`.

## skills-and-agents/performance (1 sentence, 0 new rules)
- reader-specific: "Judge a Claude Code extension on speed and token efficiency across three principles." (a lead-in naming the reviewer's task), placed under `should-use-shell-scripts-for-deterministic-work`, since no rule concerns it more.

## testing/test-data (2 sentences, 0 new rules)
Under `should-avoid-large-shared-fixture-files` and `must-keep-specific-data-visible-in-the-test`.

## ui/theming (4 sentences, 1 new rule)
- new rule: `should-render-in-light-dark-and-high-contrast`: "The app SHOULD render correctly in Light, Dark, and High Contrast modes." From "app renders correctly in Light, Dark, and High Contrast modes;". Keyword SHOULD (plain check). Added to `a-build-must-establish.md` and a short line to `look-for.md`.

## planning/code-quality/purpose-classification (1 sentence, 0 new rules)
Under `should-classify-each-file-into-one-category`.

## testing/post-generation-verification (8 sentences, 0 new rules)
- Under `must-fix-failures-before-complete`, `must-pass-full-test-suite`, `must-verify-expected-log-messages`, `must-build-for-all-target-platforms` and `must-audit-accessibility`.
- reader-specific: "treat any unverified or skipped step as a failure — if any gate fails or was never run, the change is incomplete and MUST be fixed before merge, never waved through on \"should work\"." (reviewer stance)

## principles/manage-complexity-through-boundaries (7 sentences, 3 new rules)
- new rule `should-test-adapter-to-port-wiring`: "SHOULD have at least one integration test that verifies adapter-to-port wiring." From "at least one integration test verifies adapter-to-port wiring". SHOULD (plain check).
- new rule `should-expose-clear-skill-contracts`: "Skills SHOULD expose clear input/output contracts — well-defined interfaces between subsystems — and their inputs and outputs SHOULD be clearly documented." From "skills expose clear input/output contracts" and "Skill inputs and outputs are clearly documented;". SHOULD.
- new rule `should-give-agents-only-the-context-they-need`: "Agents SHOULD receive only the context needed for their task, not the full session history." From "agents receive only the context needed for their task (not the full session history);". SHOULD.
- Each new rule has its build line, and a short `look-for.md` line where devteam's sentence sat only in the review bar.
- "don't let external technology details bleed across boundaries" and "external tool calls wrapped behind a consistent interface rather than scattered inline" were placed under `should-use-adapters`, not made new rules.
- reader-specific: "agents receive only the context needed for their task (not the full session history);" (names agents and session history)

## principles/open-source-preference (3 sentences), principles/tight-feedback-loops (2 sentences)
Under existing rules, no new rules.
