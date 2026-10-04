
- `remember(keys) { expensive() }` to cache costly computation across recompositions; recompute only when a key changes. `remember(items, query) { items.filter(...) }` keys derived results to inputs.
- In `LazyColumn`/`LazyRow`/`LazyVerticalGrid`, you **MUST** supply a stable `key` per item (`items(list, key = { it.id })`) so reorders and insertions reuse state instead of recomposing the whole list.
- Do **NOT** perform backwards writes — never write to a state value that the same composable already read; this loops recomposition. Keep composables side-effect free and idempotent.
- Avoid allocating new collections, lambdas-with-captures, or objects in the composable body on every call; hoist or `remember` them.

