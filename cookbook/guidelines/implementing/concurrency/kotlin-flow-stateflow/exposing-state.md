
- The ViewModel **MUST** expose read-only `StateFlow<UiState>` (or `SharedFlow` for one-shot events), never a mutable `MutableStateFlow` directly. Back it with a private `MutableStateFlow` and expose `.asStateFlow()`.
- When deriving state from a cold upstream (Room, DataStore, repository flow), you **SHOULD** convert with `stateIn(scope, started, initialValue)` rather than manually collecting into a `MutableStateFlow`. `stateIn` gives the production pipeline lifecycle control tied to subscription.
- The `started` policy **SHOULD** be `SharingStarted.WhileSubscribed(5_000)`. The 5-second stop timeout keeps the upstream alive across configuration changes and short app-switches while still tearing it down when the UI is truly gone.

```kotlin
val uiState: StateFlow<UiState> = repository.items
    .map { items -> UiState(items) }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = UiState.Loading,
    )
```

- `initialValue` **MUST** be a real renderable state (e.g. `Loading`), because `StateFlow.value` is read synchronously before the upstream emits.

### Choosing a SharingStarted policy

| Policy | When to use |
|--------|-------------|
| `WhileSubscribed(5_000)` | Default for UI state — stops upstream shortly after UI stops collecting. |
| `Eagerly` | Pipeline must run for the ViewModel's whole life regardless of subscribers (rare). |
| `Lazily` | Start on first subscriber, never stop. Use only when restart cost is unacceptable. |

