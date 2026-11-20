
- **Compose**: `collectAsStateWithLifecycle()`. It collects only while the lifecycle is at least `STARTED`.

```kotlin
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

- **Views / Fragments / Activities**: `repeatOnLifecycle(Lifecycle.State.STARTED)`. The block is launched on each `STARTED` and cancelled on `STOPPED`.

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```
