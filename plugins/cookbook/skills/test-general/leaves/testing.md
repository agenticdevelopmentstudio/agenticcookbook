<!-- leaf: test-general/testing · source: guidelines/testing/testing.md -->

**Rules** (cite as `test-general/testing#<slug>`):

- `round-trips-implementation-include-corresponding-test-file` MUST — Prioritize unit tests over integration tests. Test state transitions, edge cases, serialization round-trips. Every …
- `change-have-tests-bug-fix` MUST — Every change MUST have tests. Every bug fix MUST have a regression test. Unit tests SHOULD be prioritized over …
- `production-dashboard-data-not-removed-modified-during-testing` MUST — Production dashboard data MUST NOT be removed or modified during testing — use demo port 9888, not production port 8888.

# Comprehensive unit testing

Prioritize unit tests over integration tests. Test state transitions, edge cases, serialization round-trips. Every implementation MUST include a corresponding test file. UI tests are fragile — prefer testing component logic as unit tests.

---

# Testing

Every change MUST have tests. Every bug fix MUST have a regression test. Unit tests SHOULD be prioritized over integration tests. Test state transitions, edge cases, and serialization round-trips. UI tests are fragile — prefer testing component logic as unit tests.

## TypeScript

Use [Playwright](https://playwright.dev/) for end-to-end and visual regression testing. Screenshot comparison for snapshot tests. Use Storybook for component catalog and visual tests where applicable.

## C#

1. [xUnit](https://xunit.net/) with `[Fact]` for single tests and `[Theory]`/`[InlineData]` for parameterized tests.
2. [FluentAssertions](https://fluentassertions.com/) for readable assertions.
3. [NSubstitute](https://nsubstitute.github.io/) for mocking.
4. Every change needs tests. Every bug fix needs a regression test.
5. Prioritize unit tests over integration tests.

```csharp
[Fact]
public void ParseOrder_WithValidInput_ReturnsOrder()
{
    var result = OrderParser.Parse(validJson);
    result.Should().NotBeNull();
    result.OrderId.Should().Be("ORD-123");
}

[Theory]
[InlineData("", false)]
[InlineData("valid@email.com", true)]
[InlineData("no-at-sign", false)]
public void IsValidEmail_ReturnsExpected(string input, bool expected)
{
    EmailValidator.IsValid(input).Should().Be(expected);
}
```

## Python

1. Use `pytest` for all tests.
2. Every change needs tests. Every bug fix needs a regression test.
3. Prioritize unit tests over integration tests.
4. Production dashboard data MUST NOT be removed or modified during testing — use demo port 9888, not production port 8888.
