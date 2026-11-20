
- **should-construct-what-each-test-needs**: You SHOULD construct what you need, per test.
- **should-avoid-large-shared-fixture-files**: You SHOULD avoid large shared fixture files.
- **should-use-builders-or-factories-for-complex-objects**: A builder pattern or factory functions SHOULD be used for complex objects — each test calls `makeOrder(status: .pending)` with only the fields it cares about, defaults for the rest.
- **should-use-property-based-generators-for-coverage**: Property-based generators (Hypothesis strategies, fast-check arbitraries) SHOULD be used for comprehensive input coverage.
- **should-use-inline-literals-for-simple-cases**: Inline literals SHOULD be used for simple cases — `assert parse("hello") == "hello"` is clear.
- **must-keep-specific-data-visible-in-the-test**: No magic fixtures — if a test needs specific data, the data MUST be visible in the test.

