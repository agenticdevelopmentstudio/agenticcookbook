
- `must-enable-nullable`: every `.csproj` the build touches sets `<Nullable>enable</Nullable>`
- `should-treat-nullable-warnings-as-design-signals`: the build compiles with no nullable warning left unanswered, or the code says why not
- `should-not-use-null-forgiving-operator`: the build adds no `!` null-forgiving operator, or the code says why not
- `should-use-required-for-non-null-init`: every non-null member the build adds is set through `required` or a constructor parameter, or the code says why not
- `should-annotate-contracts-compiler-cannot-infer`: every null contract the build adds that the compiler cannot infer is annotated with `[NotNull]`, `[MaybeNull]` or `[NotNullWhen]`, or the code says why not
- `should-throw-if-null-at-entry-points`: `ArgumentNullException.ThrowIfNull` is used at entry points
