# Devteam text batch 4 report

All 17 topics were placed, checked (`roles gaps` 0 lacking, `roles check` 0, `roles lossless` 0), bumped, approved and committed one per topic.
For `data/clock-systems`, `data/normalization-and-denormalization` and `data/sync-schema-design`, `roles lossless` was run with `--base 1a179b2`, the base recorded in each topic's own `lossless.json`. `--base 0005775` fails for them ("cookbook/guidelines/planning/data/clock-systems is not in 0005775"), because those topics had folded copies.

## behavioral-requirements (86e76f21)
- new rules: none.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## cross-recipe-consistency (0e2b8362)
- new rules: none. "Cross-references use correct scope identifiers." was placed under `must-reference-siblings-by-uuid`; "scope identifiers" is the nearest rule, so the owner may rule on it.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## atomic-commits (bcb75805), also carries code-quality/version-discipline
- new rules:
  - `should-bump-version-in-same-change` (SHOULD): "A meaningful change to a versioned artifact SHOULD carry its version bump in the same change (one logical change includes its version metadata): frontmatter `version:` fields in ..." From "A meaningful change to a versioned artifact carries its version bump in the same change ...". SHOULD because it is a plain check and the same text says "a bump rule may not exist".
  - `should-match-version-bump-magnitude` (SHOULD): "Version fields a change touches SHOULD move by a magnitude that matches the change (patch for fixes, minor for new behavior, major for breaking)." From "version fields the diff does touch move by a magnitude that matches the change ...".
- reader-specific:
  - "Act on the machine-raised VERSION HYGIENE leads in your slice — you are their owner: verify each against the repo's own conventions (a bump rule may not exist; confirm before filing) and file at most ONE finding listing every affected file." (placed under `should-bump-version-in-same-change`)
  - "No `review_signals` gate on purpose: the leads land on any file type, so this lens rides whenever the specialist is convened."
  - "Every VERSION HYGIENE lead in the slice was either confirmed against a repo convention and folded into the single finding, or explicitly cleared as trivial/no-convention."
  - "Judge from the diff and messages only — never demand evidence that a build or test run happened before the commit."
- contradictions (R4):
  - "Judge from the diff and messages only — never demand evidence that a build or test run happened before the commit." against the topic rule `must-pass-build-and-tests-before-commit`: "The build MUST pass and existing tests MUST still pass before committing." (and review-bar "at every commit the build passes and existing tests still pass").
- not placed: none.

## clock-systems (a17ddc2a)
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (process; placed under `must-not-order-by-wall-clock-alone`, the first rule, since the review-bar bullets name no rule).
- contradictions: none.
- not placed: none.

## normalization-and-denormalization (95a884e8)
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (placed under `should-start-at-3nf`, the first rule).
- contradictions: none.
- not placed: none.

## sync-schema-design (6a9ca375)
- new rules: none.
- reader-specific: "A review passes when it establishes every item above." (placed under `must-use-uuid-primary-keys`, the first rule).
- contradictions: none.
- not placed: none.

## background-tasks (7a7dabbf)
- new rules: none. The three review-bar fragments sit under `windows-register-triggers-in-manifest`, `design-tasks-to-be-resumable` and `use-platform-background-apis`.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## prefer-explicit-apple-apis (bad0d86a)
- new rules: none.
- reader-specific: "SwiftUI MUST appear only where Apple requires it, so flag SwiftUI used for ordinary app UI when an imperative AppKit/UIKit equivalent exists." ("flag" is a reviewer instruction).
- contradictions: none.
- not placed: none.

## input-validation (dfe42b78)
- new rules: none.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## property-based-testing (2a680984)
- new rules: `should-test-preservation-property-for-collection-operations` (SHOULD): "A preservation property SHOULD be tested for collection operations." From "preservation property tested for collection operations" (plain check, so SHOULD).
- reader-specific: none.
- contradictions: none.
- not placed: none.

## unit-test-patterns (267aac8a)
- new rules: none.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## touch-click-targets (4d74fdf4)
- new rules: none. The Web/WCAG 24x24 minimum text was placed under `should-defer-to-platform-hig-minimum`, and "adjacent targets are separated by at least 8px;" under `must-space-adjacent-targets-8px`.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## database-testing (4f317f9b)
- new rules: none.
- reader-specific: "Verifies test database selection ...", "Reviews test fixtures and seed data organization.", "Validates sync logic testing including change detection, push/pull success criteria, and conflict resolution." (reviewer-role sentences).
- contradictions: none.
- not placed: none.

## flaky-test-prevention (f646186b)
- new rules: none.
- reader-specific: "Review the test changes for every source of nondeterminism: tests MUST NOT share mutable state (...)" and the "flag class-level, module-level, or global mutable fields" instruction.
- contradictions: none.
- not placed: none.

## fail-fast (3b8804ae)
- new rules: none.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## meta-principle-optimize-for-change (78b3da98)
- new rules:
  - `should-not-take-unacknowledged-easier-now-harder-later-shortcuts` (SHOULD NOT): "\"Easier now, harder later\" shortcuts SHOULD NOT be taken without explicit acknowledgment." From "no \"easier now, harder later\" shortcuts taken without explicit acknowledgment;" (negative check; SHOULD NOT since the topic's own rules here are SHOULD).
  - `should-provide-extension-points-where-change-is-anticipated` (SHOULD): "Key extension points (swappable backends, injectable services) SHOULD be present where change is anticipated." From "key extension points (swappable backends, injectable services) present where change is anticipated".
- reader-specific: "use this as the meta-question when tradeoffs arise".
- contradictions: none.
- not placed: none.

## small-reversible-decisions (f1826e58)
- new rules: none. "reversibility considered when choosing between design options" went under `should-make-cheap-to-reverse-decisions-fast` as the nearest rule.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## Unfinished
Nothing.
