
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

