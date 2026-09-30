<!-- leaf: cookbook-recipe-quality/behavioral-requirements · source: guidelines/cookbook/recipe-quality/behavioral-requirements.md -->

**Rules** (cite as `cookbook-recipe-quality/behavioral-requirements#<slug>`):

- `what-component-pattern-do-commitments-teams-rely` MUST — The behavioral requirements section is the contractual core of a recipe. It defines what a component or pattern MUST, …
- `normative-statement-use-one-rfc-2119` MUST — Every normative statement MUST use one of the RFC 2119 keywords: MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, …
- `rfc-2119-keywords-appear-caps-used-their` MUST — RFC 2119 keywords MUST appear in ALL CAPS when used with their normative meaning.
- `authors-use-keywords-their-defined` MUST — Authors MUST use the keywords with their defined semantics: - MUST / SHALL / REQUIRED — absolute requirement; …
- `lowercase-usage-words-not-interpreted-normative` MUST — Lowercase usage of these words (e.g., "must", "should") MUST NOT be interpreted as normative.
- `authors-not-use-weaker-synonyms-needs` MUST — Authors MUST NOT use weaker synonyms (e.g., "needs to", "ought to", "has to") in place of normative keywords.
- `requirement-independently-testable-developer-able` MUST — Each requirement MUST be independently testable. A developer MUST be able to write a concrete test — automated or …
- `requirements-not-compound-statements-bundle-multiple` MUST — Requirements MUST NOT be compound statements that bundle multiple behaviors into a single sentence. Each discrete …
- `requirements-not-tautological-work-correctly-circular` MUST — Requirements MUST NOT be tautological (e.g., "MUST work correctly") or circular (e.g., "MUST behave as expected").
- `numeric-measurable-constraints-include-specific-values-requirement` MUST — Numeric or measurable constraints MUST include specific values. A requirement SHOULD NOT use relative terms like …
- `contrast-ratios-requirements-cite-values-explicitly` MUST — Where platform standards define specific values (e.g., minimum touch target sizes, contrast ratios), requirements MUST …
- `requirements-describe-observable-behavior-implementation` MUST — Requirements MUST describe observable behavior, not implementation mechanism. The requirement constrains what the …
- `requirements-not-reference-platform-specific-apis` MUST — Requirements MUST NOT reference platform-specific APIs, classes, or frameworks unless the recipe is explicitly …
- `same-across-platforms-expressed-platform-neutral-terms` MUST — When a behavior is the same across platforms, it MUST be expressed in platform-neutral terms, leaving the …
- `requirements-include-measurable-verifiable` MUST — MUST requirements SHOULD include measurable, verifiable values wherever a standard or design decision provides them …
- `requirements-explain-rationale-allowing` MUST — SHOULD requirements MUST explain the rationale for allowing deviation, either inline or in a linked Design Decisions …
- `requirements-document-conditions-under` SHOULD — MAY requirements SHOULD document the conditions under which each option is appropriate to avoid arbitrary …
- `vague-requirement` MUST — SHOULD handle errors appropriately. — "Appropriately" is undefined. The reviewer cannot test it; the developer cannot …
- `implementation-specific-language` MUST — MUST use UIAlertController to display the error. — This prescribes iOS SDK usage, eliminating valid alternatives and …
- `untestable-statement` MUST — MUST provide a good user experience. — No test can verify "good." This belongs in a design rationale section, not …
- `relative-threshold-with-no-anchor` MUST — MUST have adequate touch target size. — "Adequate" is unmeasurable. A conformant version: MUST have a touch target of …
- `missing-rfc-keyword` MUST — The button changes to a loading state after the user taps it. — This reads as a description, not a requirement. A …
- `compound-requirement` MUST — MUST display the error message and log it to the analytics service and disable the submit button. — This bundles three …
- `keyword-used-with-wrong-semantics` MUST — MUST try to validate input before submission. — "Must try" implies effort, not outcome. If validation is required, the …
- `verifier-check-following-items-recipe` MUST — A verifier MUST check each of the following items. The recipe PASSES behavioral requirements quality only if every item …
- `requirement-can-converted-directly` MUST — [ ] Every MUST requirement can be converted directly into a test case with a clear PASS/FAIL criterion.
- `requirements-document-link-rationale` SHOULD — [ ] SHOULD requirements document or link to a rationale for allowing deviation.

# Behavioral Requirements

The behavioral requirements section is the contractual core of a recipe. It defines what a component or pattern MUST, SHOULD, and MAY do — commitments that teams rely on when building, reviewing, and testing implementations. Requirements that are vague, implementation-specific, or untestable are not requirements at all: they give reviewers nothing to verify and developers nothing to implement against. This guideline defines the standard for well-formed requirements.

## Requirements

### RFC 2119 Keyword Usage

- Every normative statement MUST use one of the RFC 2119 keywords: MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, or OPTIONAL.
- RFC 2119 keywords MUST appear in ALL CAPS when used with their normative meaning.
- Authors MUST use the keywords with their defined semantics:
  - **MUST / SHALL / REQUIRED** — absolute requirement; non-compliance means the implementation does not conform.
  - **MUST NOT / SHALL NOT** — absolute prohibition.
  - **SHOULD / RECOMMENDED** — strongly recommended; a valid reason may justify deviation, but the deviation MUST be documented.
  - **SHOULD NOT** — strongly discouraged; a valid reason may justify the behavior, but it MUST be documented.
  - **MAY / OPTIONAL** — the implementation is free to include or omit this behavior.
- Lowercase usage of these words (e.g., "must", "should") MUST NOT be interpreted as normative.
- Authors MUST NOT use weaker synonyms (e.g., "needs to", "ought to", "has to") in place of normative keywords.

### Testability

- Each requirement MUST be independently testable. A developer MUST be able to write a concrete test — automated or manual — that produces a clear PASS or FAIL result for the requirement in isolation.
- Requirements MUST NOT be compound statements that bundle multiple behaviors into a single sentence. Each discrete behavior MUST appear as its own requirement.
- Requirements MUST NOT be tautological (e.g., "MUST work correctly") or circular (e.g., "MUST behave as expected").
- Numeric or measurable constraints MUST include specific values. A requirement SHOULD NOT use relative terms like "adequate", "sufficient", or "reasonable" without anchoring them to a concrete threshold.
- Where platform standards define specific values (e.g., minimum touch target sizes, contrast ratios), requirements MUST cite those values explicitly.

### Behavior vs. Implementation

- Requirements MUST describe observable behavior, not implementation mechanism. The requirement constrains what the component does, not how it does it.
- Requirements MUST NOT reference platform-specific APIs, classes, or frameworks unless the recipe is explicitly platform-scoped and the API is the only conformant option.
- When a behavior is the same across platforms, it MUST be expressed in platform-neutral terms, leaving the implementation choice to the developer.

### Specificity

- MUST requirements SHOULD include measurable, verifiable values wherever a standard or design decision provides them (e.g., "MUST display the error message within 300ms of the triggering event").
- SHOULD requirements MUST explain the rationale for allowing deviation, either inline or in a linked Design Decisions section.
- MAY requirements SHOULD document the conditions under which each option is appropriate to avoid arbitrary implementation choices.

## Common Violations

- **Vague requirement.** `SHOULD handle errors appropriately.` — "Appropriately" is undefined. The reviewer cannot test it; the developer cannot implement against it. A conformant version: `MUST display an inline error message adjacent to the triggering control when a validation error occurs.`
- **Implementation-specific language.** `MUST use UIAlertController to display the error.` — This prescribes iOS SDK usage, eliminating valid alternatives and making the requirement platform-locked. A conformant version: `MUST display the error in a modal dialog that blocks interaction until dismissed.`
- **Untestable statement.** `MUST provide a good user experience.` — No test can verify "good." This belongs in a design rationale section, not requirements.
- **Relative threshold with no anchor.** `MUST have adequate touch target size.` — "Adequate" is unmeasurable. A conformant version: `MUST have a touch target of at least 44×44pt on iOS and 48×48dp on Android.`
- **Missing RFC keyword.** `The button changes to a loading state after the user taps it.` — This reads as a description, not a requirement. A developer reading it cannot know if deviation is acceptable. It MUST include MUST or SHOULD.
- **Compound requirement.** `MUST display the error message and log it to the analytics service and disable the submit button.` — This bundles three independently testable behaviors. Each MUST be a separate requirement.
- **Keyword used with wrong semantics.** `MUST try to validate input before submission.` — "Must try" implies effort, not outcome. If validation is required, the requirement MUST describe the required outcome, not the attempt.

## Verification Checklist

A verifier MUST check each of the following items. The recipe PASSES behavioral requirements quality only if every item is satisfied.

- [ ] Every normative statement uses an ALL-CAPS RFC 2119 keyword.
- [ ] No lowercase usage of "must", "should", "may" appears in a normative context.
- [ ] No weaker synonyms ("needs to", "ought to", "has to") substitute for RFC keywords.
- [ ] Each requirement tests a single, discrete behavior — no compound statements.
- [ ] Every MUST requirement can be converted directly into a test case with a clear PASS/FAIL criterion.
- [ ] No requirement references a platform-specific API or framework class unless the recipe is explicitly platform-scoped.
- [ ] All measurable thresholds (sizes, durations, counts, ratios) are expressed as specific numeric values.
- [ ] No requirement uses relative qualifiers ("adequate", "reasonable", "appropriate", "good") without a numeric anchor.
- [ ] SHOULD requirements document or link to a rationale for allowing deviation.
- [ ] No tautological or circular requirements exist.
- [ ] Requirements do not describe internal state or memory layout — only observable behavior.
