
- `should-default-to-immutable-values`: values are immutable by default and each mutable one is necessary, or the work says why
- `should-use-immutable-bindings-by-default`: every binding is `let` (Swift), `val` (Kotlin) or `const` (JS/TS) unless it is reassigned, or the work says why not
- `should-prefer-value-types`: value types (structs, data classes) are used over reference types, or the work says why a reference type is needed
- `should-contain-mutation-behind-boundaries`: every mutation of shared state happens behind a clear boundary (actors, StateFlow, useState), or the work says why not
- `must-not-access-shared-mutable-state-unsynchronized`: no mutable state shared across concurrent contexts is accessed without synchronization or an owning actor
