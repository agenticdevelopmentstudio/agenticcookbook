
- `must-enable-nullable`: a project file without `<Nullable>enable</Nullable>`, or with it disabled
- `should-treat-nullable-warnings-as-design-signals`: nullable warnings suppressed or ignored rather than answered by fixing the type (`string` versus `string?`)
- `should-not-use-null-forgiving-operator`: any `!` null-forgiving operator where `?? throw` or a guard clause would do
- `should-use-required-for-non-null-init`: a non-null property or field initialized by convention instead of a `required` property or constructor parameter
- `should-annotate-contracts-compiler-cannot-infer`: a null contract the compiler cannot infer (a try-pattern out parameter, a helper that throws on null) left without `[NotNull]`, `[MaybeNull]` or `[NotNullWhen]`
- `should-throw-if-null-at-entry-points`: an entry point that does not call `ArgumentNullException.ThrowIfNull` on its reference arguments
