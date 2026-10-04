
# Test Data

Build test data inline using builders or factories so every test declares exactly what it needs. Avoid shared fixture files and magic data.

**Construct what you need, per test.** Avoid large shared fixture files.

- **Builder pattern** or **factory functions** SHOULD be used for complex objects — each test calls
  `makeOrder(status: .pending)` with only the fields it cares about, defaults for the rest
- **Property-based generators** (Hypothesis strategies, fast-check arbitraries) for
  comprehensive input coverage
- **Inline literals** for simple cases — `assert parse("hello") == "hello"` is clear
- **No magic fixtures** — if a test needs specific data, the data MUST be visible in the test

