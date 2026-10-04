
- **Isolation domains** — code is isolated to an actor, to `@MainActor`, or is `nonisolated`. Crossing between domains is a boundary the compiler checks.
- **Sendable** — a type is safe to pass across an isolation boundary. Value types of `Sendable` members are inferred `Sendable`; reference types are not, unless made safe.
- **Requirement**: Any type that crosses an isolation boundary (closure capture, actor argument/return, `Task` value, `async let`) **MUST** be `Sendable`. The compiler enforces this in Swift 6 mode.

