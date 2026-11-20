
- **`@Test`** marks a function as a test.
- **`#expect(expr)`** records a failure but continues.
- **`#require(expr)`** throws and halts the test when the expectation fails. `try #require(optional)` unwraps an optional and aborts on `nil`, replacing force-unwraps.

