
- Pass the **narrowest** parameters a composable needs (e.g. `title: String`), not whole aggregate objects, so recomposition is scoped to what actually changed.
- Prefer **stable** types as parameters: immutable `data class`es, primitives, and lambdas. Unstable types (e.g. `var` fields, plain `List` whose runtime impl Compose can't prove immutable) can defeat recomposition skipping.
- Use Kotlin immutable collections (`kotlinx.collections.immutable`) or annotate types as `@Immutable` / `@Stable` only when the contract genuinely holds — a false stability annotation causes missed updates.
- Treat unnecessary recomposition as a **performance** concern, not a correctness one: make it work and right first, then measure with the Compose recomposition tooling before optimizing (`make-it-work-make-it-right-make-it-fast`).
- The Compose compiler enables **strong skipping** by default in current releases (Kotlin 2.x + the Compose compiler Gradle plugin), which skips composables even with some unstable parameters — but minimizing scope and preferring stable types remains the durable practice.

