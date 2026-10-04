
Swift 6.2 (Xcode 26, 2025) ships an opt-in mode that reduces ceremony for single-threaded code. Behavior depends on settings — confirm what a target actually enables before assuming it.

- **Default actor isolation** — a target can default to `@MainActor` isolation (build setting / `defaultIsolation(MainActor.self)`), so app/UI code runs on the main actor without per-declaration annotations. This is intended for **app and executable targets**, NOT libraries — a library **SHOULD** leave default isolation `nonisolated` so callers stay in control.
- Enabling "Approachable Concurrency" toggles two upcoming features: `InferIsolatedConformances` (SE-0470) and `NonisolatedNonsendingByDefault` (SE-0461, async functions run in the caller's context). Enable each **individually** when migrating an existing project, because changing where async work runs can move code off the thread it ran on before.
- Use the `@concurrent` attribute to explicitly opt a function into running off the main actor.
- Treat any default-isolation choice as a **deliberate per-target decision**, not a global mandate; record it where the target is configured.

