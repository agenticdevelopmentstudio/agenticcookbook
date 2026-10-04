
- A `ViewModel` **MUST** expose read-only state — a `StateFlow<UiState>` (or `State<UiState>`), never the mutable backing field. Keep the `MutableStateFlow` private and expose the immutable upcast.
- Composables **MUST NOT** mutate hoisted state directly; they signal intent through event callbacks. This is `explicit-over-implicit` — every state change has a named, traceable entry point.
- Collect `StateFlow` with `collectAsStateWithLifecycle()` (from `lifecycle-runtime-compose`) so collection stops in the background — prefer it over `collectAsState()` on Android. Confirm the lifecycle-compose dependency is present.
- Model screen state as a single immutable `data class` or a `sealed interface` of cases (Loading / Success / Empty / Error). Immutable state aligns with `immutability-by-default` and removes a class of concurrency bugs.

```kotlin
class ProfileViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()
}
// In the composable:
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

