
- **must-enable-nullable**: All projects MUST enable `<Nullable>enable</Nullable>`.
- **should-treat-nullable-warnings-as-design-signals**: SHOULD treat warnings as design signals — `string` means non-null, `string?` means nullable.
- **should-not-use-null-forgiving-operator**: The null-forgiving operator (`!`) SHOULD NOT be used — prefer `?? throw` or guard clauses.
- **should-use-required-for-non-null-init**: SHOULD use `required` properties and constructor parameters for non-null initialization.
- **should-annotate-contracts-compiler-cannot-infer**: SHOULD use `[NotNull]`, `[MaybeNull]`, `[NotNullWhen]` from `System.Diagnostics.CodeAnalysis` for contracts the compiler cannot infer.
