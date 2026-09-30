<!-- leaf: cookbook-testing/properties-of-good-tests · source: guidelines/cookbook/testing/properties-of-good-tests.md -->

**Rules** (cite as `cookbook-testing/properties-of-good-tests#<slug>`):

- `isolated` MUST — each test vector MUST be independent; no shared mutable state or ordering dependency between vectors
- `deterministic` MUST — the expected result MUST be unambiguous; the same input always produces the same output
- `behavioral` SHOULD — test vectors SHOULD verify what the component does, not how it does it internally
- `specific` SHOULD — each vector SHOULD target one behavior or edge case; a failure points to exactly one cause
- `readable` MUST — a test vector MUST clearly communicate what it tests and what the expected outcome is
- `predictive` SHOULD — the set of test vectors SHOULD be sufficient to catch real bugs; if all vectors pass, the implementation is likely …

# Properties of Good Tests

When writing test vectors in cookbook artifacts (ingredients and recipes), each test vector should exhibit these properties — adapted from Kent Beck's Test Desiderata.

## For test vectors in cookbook artifacts

1. **Isolated** — each test vector MUST be independent; no shared mutable state or ordering dependency between vectors
2. **Deterministic** — the expected result MUST be unambiguous; the same input always produces the same output
3. **Behavioral** — test vectors SHOULD verify what the component does, not how it does it internally
4. **Specific** — each vector SHOULD target one behavior or edge case; a failure points to exactly one cause
5. **Readable** — a test vector MUST clearly communicate what it tests and what the expected outcome is
6. **Predictive** — the set of test vectors SHOULD be sufficient to catch real bugs; if all vectors pass, the implementation is likely correct

## Less relevant for cookbook authoring

The remaining Beck desiderata (fast, composable, writable, automated, structure-insensitive, inspiring) apply to the generated test code, not to the test vector specifications in cookbook artifacts. They are covered by the implementing and testing use cases.
