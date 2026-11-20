
- Event-driven work (button taps) **MUST** use `rememberCoroutineScope`, not `LaunchedEffect` — composition is not an event.
- Cleanup-bearing resources **MUST** use `DisposableEffect` with a non-empty `onDispose`; `LaunchedEffect` **MUST NOT** be used where teardown is required.
- `produceState` **SHOULD** be preferred over manually launching a coroutine that writes to a `mutableStateOf`.
- `derivedStateOf` is comparatively expensive and **SHOULD** be reserved for collapsing frequent state changes (e.g., scroll offset → boolean) into fewer recompositions — not for trivial combinations of state. Adopt it only when profiling shows wasted recompositions.
- Prefer hoisting state and side effects into the ViewModel where the work outlives composition; effect APIs are for work bound to the composable's lifetime.

