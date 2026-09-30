<!-- leaf: implement-concurrency/swift6-strict-concurrency · source: guidelines/implementing/concurrency/swift6-strict-concurrency.md -->

**Rules** (cite as `implement-concurrency/swift6-strict-concurrency#<slug>`):

- `requirement` MUST — Any type that crosses an isolation boundary (closure capture, actor argument/return, Task value, async let) MUST be …
- `stored-properties-they-sendable-automatically-see-agenticdevelopercookbook` SHOULD — Prefer immutable value types (struct/enum with let Sendable stored properties) — they SHOULD be Sendable automatically; …
- `immutable-sendable-state-declare-sendable-conformance-explicitly` MAY — A final class with only immutable Sendable state MAY declare Sendable conformance explicitly.
- `guarantee-internal-locking-use-unchecked-sendable-but` MUST — A class whose safety the compiler cannot prove but that you guarantee (e.g. internal locking) MAY use @unchecked …
- `mutable-shared-state-wrapped-actor-retrofitted-unchecked` SHOULD — Mutable shared state SHOULD be wrapped in an actor, not retrofitted with @unchecked Sendable.
- `mainactor-ui-updates-run-main-actor` MUST — Annotate UI types and view models that touch UIKit/AppKit/SwiftUI state with @MainActor. UI updates MUST run on the …
- `function-nonisolated-not-access-actor-isolated-state` MUST — A function that is nonisolated MUST NOT access actor-isolated state synchronously.
- `strict-concurrency-adopted-incrementally-per-module` SHOULD — Strict concurrency SHOULD be adopted incrementally per module — a Swift 6 compiler still builds Swift 5 modules, so the …
- `default-actor-isolation` SHOULD — a target can default to @MainActor isolation (build setting / defaultIsolation(MainActor.self)), so app/UI code runs on …

# Adopt Swift 6 strict concurrency incrementally

The Swift 6 language mode turns data-race safety into a **compile-time** guarantee: the compiler statically rejects code that could race. Adopt it module by module so each isolation boundary is fixed in isolation rather than fighting the whole graph at once.

## Core model

- **Isolation domains** — code is isolated to an actor, to `@MainActor`, or is `nonisolated`. Crossing between domains is a boundary the compiler checks.
- **Sendable** — a type is safe to pass across an isolation boundary. Value types of `Sendable` members are inferred `Sendable`; reference types are not, unless made safe.
- **Requirement**: Any type that crosses an isolation boundary (closure capture, actor argument/return, `Task` value, `async let`) **MUST** be `Sendable`. The compiler enforces this in Swift 6 mode.

## Making types Sendable

- Prefer immutable value types (`struct`/`enum` with `let` `Sendable` stored properties) — they **SHOULD** be `Sendable` automatically; see `agenticdevelopercookbook://principles/immutability-by-default`.
- A `final class` with only immutable `Sendable` state **MAY** declare `Sendable` conformance explicitly.
- A class whose safety the compiler cannot prove but that you guarantee (e.g. internal locking) **MAY** use `@unchecked Sendable` — but this **MUST** be justified in a comment, and the class **MUST NOT** expose mutable state without synchronization.
- Mutable shared state **SHOULD** be wrapped in an `actor`, not retrofitted with `@unchecked Sendable`.

## Actor isolation and @MainActor

- Use `actor` to protect mutable state; its members are isolated and accessed with `await` from outside.
- Annotate UI types and view models that touch UIKit/AppKit/SwiftUI state with `@MainActor`. UI updates **MUST** run on the main actor.
- A function that is `nonisolated` **MUST NOT** access actor-isolated state synchronously.

## Incremental migration

- Strict concurrency **SHOULD** be adopted incrementally per module — a Swift 6 compiler still builds Swift 5 modules, so the strictness is opt-in per target.
- Recommended order (durable practice from the Swift migration guide):
  1. Enable checks as **warnings** first via the `StrictConcurrency` upcoming-feature flag (or the "Strict Concurrency Checking" build setting at `Targeted`, then `Complete`) while still in Swift 5 mode.
  2. Migrate **leaf modules first** (no dependents), then work upward; switch the **app target last**.
  3. Flip a module to the Swift 6 language mode only once its warnings are clear.
  4. Use `@preconcurrency` on imports/conformances to keep Swift-5 clients compiling against a not-yet-migrated dependency — treat it as a **temporary** shim, not a destination.
- Do not flip the whole workspace to Swift 6 mode at once; that produces an unactionable wall of errors.

## Swift 6.2 "Approachable Concurrency" (version-specific)

Swift 6.2 (Xcode 26, 2025) ships an opt-in mode that reduces ceremony for single-threaded code. Behavior depends on settings — confirm what a target actually enables before assuming it.

- **Default actor isolation** — a target can default to `@MainActor` isolation (build setting / `defaultIsolation(MainActor.self)`), so app/UI code runs on the main actor without per-declaration annotations. This is intended for **app and executable targets**, NOT libraries — a library **SHOULD** leave default isolation `nonisolated` so callers stay in control.
- Enabling "Approachable Concurrency" toggles two upcoming features: `InferIsolatedConformances` (SE-0470) and `NonisolatedNonsendingByDefault` (SE-0461, async functions run in the caller's context). Enable each **individually** when migrating an existing project, because changing where async work runs can move code off the thread it ran on before.
- Use the `@concurrent` attribute to explicitly opt a function into running off the main actor.
- Treat any default-isolation choice as a **deliberate per-target decision**, not a global mandate; record it where the target is configured.

## Verification

- Build each migrated module in Swift 6 language mode with zero concurrency warnings before moving up the graph.
- Grep for `@unchecked Sendable` and confirm each has a justifying comment and real synchronization.
