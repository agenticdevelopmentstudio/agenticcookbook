<!-- leaf: implement-ui/compose-performance-and-stability · source: guidelines/implementing/ui/compose-performance-and-stability.md -->

**Rules** (cite as `implement-ui/compose-performance-and-stability#<slug>`):

- `intuition-ui-state-stable-state-reads-deferred` SHOULD — Compose performance is dominated by recomposition cost. Make UI state stable, defer state reads, and let the compiler …
- `lazyrow-lazyverticalgrid-you-supply-stable-key-per` MUST — In LazyColumn/LazyRow/LazyVerticalGrid, you MUST supply a stable key per item (items(list, key = { it.id })) so …

# Jetpack Compose performance and stability

Compose performance is dominated by recomposition cost. Make UI state stable, defer state reads, and let the compiler skip unchanged composables — then verify with measurement, never intuition. UI state SHOULD be stable and state reads SHOULD be deferred so the runtime can skip unnecessary recomposition.

## Stability and skipping

- Composable parameters of **stable** types let the runtime skip recomposition when values are unchanged. The compiler infers stability for primitives, `String`, function types, and types whose public reads are all stable `val`/`State`.
- Pass **immutable** data into composables. Prefer `val` over `var`, `kotlinx.collections.immutable` (`ImmutableList`/`PersistentList`) over `List`, and data classes whose properties are themselves stable.
- **Strong-skipping mode** is enabled by default in current Compose (Kotlin 2.0.20+). It lets the runtime skip composables with *unstable* parameters by comparing those parameters with referential equality (`===`), and auto-remembers lambdas. NOTE: strong skipping does **not** make a type stable — passing a fresh `ArrayList` instance each recomposition still defeats skipping. Prefer genuinely stable inputs.
- Annotate `@Immutable` (deeply unchanging) or `@Stable` (changes only via `State`) **only** when the type is truly so and the compiler cannot infer it (e.g., a type from a module without the Compose compiler, or one using an interface field). A false annotation causes missed recompositions and stale UI — do not annotate to silence the compiler.

## Defer state reads

- Read state as **late** as possible. Hoist the read into a lambda-based modifier so a value change triggers only layout/draw, not recomposition: `Modifier.offset { IntOffset(x, y) }`, `Modifier.graphicsLayer { alpha = a }`, `Modifier.drawBehind { ... }`.
- Pass **lambdas** instead of already-read values when the value changes frequently (e.g. scroll/animation): `Counter(count = { viewModel.count })` defers the read to the consumer.
- Use `derivedStateOf { ... }` when a frequently-changing state should drive UI only when a **computed** result crosses a threshold (e.g. `firstVisibleItemIndex > 0`). Do not use it for one-to-one transforms — that adds overhead with no benefit.

## Avoid wasted work

- `remember(keys) { expensive() }` to cache costly computation across recompositions; recompute only when a key changes. `remember(items, query) { items.filter(...) }` keys derived results to inputs.
- In `LazyColumn`/`LazyRow`/`LazyVerticalGrid`, you **MUST** supply a stable `key` per item (`items(list, key = { it.id })`) so reorders and insertions reuse state instead of recomposing the whole list.
- Do **NOT** perform backwards writes — never write to a state value that the same composable already read; this loops recomposition. Keep composables side-effect free and idempotent.
- Avoid allocating new collections, lambdas-with-captures, or objects in the composable body on every call; hoist or `remember` them.

## Measure (release builds only)

- Profile **release** builds with R8 enabled and a **Baseline Profile** applied. Debug builds run unoptimized Compose and produce misleading numbers — never tune against them.
- Use **Layout Inspector** recomposition counts to find composables recomposing more than expected; a high count signals an unstable parameter or an un-deferred read. The Compose compiler can also emit stability metrics/reports to identify unstable parameters.
- For regression gates, use Macrobenchmark (frame timing, `recompositionCount`) on representative journeys. Optimize a hotspot **only** after a measurement justifies it (per make-it-work-make-it-right-make-it-fast); do not pre-optimize composables that are not hot.
