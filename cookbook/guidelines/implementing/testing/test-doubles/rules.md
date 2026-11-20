
- **should-use-fowlers-taxonomy**: You SHOULD use [Martin Fowler's taxonomy](https://martinfowler.com/bliki/TestDouble.html) for test doubles: dummy, stub, spy, mock and fake.
- **should-prefer-fakes-over-mocks**: Fakes SHOULD be preferred over mocks when possible.
- **must-not-mock-what-you-dont-own**: You MUST NOT mock what you don't own.
- **should-wrap-external-dependencies**: You SHOULD wrap external dependencies (HTTP clients, databases, SDKs) behind your own interface.
- **should-mock-your-interface-not-the-third-party-api**: You SHOULD mock your interface, not the third-party API directly.
- **should-use-platform-appropriate-mock-library**: SHOULD use the platform-appropriate mock library (NSubstitute/.NET, MockK/Kotlin, pytest-mock/Python, vitest/TS).
