
# Nullable Reference Types

All projects MUST enable `<Nullable>enable</Nullable>`. Treat warnings as design signals — `string` means non-null, `string?` means nullable.

- The null-forgiving operator (`!`) SHOULD NOT be used — prefer `?? throw` or guard clauses
- Use `required` properties and constructor parameters for non-null initialization
- Use `[NotNull]`, `[MaybeNull]`, `[NotNullWhen]` from `System.Diagnostics.CodeAnalysis` for contracts the compiler cannot infer

```csharp
// Good: required + guard clause
public required string Name { get; init; }

public void Process(string? input)
{
    ArgumentNullException.ThrowIfNull(input);
    // input is now non-null
}
```

