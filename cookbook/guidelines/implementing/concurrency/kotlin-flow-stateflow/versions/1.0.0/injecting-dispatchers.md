
- Code that switches threads **SHOULD** receive its dispatchers via constructor injection, not reference `Dispatchers.IO` / `Dispatchers.Default` directly. Hardcoded dispatchers cannot be swapped for a test dispatcher, making suspend logic flaky or untestable.

```kotlin
class ItemRepository(private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) {
    suspend fun load() = withContext(ioDispatcher) { /* blocking I/O */ }
}
```

- In tests, inject `StandardTestDispatcher` / `UnconfinedTestDispatcher` and drive virtual time with `runTest`.
- A `StateFlow` built with `WhileSubscribed` only starts its upstream when collected: tests **MUST** keep at least one active collector (e.g. collect into a job) or `value` stays at `initialValue`.

