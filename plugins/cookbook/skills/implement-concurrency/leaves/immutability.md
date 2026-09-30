<!-- leaf: implement-concurrency/immutability · source: guidelines/implementing/concurrency/immutability.md -->

**Rules** (cite as `implement-concurrency/immutability#<slug>`):

- `bugs-immutable-values-default-introduce-mutability-only` MUST — Mutable shared state is the root cause of most concurrency bugs. Immutable values MUST be the default; introduce …

# Immutability

Mutable shared state is the root cause of most concurrency bugs. Immutable values MUST be the default; introduce mutability only where necessary. Value types SHOULD be preferred over reference types. Mutation MUST be contained behind clear boundaries.

## Kotlin

Use `val` by default. Use `data class` for value types. Introduce `var` only when mutation is required, and contain mutable state behind `StateFlow`.

## TypeScript

Use `const` by default. Use `var`/`let` only when mutation is required. Prefer `useState` (React) for contained mutable state.

## C#

Use `readonly` fields and `readonly struct` by default. Introduce mutability only when required.

- Prefer `System.Collections.Immutable` (`ImmutableList<T>`, `ImmutableDictionary<K,V>`) for shared collections
- Use `record` for DTOs, API responses, domain events, value objects
- Use `record struct` / `readonly record struct` for small immutable value types
- Prefer positional records (`record Person(string Name, int Age)`) for simple data carriers
- Use `init` setters and `required` keyword for mandatory properties
- Use `with` expressions for non-destructive mutation
- Contain mutable state behind `ObservableObject` (UI) or thread-safe wrappers
- Reserve `class` with mutable state for entities with identity semantics

```csharp
// Immutable DTO
public record OrderSummary(string OrderId, decimal Total, DateTime CreatedAt);

// Modified copy
var updated = order with { Total = 99.99m };

// Readonly value type
public readonly record struct Point(double X, double Y);
```
