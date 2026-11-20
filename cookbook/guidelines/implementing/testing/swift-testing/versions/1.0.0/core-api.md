
- **`@Test`** marks a function as a test. The function **MAY** be a global function or a method, and **MAY** be `async`, `throws`, or isolated to a global actor (e.g. `@MainActor`). A descriptive display name **SHOULD** be passed: `@Test("Parses ISO-8601 dates")`.
- **`#expect(expr)`** records a failure but continues; use it for ordinary assertions. It captures sub-expression values, so a single `#expect(a == b)` reports both operands on failure — you **SHOULD NOT** add a custom message that restates the expression.
- **`#require(expr)`** throws and halts the test when the expectation fails; use it for preconditions whose failure makes the rest of the test meaningless. `try #require(optional)` unwraps an optional and aborts on `nil`, replacing force-unwraps.
- Use **`#expect(throws:)`** / `#require(throws:)` to assert error behavior instead of `do/catch`.

