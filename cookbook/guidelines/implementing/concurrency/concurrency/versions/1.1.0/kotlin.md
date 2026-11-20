
Kotlin Coroutines: I/O on `Dispatchers.IO` inside `viewModelScope`, back on the main dispatcher to update the UI.

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val result = repository.fetch()
    withContext(Dispatchers.Main) { updateUi(result) }
}
```
