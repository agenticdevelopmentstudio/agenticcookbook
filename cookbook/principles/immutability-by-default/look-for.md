
- `should-default-to-immutable-values`: mutable state introduced where an immutable value would do
- `should-use-immutable-bindings-by-default`: `var` or `let` (JS/TS) bindings that are never reassigned
- `should-prefer-value-types`: a reference type used where a value type (struct, data class) would serve
- `should-contain-mutation-behind-boundaries`: shared state mutated from many places rather than behind a clear boundary (actor, StateFlow, useState)
- `must-not-share-mutable-state-across-concurrent-contexts`: mutable state shared across concurrent contexts
