
- Every mutable or immutable variable read inside the effect block **MUST** be a key, OR be wrapped in `rememberUpdatedState`. There is no third option.
- **Too few keys** → the effect captures stale values and silently misbehaves.
- **Too many keys** → the effect cancels and restarts needlessly (dropped coroutines, re-registered observers, flicker).
- `LaunchedEffect(Unit)` / `LaunchedEffect(true)` runs once per entry into composition; use it **only** when the effect is genuinely lifecycle-scoped, and **MUST** still wrap latched callbacks in `rememberUpdatedState`.

```kotlin
// Long-lived effect: key on lifecycleOwner; wrap callbacks so they don't restart it.
val currentOnEnter by rememberUpdatedState(onEnter)
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, e ->
        if (e == Lifecycle.Event.ON_START) currentOnEnter()
    }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
}
```

