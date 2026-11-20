
- `should-structure-tests-as-arrange-act-assert`: every unit test in the change follows Arrange, Act, Assert, or the code says why not
- `must-have-one-assertion-concept`: every unit test in the change asserts one logical concept
- `must-not-contain-logic`: no unit test in the change contains `if`, `for`, `try/catch` or `switch`
- `should-target-public-api`: every unit test in the change targets the public API, not internals, or the code says why not
- `must-be-independent`: every unit test in the change arranges its own state and relies on no other test
- `should-use-specification-names`: every unit test in the change has a descriptive name that reads as a specification, or the code says why not
