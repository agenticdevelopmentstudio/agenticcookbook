<!-- leaf: implement-testing/unit-test-patterns · source: guidelines/implementing/testing/unit-test-patterns.md -->

**Rules** (cite as `implement-testing/unit-test-patterns#<slug>`):

- `test-have-one-assertion-concept` MUST — Each test MUST have one assertion concept (not one assert — one logical concept)
- `tests-not-contain-logic-try-catch` MUST — Tests MUST NOT contain logic — no if, for, try/catch, switch
- `tests-target-public-api-internals` SHOULD — Tests SHOULD target the public API, not internals — tests should survive refactoring
- `test-independent-arrange-own-state` MUST — Each test MUST be independent — arrange its own state, don't rely on other tests

# Unit Test Patterns

Structure every unit test as Arrange-Act-Assert with one assertion concept per test, no logic in tests, and no coupling between tests.

**Structure — Arrange, Act, Assert (AAA):**

```
// Arrange — set up preconditions
// Act — call the method under test
// Assert — verify the result
```

**Rules:**
- Each test MUST have one assertion concept (not one `assert` — one logical concept)
- Tests MUST NOT contain logic — no `if`, `for`, `try/catch`, `switch`
- Tests SHOULD target the public API, not internals — tests should survive refactoring
- Each test MUST be independent — arrange its own state, don't rely on other tests

**Naming — use descriptive names that read as specifications:**
- `test_parse_order_with_valid_json_returns_order`
- `ParseOrder_WithMissingField_ThrowsValidationError`
- `"returns empty list when no results match"`
