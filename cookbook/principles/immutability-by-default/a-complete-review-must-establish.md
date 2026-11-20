
- `should-default-to-immutable-values`: whether every piece of mutable state introduced is necessary
- `should-use-immutable-bindings-by-default`: whether bindings use `let` (Swift), `val` (Kotlin), `const` (JS/TS) unless they must be reassigned
- `should-prefer-value-types`: whether value types (structs, data classes) are used over reference types where they serve
- `should-contain-mutation-behind-boundaries`: whether every mutation is contained behind a clear boundary (actors, StateFlow, useState)
- `should-use-immutable-bindings-by-default`: No `var`/`var` declarations where `let`/`val` would suffice;
- `should-contain-mutation-behind-boundaries`: mutable state confined to a single owner (actor, ViewModel, store);
- `must-not-access-shared-mutable-state-unsynchronized`: no shared mutable state across concurrent contexts;
- `should-prefer-value-types`: data classes or structs used for domain models
