
- **should-default-to-immutable-values**: Values SHOULD be immutable by default; mutability SHOULD be introduced only where necessary.
- **should-use-immutable-bindings-by-default**: `let` (Swift), `val` (Kotlin), `const` (JS/TS) SHOULD be used by default.
- **should-prefer-value-types**: SHOULD prefer value types (structs, data classes) over reference types.
- **should-contain-mutation-behind-boundaries**: Mutation SHOULD be contained behind clear boundaries (actors, StateFlow, useState).
