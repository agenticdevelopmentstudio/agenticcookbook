
- `must-enable-nullable`: every project enables `<Nullable>enable</Nullable>`
- `should-treat-nullable-warnings-as-design-signals`: every nullable warning is answered in the type design, or the code says why not
- `should-not-use-null-forgiving-operator`: no `!` is used where `?? throw` or a guard clause would serve, or the code says why not
- `should-use-required-for-non-null-init`: non-null members are initialized through `required` properties or constructor parameters, or the code says why not
- `should-annotate-contracts-compiler-cannot-infer`: every null contract the compiler cannot infer carries the matching `System.Diagnostics.CodeAnalysis` attribute, or the code says why not
- `should-throw-if-null-at-entry-points`: `ArgumentNullException.ThrowIfNull` used at entry points;
