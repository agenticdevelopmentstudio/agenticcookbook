
- `should-use-fowlers-taxonomy`: each test double is named and used as the dummy, stub, spy, mock or fake it is
- `should-prefer-fakes-over-mocks`: a fake is used wherever one is possible
- `must-not-mock-what-you-dont-own`: no test mocks a type the project does not own
- `should-wrap-external-dependencies`: every external dependency is reached through the project's own interface
- `should-mock-your-interface-not-the-third-party-api`: mocks target the project's own interface only
- `should-use-platform-appropriate-mock-library`: each test uses its platform's mock library (NSubstitute/.NET, MockK/Kotlin, pytest-mock/Python, vitest/TS), or the build says why not
