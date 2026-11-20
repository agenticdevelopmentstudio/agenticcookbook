
- `should-default-to-immutable-values`: whether every piece of mutable state introduced is necessary
- `should-use-immutable-bindings-by-default`: whether bindings use `let` (Swift), `val` (Kotlin), `const` (JS/TS) unless they must be reassigned
- `should-prefer-value-types`: whether value types (structs, data classes) are used over reference types where they serve
- `should-contain-mutation-behind-boundaries`: whether every mutation is contained behind a clear boundary (actors, StateFlow, useState)
