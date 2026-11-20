
- **should-structure-tests-as-arrange-act-assert**: Every unit test SHOULD be structured as Arrange, Act, Assert (AAA): Arrange sets up preconditions, Act calls the method under test, and Assert verifies the result.
- **must-have-one-assertion-concept**: Each test MUST have one assertion concept (not one `assert` — one logical concept)
- **must-not-contain-logic**: Tests MUST NOT contain logic — no `if`, `for`, `try/catch`, `switch`
- **should-target-public-api**: Tests SHOULD target the public API, not internals — tests should survive refactoring
- **must-be-independent**: Each test MUST be independent — arrange its own state, don't rely on other tests
- **should-use-specification-names**: Tests SHOULD use descriptive names that read as specifications.
