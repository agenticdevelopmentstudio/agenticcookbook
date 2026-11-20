
Use Kotlin Coroutines for all async work. Run I/O on `Dispatchers.IO`. Use `viewModelScope` for ViewModel-scoped coroutines. Never block the main thread.

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val result = repository.fetch()
    withContext(Dispatchers.Main) { updateUi(result) }
}
```

