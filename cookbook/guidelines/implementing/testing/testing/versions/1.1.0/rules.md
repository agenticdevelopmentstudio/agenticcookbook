
- **must-test-every-change**: Every change needs tests: it MUST have them.
- **must-include-a-test-file-per-implementation**: Every implementation MUST include a corresponding test file.
- **must-add-a-regression-test-per-bug-fix**: Every bug fix MUST have a regression test.
- **should-prioritize-unit-tests**: Unit tests SHOULD be prioritized over integration tests.
- **should-test-transitions-edge-cases-and-round-trips**: You SHOULD test state transitions, edge cases, and serialization round-trips.
- **should-test-component-logic-as-unit-tests**: UI tests are fragile — you SHOULD prefer testing component logic as unit tests.
- **should-use-playwright-for-end-to-end-tests**: In TypeScript, you SHOULD use [Playwright](https://playwright.dev/) for end-to-end and visual regression testing.
- **should-use-screenshot-comparison-for-snapshot-tests**: In TypeScript, screenshot comparison SHOULD be used for snapshot tests.
- **should-use-storybook-where-applicable**: In TypeScript, you SHOULD use Storybook for component catalog and visual tests where applicable.
- **should-use-xunit**: In C#, you SHOULD use [xUnit](https://xunit.net/) with `[Fact]` for single tests and `[Theory]`/`[InlineData]` for parameterized tests.
- **should-use-fluentassertions**: In C#, you SHOULD use [FluentAssertions](https://fluentassertions.com/) for readable assertions.
- **should-use-nsubstitute-for-mocking**: In C#, you SHOULD use [NSubstitute](https://nsubstitute.github.io/) for mocking.
- **should-use-pytest**: In Python, you SHOULD use `pytest` for all tests.
- **must-not-touch-production-dashboard-data**: Production dashboard data MUST NOT be removed or modified during testing — use demo port 9888, not production port 8888.

