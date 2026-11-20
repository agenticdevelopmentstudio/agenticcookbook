
- `should-structure-tests-as-arrange-act-assert`: each new unit test is laid out as Arrange, Act, Assert
- `must-have-one-assertion-concept`: each new unit test asserts one logical concept
- `must-not-contain-logic`: no new unit test contains `if`, `for`, `try/catch` or `switch`
- `should-target-public-api`: each new unit test calls only the public API of the unit under test
- `must-be-independent`: each new unit test arranges its own state and passes when run alone or in any order
- `should-use-specification-names`: each new unit test's name reads as a specification of the behavior it checks
