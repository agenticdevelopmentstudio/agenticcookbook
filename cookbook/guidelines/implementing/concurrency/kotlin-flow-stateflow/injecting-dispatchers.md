
```kotlin
class ItemRepository(private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) {
    suspend fun load() = withContext(ioDispatcher) { /* blocking I/O */ }
}
```
