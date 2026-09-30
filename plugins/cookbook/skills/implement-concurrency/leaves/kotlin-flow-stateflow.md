<!-- leaf: implement-concurrency/kotlin-flow-stateflow · source: guidelines/implementing/concurrency/kotlin-flow-stateflow.md -->

**Rules** (cite as `implement-concurrency/kotlin-flow-stateflow#<slug>`):

- `viewmodel-expose-read-only-stateflow` MUST — The ViewModel MUST expose read-only StateFlow<UiState> (or SharedFlow for one-shot events), never a mutable …
- `repository-flow-you-convert-statein-scope-started` SHOULD — When deriving state from a cold upstream (Room, DataStore, repository flow), you SHOULD convert with stateIn(scope, …
- `started-policy-sharingstarted-whilesubscribed-000-second` SHOULD — The started policy SHOULD be SharingStarted.WhileSubscribed(5_000). The 5-second stop timeout keeps the upstream alive …
- `initialvalue-real-renderable-state-loading` MUST — initialValue MUST be a real renderable state (e.g. Loading), because StateFlow.value is read synchronously before the …
- `livedata-observe-you-collect-lifecycle-aware-way` MUST — Collecting a StateFlow does NOT auto-stop when the UI goes to the background — unlike LiveData.observe(). You MUST …
- `must-not` MUST — use bare collectAsState() for ViewModel flows in lifecycle-bound UI. It collects regardless of lifecycle state, wasting …
- `must-not-2` MUST — use lifecycleScope.launchWhenStarted / launchWhenResumed / whenStarted. These are deprecated (androidx.lifecycle 2.4+): …
- `must-not-3` MUST — collect a flow directly in lifecycleScope.launch { ... } without repeatOnLifecycle; that collects through the …
- `code-switches-threads-receive-dispatchers-via-constructor` SHOULD — Code that switches threads SHOULD receive its dispatchers via constructor injection, not reference Dispatchers.IO / …
- `upstream-collected-tests-keep-least-one-active` MUST — A StateFlow built with WhileSubscribed only starts its upstream when collected: tests MUST keep at least one active …

# Kotlin Flow and StateFlow: lifecycle-aware state exposure

`StateFlow` is the durable way to expose observable UI state from a ViewModel: a hot, always-has-a-value flow. The two failure modes are leaking work into the background (non-lifecycle-aware collection) and untestable code (hardcoded dispatchers). This guideline encodes the patterns that avoid both, current as of androidx.lifecycle 2.8+ (2024–2026).

## Exposing state

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

## Collecting lifecycle-aware (the critical part)

Collecting a `StateFlow` does NOT auto-stop when the UI goes to the background — unlike `LiveData.observe()`. You **MUST** collect in a lifecycle-aware way or the collector keeps running (and keeps `WhileSubscribed` upstream alive) while the screen is invisible.

- **Compose**: use `collectAsStateWithLifecycle()` (from `androidx.lifecycle:lifecycle-runtime-compose`). It collects only while the lifecycle is at least `STARTED`.

```kotlin
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

- **Views / Fragments / Activities**: collect inside `repeatOnLifecycle(Lifecycle.State.STARTED)` from `lifecycleScope`. The block is launched on each `STARTED` and cancelled on `STOPPED`.

```kotlin
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
```

### Anti-patterns — flag and fix

- **MUST NOT** use bare `collectAsState()` for ViewModel flows in lifecycle-bound UI. It collects regardless of lifecycle state, wasting CPU/network/battery while backgrounded. Replace with `collectAsStateWithLifecycle()`.
- **MUST NOT** use `lifecycleScope.launchWhenStarted` / `launchWhenResumed` / `whenStarted`. These are deprecated (androidx.lifecycle 2.4+): the pausing dispatcher suspends the coroutine but leaves upstream resources allocated. Replace with `repeatOnLifecycle`.
- **MUST NOT** collect a flow directly in `lifecycleScope.launch { ... }` without `repeatOnLifecycle`; that collects through the backgrounded state.

## Injecting dispatchers

- Code that switches threads **SHOULD** receive its dispatchers via constructor injection, not reference `Dispatchers.IO` / `Dispatchers.Default` directly. Hardcoded dispatchers cannot be swapped for a test dispatcher, making suspend logic flaky or untestable.

```kotlin
class ItemRepository(private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) {
    suspend fun load() = withContext(ioDispatcher) { /* blocking I/O */ }
}
```

- In tests, inject `StandardTestDispatcher` / `UnconfinedTestDispatcher` and drive virtual time with `runTest`.
- A `StateFlow` built with `WhileSubscribed` only starts its upstream when collected: tests **MUST** keep at least one active collector (e.g. collect into a job) or `value` stays at `initialValue`.
