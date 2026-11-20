
- `must-test-every-change`: a change with no tests
- `must-include-a-test-file-per-implementation`: an implementation file with no corresponding test file
- `must-add-a-regression-test-per-bug-fix`: a bug fix with no regression test
- `should-prioritize-unit-tests`: behavior covered by an integration test where a unit test would serve
- `should-test-transitions-edge-cases-and-round-trips`: missing tests for state transitions, edge cases or serialization round-trips
- `should-test-component-logic-as-unit-tests`: component logic tested only through a UI test
- `should-use-playwright-for-end-to-end-tests`: TypeScript end-to-end or visual regression tests on a tool other than Playwright
- `should-use-screenshot-comparison-for-snapshot-tests`: a TypeScript snapshot test without screenshot comparison
- `should-use-storybook-where-applicable`: TypeScript components with no Storybook catalog or visual tests where they apply
- `should-use-xunit`: C# tests not on xUnit, or parameterized cases without `[Theory]`/`[InlineData]`
- `should-use-fluentassertions`: C# assertions not written with FluentAssertions
- `should-use-nsubstitute-for-mocking`: C# mocking with a library other than NSubstitute
- `should-use-pytest`: Python tests not run by `pytest`
- `must-not-touch-production-dashboard-data`: a test that touches production port 8888 or removes or modifies production dashboard data

