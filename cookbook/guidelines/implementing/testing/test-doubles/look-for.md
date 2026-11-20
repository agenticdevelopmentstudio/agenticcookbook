
- `should-use-fowlers-taxonomy`: a test double named or built as a kind that does not match what it does (a "mock" that only returns canned answers)
- `should-prefer-fakes-over-mocks`: a mock where a fake was possible
- `must-not-mock-what-you-dont-own`: a mock of a third-party type the project does not own
- `should-wrap-external-dependencies`: an HTTP client, database or SDK used directly with no project-owned interface in front
- `should-mock-your-interface-not-the-third-party-api`: a mock set on the third-party API rather than the project's interface

