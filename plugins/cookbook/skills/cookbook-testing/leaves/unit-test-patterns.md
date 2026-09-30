<!-- leaf: cookbook-testing/unit-test-patterns · source: guidelines/cookbook/testing/unit-test-patterns.md -->

**Rules** (cite as `cookbook-testing/unit-test-patterns#<slug>`):

- `vector-cookbook-artifact-follow-arrange-act-assert` SHOULD — Each test vector in a cookbook artifact SHOULD follow the Arrange-Act-Assert pattern:
- `vector-test-one-behavioral-concept` MUST — Each vector MUST test one behavioral concept — not multiple unrelated assertions
- `vectors-not-depend-other-self-contained` MUST — Vectors MUST NOT depend on each other — each is self-contained
- `vectors-target-public-api-described` SHOULD — Vectors SHOULD target the public API described in the artifact's requirements, not implementation details
- `generators-so-they-clear-enough-serve-test` MUST — These names will be used verbatim by code generators, so they MUST be clear enough to serve as test documentation.

# Unit Test Patterns

When writing test vectors in cookbook artifacts (ingredients and recipes), structure them as Arrange-Act-Assert specifications so that code generators produce well-structured test code.

## Test vector structure

Each test vector in a cookbook artifact SHOULD follow the Arrange-Act-Assert pattern:

- **Arrange** — describe the preconditions and input state
- **Act** — describe the action or method call being tested
- **Assert** — describe the expected outcome

## Rules for test vectors

- Each vector MUST test one behavioral concept — not multiple unrelated assertions
- Vectors MUST NOT depend on each other — each is self-contained
- Vectors SHOULD target the public API described in the artifact's requirements, not implementation details

## Naming test vectors

Use descriptive names that read as specifications:
- `test_parse_order_with_valid_json_returns_order`
- `ParseOrder_WithMissingField_ThrowsValidationError`
- `"returns empty list when no results match"`

These names will be used verbatim by code generators, so they MUST be clear enough to serve as test documentation.
