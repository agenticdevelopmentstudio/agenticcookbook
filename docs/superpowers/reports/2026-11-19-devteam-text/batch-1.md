# Devteam text batch 1 report (R7)

All 15 topics done: every lacking sentence placed verbatim, `roles gaps` reports 0 lacking for every file, `roles check` and `roles lossless` exit 0, bumped, approved, committed one commit per topic. Nothing in "not placed".

Note on `roles lossless`: topics folded from copies (indexing, schema-evolution, feature-flags) fail with `--base 0005775` ("<copy> is not in 0005775"); they pass with the base recorded in their own `lossless.json` (1a179b2, 1a179b2, cd4a714). Schema-evolution's one obsolete entry's pin went stale when its review-bar part changed, so it was re-judged by an independent judge (sonnet), verdict pass, written into its `lossless.json`.

## recipe-quality/completeness (0d4451e6)
- placed 1, new rules 0.
- reader-specific: none.

## code-quality/linting (7942c8ec)
- placed 2, new rules 2.
- new rule `must-not-suppress-lint-inline-without-justification` ("Lint errors MUST NOT be suppressed inline without justification."), from "no lint errors suppressed inline without justification;", MUST NOT ("no" wording).
- new rule `should-document-formatter-command` ("The formatter command SHOULD be documented in the README or Makefile."), from "formatter command documented in README or Makefile", SHOULD (plain check).

## concurrency/immutability (f7f544d1)
- placed 1, new rules 1.
- new rule `must-not-access-shared-mutable-fields-unsynchronized` ("Mutable shared fields MUST NOT be accessed from multiple concurrent contexts without synchronization."), from "no mutable shared fields accessed from multiple concurrent contexts without synchronization", MUST NOT.

## data/indexing (2c31feb1)
- placed 1, new rules 0.
- reader-specific: "A review passes when it establishes every item above." (placed as a closing plain line at the end of the review-bar part, not a bullet, since no rule it concerns).

## data/schema-evolution (ec0837de)
- placed 1, new rules 0.
- reader-specific: "A review passes when it establishes every item above." (closing plain line, as above).

## feature-management/feature-flags (36b8d31c)
- placed 1, new rules 0.
- reader-specific: "A review passes when it establishes every item above." (closing plain line, as above).

## observability/logging (3f778f00)
- placed 5, new rules 0 (all under existing rules: `should-use-android-log-with-consistent-tags`, `should-emit-telemetry-via-opentelemetry` x2, `should-follow-otel-semantic-conventions`, `must-not-log-pii`).
- reader-specific: none. Fragments keep their original leading "and" and trailing ";".

## platform-integration/handoff-and-continuity (187453f1)
- placed 4, new rules 2.
- new rule `windows-use-protocol-activation-uris` ("On Windows, you SHOULD use protocol activation URIs as the cross-device handoff mechanism."), from "protocol activation URIs as cross-device handoff mechanism;" and "Key views have protocol activation URIs suitable for cross-device handoff;", SHOULD.
- new rule `windows-resolve-uris-on-web-or-mobile` ("On Windows, handoff URIs SHOULD resolve on web or mobile equivalents."), from "URLs resolve on web or mobile equivalents;", SHOULD.
- "state encoded in URI is sufficient to restore context" placed under existing `capture-enough-state`.

## platform-integration/search-integration (f193d2ec)
- placed 3, new rules 1.
- new rule `windows-deploy-property-handlers-for-custom-file-types` ("On Windows, you SHOULD deploy property handlers for custom file types."), from "property handlers deployed for custom file types;", SHOULD.
- "indexed items resolve via protocol activation;" and "search results navigate to correct content" placed under existing `must-deep-link-indexed-items`.

## platform-integration/share-and-inter-app-data (bbbd3232)
- placed 2, new rules 1.
- new rule `windows-check-clipboard-format-availability` ("On Windows, clipboard operations SHOULD handle format availability checks."), from "clipboard operations handle format availability checks", SHOULD.
- "`ACTION_SEND` intent filter present for expected MIME types;" placed under existing `android-declare-send-intent-filter`.

## skills-and-agents/copilot-configuration (b59c95ef)
- placed 1, new rules 0 ("agent instruction files do not disagree." under `should-not-carry-conflicting-agent-files`).

## ui/form-design (636f363e)
- placed 2, new rules 1.
- new rule `should-link-errors-to-fields-with-aria-describedby` ("An inline error message SHOULD be linked to its field with ARIA (`aria-describedby`)."), from "`aria-describedby` links field to error;" and the ARIA clause of the review-focus sentence, SHOULD (plain check).
- The one-sentence review-focus list ("Single-column layout, `<label>` top-aligned or floating, ...") spans many rules; placed as one verbatim bullet under `must-show-errors-inline`.

## planning/code-quality/app-interactions (84b5165d)
- placed 1, new rules 0.
- reader-specific (process): "Map how components communicate with each other." placed under `should-note-notification-endpoints`, the nearest rule; no rule invented for it.

## planning/code-quality/framework-conventions (03782e18)
- placed 4, new rules 0 (all under `should-flag-convention-deviations`).
- reader-specific: "In the code **this diff adds or changes**, identify the MVC/MVVM/MVP/TCA pattern, View+ViewModel pairs, Controller+Routes groupings, middleware chains, service/repository patterns, and plugin architectures it participates in — and flag where the change deviates from the surrounding convention."; "For the units the diff adds or changes, the framework convention they follow is identified and any deviation the change introduces is flagged;"; "a diff that raises no convention question is explicitly cleared."; "Scope is the change under review — NOT a whole-codebase inventory."
- contradictions (R4), left unfixed: "Scope is the change under review — NOT a whole-codebase inventory." against topic rule `should-default-to-conventional-units`: "When the codebase follows framework conventions, those conventions **SHOULD** define the scope groups". The topic works over the whole codebase; devteam's text scopes to the diff.

## testing/mutation-testing (05c82531)
- placed 3, new rules 0 (under `must-run-before-claiming-complete`, `must-address-all-surviving-mutants`, `should-repeat-until-score-acceptable`).
- reader-specific: none.
