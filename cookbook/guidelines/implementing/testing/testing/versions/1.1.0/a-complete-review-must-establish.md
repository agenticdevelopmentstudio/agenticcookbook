
- `must-test-every-change`: whether every change has tests
- `must-include-a-test-file-per-implementation`: whether every implementation has a corresponding test file
- `must-add-a-regression-test-per-bug-fix`: whether every bug fix has a regression test
- `should-prioritize-unit-tests`: whether unit tests are prioritized over integration tests
- `should-test-transitions-edge-cases-and-round-trips`: whether state transitions, edge cases and serialization round-trips are tested
- `should-test-component-logic-as-unit-tests`: whether component logic is tested as unit tests rather than UI tests
- `should-use-playwright-for-end-to-end-tests`: whether TypeScript end-to-end and visual regression tests use Playwright
- `should-use-screenshot-comparison-for-snapshot-tests`: whether TypeScript snapshot tests use screenshot comparison
- `should-use-storybook-where-applicable`: whether Storybook is used for the component catalog and visual tests where applicable
- `should-use-xunit`: whether C# tests use xUnit `[Fact]` and `[Theory]`/`[InlineData]`
- `should-use-fluentassertions`: whether C# assertions use FluentAssertions
- `should-use-nsubstitute-for-mocking`: whether C# mocking uses NSubstitute
- `should-use-pytest`: whether all Python tests use `pytest`
- `must-not-touch-production-dashboard-data`: whether any test removes or modifies production dashboard data or uses port 8888

