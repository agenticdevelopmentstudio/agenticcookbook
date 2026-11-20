
Swift 6.2 (Xcode 26, 2025) ships an opt-in mode that reduces ceremony for single-threaded code. Behavior depends on settings.

- **Default actor isolation** — a target can default to `@MainActor` isolation (build setting / `defaultIsolation(MainActor.self)`), so app/UI code runs on the main actor without per-declaration annotations.
- Enabling "Approachable Concurrency" toggles two upcoming features: `InferIsolatedConformances` (SE-0470) and `NonisolatedNonsendingByDefault` (SE-0461, async functions run in the caller's context).
