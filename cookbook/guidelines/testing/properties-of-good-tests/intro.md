
# Properties of Good Tests

From Kent Beck's Test Desiderata — tests should be:

1. **Isolated** — tests MUST NOT share mutable state or depend on execution order
2. **Composable** — tests MUST be runnable in any subset and any order
3. **Deterministic** — tests MUST produce the same result every time, no flakiness
4. **Fast** — milliseconds per unit test, seconds per integration test
5. **Writable** — easy to author, low ceremony
6. **Readable** — a failing test tells you what broke and why
7. **Behavioral** — tests SHOULD verify what the code does, not how it does it
8. **Structure-insensitive** — refactoring internals SHOULD NOT break tests
9. **Automated** — no manual steps, no human judgment needed
10. **Specific** — a failure points to exactly one cause
11. **Predictive** — passing tests mean the code works in production
12. **Inspiring** — confidence to refactor and ship

