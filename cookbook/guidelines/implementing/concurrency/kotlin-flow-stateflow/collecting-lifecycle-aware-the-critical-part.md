
Collecting a `StateFlow` does NOT auto-stop when the UI goes to the background — unlike `LiveData.observe()`. You **MUST** collect in a lifecycle-aware way or the collector keeps running (and keeps `WhileSubscribed` upstream alive) while the screen is invisible.

- **Compose**: use `collectAsStateWithLifecycle()` (from `androidx.lifecycle:lifecycle-runtime-compose`). It collects only while the lifecycle is at least `STARTED`.

```kotlin
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

- **Views / Fragments / Activities**: collect inside `repeatOnLifecycle(Lifecycle.State.STARTED)` from `lifecycleScope`. The block is launched on each `STARTED` and cancelled on `STOPPED`.

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

### Anti-patterns — flag and fix

- **MUST NOT** use bare `collectAsState()` for ViewModel flows in lifecycle-bound UI. It collects regardless of lifecycle state, wasting CPU/network/battery while backgrounded. Replace with `collectAsStateWithLifecycle()`.
- **MUST NOT** use `lifecycleScope.launchWhenStarted` / `launchWhenResumed` / `whenStarted`. These are deprecated (androidx.lifecycle 2.4+): the pausing dispatcher suspends the coroutine but leaves upstream resources allocated. Replace with `repeatOnLifecycle`.
- **MUST NOT** collect a flow directly in `lifecycleScope.launch { ... }` without `repeatOnLifecycle`; that collects through the backgrounded state.

