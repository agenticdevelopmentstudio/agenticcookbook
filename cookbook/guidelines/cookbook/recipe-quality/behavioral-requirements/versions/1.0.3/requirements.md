
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

