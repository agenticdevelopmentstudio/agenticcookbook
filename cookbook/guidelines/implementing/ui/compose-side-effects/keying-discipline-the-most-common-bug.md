
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
