
- `must-test-every-change`: every change ships with tests
- `must-include-a-test-file-per-implementation`: every implementation file has a corresponding test file
- `must-add-a-regression-test-per-bug-fix`: every bug fix has a regression test that fails without the fix
- `should-prioritize-unit-tests`: unit tests carry the coverage, integration tests the rest
- `should-test-transitions-edge-cases-and-round-trips`: state transitions, edge cases and serialization round-trips have tests
- `should-test-component-logic-as-unit-tests`: component logic has unit tests
- `should-use-playwright-for-end-to-end-tests`: TypeScript end-to-end and visual regression tests run on Playwright
- `should-use-screenshot-comparison-for-snapshot-tests`: TypeScript snapshot tests compare screenshots
- `should-use-storybook-where-applicable`: applicable TypeScript components have Storybook stories
- `should-use-xunit`: C# tests use xUnit, `[Fact]` for single and `[Theory]`/`[InlineData]` for parameterized tests
- `should-use-fluentassertions`: C# assertions use FluentAssertions
- `should-use-nsubstitute-for-mocking`: C# mocks use NSubstitute
- `should-use-pytest`: all Python tests run under `pytest`
- `must-not-touch-production-dashboard-data`: tests use demo port 9888 and leave production dashboard data unchanged

