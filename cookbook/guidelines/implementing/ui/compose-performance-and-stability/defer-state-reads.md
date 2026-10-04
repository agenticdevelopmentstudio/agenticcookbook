
- Read state as **late** as possible. Hoist the read into a lambda-based modifier so a value change triggers only layout/draw, not recomposition: `Modifier.offset { IntOffset(x, y) }`, `Modifier.graphicsLayer { alpha = a }`, `Modifier.drawBehind { ... }`.
- Pass **lambdas** instead of already-read values when the value changes frequently (e.g. scroll/animation): `Counter(count = { viewModel.count })` defers the read to the consumer.
- Use `derivedStateOf { ... }` when a frequently-changing state should drive UI only when a **computed** result crosses a threshold (e.g. `firstVisibleItemIndex > 0`). Do not use it for one-to-one transforms — that adds overhead with no benefit.

