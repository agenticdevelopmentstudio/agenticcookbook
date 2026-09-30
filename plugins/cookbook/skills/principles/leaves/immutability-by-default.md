<!-- leaf: principles/immutability-by-default · source: principles/immutability-by-default.md -->

# Immutability by default

Mutable shared state is the root cause of most concurrency bugs. Default to immutable values; introduce mutability only where necessary:

- Use `let` (Swift), `val` (Kotlin), `const` (JS/TS) by default
- Prefer value types (structs, data classes) over reference types
- Contain mutation behind clear boundaries (actors, StateFlow, useState)
