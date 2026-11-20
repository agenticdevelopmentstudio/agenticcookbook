
```kotlin
val uiState: StateFlow<UiState> = repository.items
    .map { items -> UiState(items) }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = UiState.Loading,
    )
```
