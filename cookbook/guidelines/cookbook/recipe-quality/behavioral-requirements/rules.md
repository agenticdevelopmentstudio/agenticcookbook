
### RFC 2119 Keyword Usage

- **must-use-rfc-keywords-for-normative-statements**: Every normative statement MUST use one of the RFC 2119 keywords: MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, or OPTIONAL.
- **must-write-rfc-keywords-in-all-caps**: RFC 2119 keywords MUST appear in ALL CAPS when used with their normative meaning.
- **must-use-keywords-with-defined-semantics**: Authors MUST use the keywords with their defined semantics:
  - **MUST / SHALL / REQUIRED** — absolute requirement; non-compliance means the implementation does not conform.
  - **MUST NOT / SHALL NOT** — absolute prohibition.
  - **SHOULD / RECOMMENDED** — strongly recommended; a valid reason may justify deviation, but the deviation MUST be documented.
  - **SHOULD NOT** — strongly discouraged; a valid reason may justify the behavior, but it MUST be documented.
  - **MAY / OPTIONAL** — the implementation is free to include or omit this behavior.
- **must-not-treat-lowercase-keywords-as-normative**: Lowercase usage of these words (e.g., "must", "should") MUST NOT be interpreted as normative.
- **must-not-use-weaker-synonyms**: Authors MUST NOT use weaker synonyms (e.g., "needs to", "ought to", "has to") in place of normative keywords.

### Testability

- **must-be-independently-testable**: Each requirement MUST be independently testable. A developer MUST be able to write a concrete test — automated or manual — that produces a clear PASS or FAIL result for the requirement in isolation.
- **must-not-bundle-behaviors-into-one-requirement**: Requirements MUST NOT be compound statements that bundle multiple behaviors into a single sentence. Each discrete behavior MUST appear as its own requirement.
- **must-not-be-tautological-or-circular**: Requirements MUST NOT be tautological (e.g., "MUST work correctly") or circular (e.g., "MUST behave as expected").
- **must-include-specific-values-for-measurable-constraints**: Numeric or measurable constraints MUST include specific values.
- **should-not-use-unanchored-relative-terms**: A requirement SHOULD NOT use relative terms like "adequate", "sufficient", or "reasonable" without anchoring them to a concrete threshold.
- **must-cite-platform-standard-values**: Where platform standards define specific values (e.g., minimum touch target sizes, contrast ratios), requirements MUST cite those values explicitly.

### Behavior vs. Implementation

- **must-describe-observable-behavior**: Requirements MUST describe observable behavior, not implementation mechanism. The requirement constrains what the component does, not how it does it.
- **must-not-reference-platform-apis-unless-scoped**: Requirements MUST NOT reference platform-specific APIs, classes, or frameworks unless the recipe is explicitly platform-scoped and the API is the only conformant option.
- **must-use-platform-neutral-terms-for-shared-behavior**: When a behavior is the same across platforms, it MUST be expressed in platform-neutral terms, leaving the implementation choice to the developer.

### Specificity

- **should-give-measurable-values-in-must-requirements**: MUST requirements SHOULD include measurable, verifiable values wherever a standard or design decision provides them (e.g., "MUST display the error message within 300ms of the triggering event").
- **must-explain-rationale-for-should-requirements**: SHOULD requirements MUST explain the rationale for allowing deviation, either inline or in a linked Design Decisions section.
- **should-document-conditions-for-may-requirements**: MAY requirements SHOULD document the conditions under which each option is appropriate to avoid arbitrary implementation choices.

### Outcome vs. Attempt

- **must-describe-required-outcome**: A requirement MUST describe the required outcome, not the attempt — "MUST try to" implies effort, not outcome.
