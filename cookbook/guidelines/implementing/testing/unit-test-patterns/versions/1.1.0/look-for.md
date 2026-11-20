
- `should-structure-tests-as-arrange-act-assert`: each test body falls into an arrange block, a single act (the call under test) and an assert block, in that order; interleaved acts and asserts break it
- `must-have-one-assertion-concept`: each test's assertions all check one logical outcome; asserts on unrelated outcomes in one test break it
- `must-not-contain-logic`: no `if`, `for`, `try/catch` or `switch` in a test body
- `should-target-public-api`: tests call the unit's public API, not private members, internal state or reflection into internals
- `must-be-independent`: each test arranges its own state; shared mutable state, ordering dependencies or one test reading another's output break it
- `should-use-specification-names`: test names state the scenario and the expected result, like `ParseOrder_WithMissingField_ThrowsValidationError`, not `test1` or `testParse`
