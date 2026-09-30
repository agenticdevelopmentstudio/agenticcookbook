<!-- leaf: implement-ui/compose-state-and-udf · source: guidelines/implementing/ui/compose-state-and-udf.md -->

**Rules** (cite as `implement-ui/compose-state-and-udf#<slug>`):

- `reusable-composable-stateless-takes-state-via` SHOULD — A reusable composable SHOULD be stateless: it takes its state via parameters and emits changes via callback lambdas. …
- `state-hoisted-lowest-common-ancestor` MUST — State MUST be hoisted to the lowest common ancestor that reads or writes it — no higher. Hoisting too high causes …
- `form-submission-status-live-viewmodel-composition-so` SHOULD — Screen-level / business state (data loaded from repositories, navigation results, form submission status) SHOULD live …
- `text-field-cursor-stay-composition-via-remember` MAY — Pure UI element state (scroll position, expanded/collapsed, focus, text-field cursor) MAY stay in composition via …
- `use-remembersaveable-state-survive-rotation-process-death` SHOULD — Use rememberSaveable for state that SHOULD survive rotation or process death (entered text, selected tab) when it does …
- `values-stored-remembersaveable-bundle-serializable-supplied-custom` MUST — Values stored in rememberSaveable MUST be Bundle-serializable or supplied with a custom Saver.
- `remember-not-relied-across-configuration-changes` MUST — remember MUST NOT be relied on across configuration changes — it is cleared when the composable leaves composition.
- `viewmodel-expose-read-only-state` MUST — A ViewModel MUST expose read-only state — a StateFlow<UiState> (or State<UiState>), never the mutable backing field. …
- `composables-not-mutate-hoisted-state-directly` MUST — Composables MUST NOT mutate hoisted state directly; they signal intent through event callbacks. This is …

# Jetpack Compose: state hoisting and unidirectional data flow

In Jetpack Compose, **state flows down and events flow up** (unidirectional data flow, UDF). Hoist state out of composables to the lowest common owner that needs it — or to a `ViewModel` for screen-level state — and keep individual composables stateless where practical. This is the most stable consensus in modern Android UI and the foundation every other Compose decision rests on.

## Hoist state

State hoisting moves state up to a caller, making a composable stateless. A hoisted state-holder pattern replaces a state value with a `value` parameter (flows down) and an `onValueChange` lambda (flows up).

- A reusable composable **SHOULD** be stateless: it takes its state via parameters and emits changes via callback lambdas. This advances `separation-of-concerns` — rendering is decoupled from state ownership.
- State **MUST** be hoisted to the **lowest common ancestor** that reads or writes it — no higher. Hoisting too high causes unnecessary recomposition and couples unrelated subtrees; hoisting too low blocks sharing.
- Screen-level / business state (data loaded from repositories, navigation results, form submission status) **SHOULD** live in a `ViewModel`, not in composition, so it survives configuration changes and process-death restoration.
- Pure UI element state (scroll position, expanded/collapsed, focus, text-field cursor) **MAY** stay in composition via `remember` when no other component needs it.

```kotlin
// Stateless: state down, events up
@Composable
fun NameField(name: String, onNameChange: (String) -> Unit) {
    OutlinedTextField(value = name, onValueChange = onNameChange, label = { Text("Name") })
}
```

## remember vs rememberSaveable

| API | Survives recomposition | Survives config change / process death | Use for |
|-----|------------------------|----------------------------------------|---------|
| `remember { ... }` | Yes | No | Transient UI state recomputable on the spot |
| `rememberSaveable { ... }` | Yes | Yes (via saved-instance `Bundle`) | UI state a user would be annoyed to lose on rotation |

- Use `rememberSaveable` for state that **SHOULD** survive rotation or process death (entered text, selected tab) when it does not belong in a `ViewModel`.
- Values stored in `rememberSaveable` **MUST** be `Bundle`-serializable or supplied with a custom `Saver`.
- `remember` **MUST NOT** be relied on across configuration changes — it is cleared when the composable leaves composition.

## Expose immutable UI state

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

## Recomposition and stability awareness

- Pass the **narrowest** parameters a composable needs (e.g. `title: String`), not whole aggregate objects, so recomposition is scoped to what actually changed.
- Prefer **stable** types as parameters: immutable `data class`es, primitives, and lambdas. Unstable types (e.g. `var` fields, plain `List` whose runtime impl Compose can't prove immutable) can defeat recomposition skipping.
- Use Kotlin immutable collections (`kotlinx.collections.immutable`) or annotate types as `@Immutable` / `@Stable` only when the contract genuinely holds — a false stability annotation causes missed updates.
- Treat unnecessary recomposition as a **performance** concern, not a correctness one: make it work and right first, then measure with the Compose recomposition tooling before optimizing (`make-it-work-make-it-right-make-it-fast`).
- The Compose compiler enables **strong skipping** by default in current releases (Kotlin 2.x + the Compose compiler Gradle plugin), which skips composables even with some unstable parameters — but minimizing scope and preferring stable types remains the durable practice.
