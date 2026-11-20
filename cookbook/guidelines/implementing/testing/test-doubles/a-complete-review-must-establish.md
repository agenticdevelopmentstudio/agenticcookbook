
- `should-use-fowlers-taxonomy`: whether each test double is the dummy, stub, spy, mock or fake its role calls for
- `should-prefer-fakes-over-mocks`: whether fakes were used wherever possible instead of mocks
- `must-not-mock-what-you-dont-own`: whether any test mocks a type the project does not own
- `should-wrap-external-dependencies`: whether external dependencies sit behind the project's own interface
- `should-mock-your-interface-not-the-third-party-api`: whether mocks target the project's interface rather than the third-party API
- `should-use-platform-appropriate-mock-library`: platform-appropriate mock library used (NSubstitute/.NET, MockK/Kotlin, pytest-mock/Python, vitest/TS)
