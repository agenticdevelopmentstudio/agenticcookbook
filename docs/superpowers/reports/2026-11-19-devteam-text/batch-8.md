# Devteam text batch 8 report

All 18 topics placed, `roles gaps` 0 lacking for every file, `roles check` 0, `roles lossless` 0, approved, one commit each.

Process notes:
- `roles lossless --base` uses each topic's own `lossless.json` base, not `0005775`, where they differ: `data/foreign-keys` and `data/relationships` account for `1a179b2`, and `feature-management/debug-mode` for `2071c94e51a8c517e11178fdee54e0ec033064c2`. `0005775` is refused for them.
- `feature-management/debug-mode`: adding a bullet to its review-bar part made the judged verdict for entry 16 stale (a pin covers the target's whole text). An independent opus judge re-judged it (pass) and the new pin was written to its `lossless.json`.
- `data/foreign-keys` and `data/relationships`: a stray blank line before my bar bullet was removed in a follow-up commit each (00af28fb, c53ef834).
- Bullets that name an unnamed-bullet part (foreign-keys, relationships, debug-mode bar) carry a backticked rule name as the brief says, so they differ in shape from their neighbours.

## accessibility/font-scaling
- new rules: `should-use-sp-for-text-sizes` (SHOULD) from "use sp units for text, avoid fixed dp font sizes"; `should-use-scrollable-containers-for-expanding-text` (SHOULD) from "scrollable containers used where text may expand".
- reader-specific: none. contradictions: none. not placed: none.

## code-quality/naming
- new rules: none. The lead-in "Hold every identifier to .NET's established casing conventions applied consistently:" is joined to its two items as sub-bullets under `should-use-dotnet-casing-consistently`.
- reader-specific: none. contradictions: none. not placed: none.

## code-quality/nullable-reference-types
- new rules: `should-throw-if-null-at-entry-points` (SHOULD) from "`ArgumentNullException.ThrowIfNull` used at entry points;".
- reader-specific: none. contradictions: none. not placed: none.

## data/foreign-keys
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (process; placed under `must-enable-foreign-keys-per-connection`, the first rule, in the review-bar part).
- contradictions: none. not placed: none.

## data/relationships
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (process; placed under `must-index-fk-column`, the first rule).
- contradictions: none. not placed: none.

## feature-management/debug-mode
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (process; placed under `debug-only-config-panel`, the first rule).
- contradictions: none. not placed: none.

## networking/api-design
- new rules: `should-display-field-level-errors-for-422` (SHOULD) from "422 responses display field-level errors;".
- reader-specific: none. contradictions: none. not placed: none.

## networking/timeouts
- new rules: none (all nine sentences sit under the existing connection/read, infinite, default and 202 rules).
- reader-specific: "infinite timeouts must never be used, so flag any request configured with no timeout or with a 0/null/disabled timeout that lets it block forever." ("flag").
- contradictions: none. not placed: none.

## platform-integration/deep-linking
- new rules: `apple-support-universal-links-and-url-schemes` (SHOULD) from "On Apple, look for Universal Links plus custom URL schemes, with `onOpenURL` ..."; `android-declare-app-links-and-intent-filters` (SHOULD) from "On Android, look for App Links and `<intent-filter>` declarations ...". Keyword SHOULD chosen as a plain check.
- reader-specific: "flag any meaningful view reachable only by in-app navigation with no addressable entry point."; "Also check that the feature's spec carries a dedicated Deep Linking section defining its URL patterns." ("the feature's spec").
- contradictions: none. not placed: none.

## skills-and-agents/agent-structure-reference
- new rules: `should-keep-system-prompt-focused-and-unambiguous` (SHOULD) from "system prompt is focused and unambiguous".
- reader-specific: none. contradictions: none. not placed: none.

## skills-and-agents/rule-structure-reference
- new rules: none. "quality criteria — imperative tone, deterministic, explicit file refs, no vague directives;" is placed whole under `should-use-an-imperative-tone`; it spans four rules.
- reader-specific: none. contradictions: none. not placed: none.

## ui/layout
- new rules: `must-not-use-inline-style-pixel-widths` (MUST NOT) from "No inline style pixel widths for layout;"; `should-use-em-rem-or-device-class-breakpoints` (SHOULD) from "breakpoints use `em`/`rem` or device-class media queries;"; `should-match-dom-order-to-reading-order` (SHOULD) from "DOM order matches visual reading order".
- reader-specific: none. contradictions: none. not placed: none.

## ui/typography
- new rules: none. "System font used (not custom fonts without justification);" is placed under `must-use-platform-system-font`.
- reader-specific: none.
- contradictions: possible tension, not a direct conflict: the rule is "The platform's system font MUST be used", while devteam's sentence allows custom fonts with justification. Left unfixed.
- not placed: none.

## planning/code-quality/system-dependencies
- new rules: `should-identify-introduced-system-dependencies` (SHOULD) from "Identify OS framework imports, SDK usage, ... introduced or changed by this diff, mapping each to the code unit that uses it." and "a diff that introduces none is explicitly cleared."; `must-scope-system-dependencies-to-the-change` (MUST NOT, from "NOT") from "Scope is the change under review — NOT a whole-codebase inventory." In both rules "this diff" is written "the change under review".
- reader-specific: "introduced or changed by this diff"; "a diff that introduces none is explicitly cleared."; "Scope is the change under review — NOT a whole-codebase inventory."
- contradictions: this topic's rules group a codebase into scope groups, which is a whole-codebase view, against devteam's diff-only scope. No rule is directly contradicted. Left unfixed.
- not placed: none.

## shipping/msix-packaging
- new rules: none.
- reader-specific: none. contradictions: none. not placed: none.

## principles/design-for-deletion
- new rules: `should-delete-rules-that-no-longer-apply` (SHOULD) from "treat lines of instructions as lines spent — delete rules that no longer apply;" and "dead rules (no longer triggered) removed rather than kept "just in case"".
- reader-specific: none. contradictions: none. not placed: none.

## principles/explicit-over-implicit
- new rules: `must-not-hide-behavior-behind-magic-invocation` (MUST, from "no hidden behavior or magic invocation paths") and `should-say-what-to-do-not-how-to-figure-it-out` (SHOULD, from "agent instructions say what to do, not how to "figure it out";").
- reader-specific: none. contradictions: none. not placed: none.

## principles/immutability-by-default
- new rules: `must-not-share-mutable-state-across-concurrent-contexts` (MUST NOT) from "no shared mutable state across concurrent contexts;".
- reader-specific: none. contradictions: none. not placed: none.
