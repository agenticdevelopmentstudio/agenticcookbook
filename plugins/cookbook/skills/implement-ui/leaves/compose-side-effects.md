<!-- leaf: implement-ui/compose-side-effects · source: guidelines/implementing/ui/compose-side-effects.md -->

**Rules** (cite as `implement-ui/compose-side-effects#<slug>`):

- `so-side-effects-launched-through-compose-effect` MUST — A side effect is any change to state outside the scope of a composable function. Composition can run, re-run, and …
- `composable-function-side-effect-free-during` MUST — A composable function MUST be side-effect-free during composition. Network calls, observer registration, logging, and …
- `side-effects-launched-via-appropriate-effect` MUST — Side effects MUST be launched via the appropriate effect API, keyed to the inputs the effect reads.
- `keys-include-value-whose-change` MUST — Keys MUST include every value whose change should restart the effect. Values that should be read freshly but MUST NOT …
- `inside-effect-block-key-wrapped-rememberupdatedstate-there` MUST — Every mutable or immutable variable read inside the effect block MUST be a key, OR be wrapped in rememberUpdatedState. …
- `genuinely-lifecycle-scoped-still-wrap-latched-callbacks` MUST — LaunchedEffect(Unit) / LaunchedEffect(true) runs once per entry into composition; use it only when the effect is …
- `work-button-taps-use-remembercoroutinescope-launchedeffect-composition` MUST — Event-driven work (button taps) MUST use rememberCoroutineScope, not LaunchedEffect — composition is not an event.
- `cleanup-bearing-resources-use-disposableeffect-non-empty` MUST — Cleanup-bearing resources MUST use DisposableEffect with a non-empty onDispose; LaunchedEffect MUST NOT be used where …
- `producestate-preferred-over-manually-launching` SHOULD — produceState SHOULD be preferred over manually launching a coroutine that writes to a mutableStateOf.
- `derivedstateof-comparatively-expensive-reserved-collapsing-frequent-state` SHOULD — derivedStateOf is comparatively expensive and SHOULD be reserved for collapsing frequent state changes (e.g., scroll …

# Jetpack Compose side effects

A side effect is any change to state outside the scope of a composable function. Composition can run, re-run, and abandon at any time, so side effects MUST be launched through a Compose effect API keyed to their inputs — never inline in the composable body. Choosing the right API and the right keys is what separates a leak-free effect from one that restarts on every recomposition or captures stale values.

## Core rule

- A composable function **MUST** be side-effect-free during composition. Network calls, observer registration, logging, and mutation of external objects **MUST NOT** run directly in the body — they run on every recomposition, an unpredictable count.
- Side effects **MUST** be launched via the appropriate effect API, **keyed to the inputs the effect reads**.
- Keys **MUST** include every value whose change should restart the effect. Values that should be read freshly but **MUST NOT** restart the effect **MUST** be wrapped with `rememberUpdatedState`.

## API selection

| Need | Use | Keys |
|------|-----|------|
| Run a `suspend` block tied to composition lifecycle | `LaunchedEffect(key1, ...)` | inputs that should cancel + restart |
| Launch a coroutine in response to a UI event (callback, not composition) | `rememberCoroutineScope()` | none (scope cancels on leaving composition) |
| Register/acquire a resource needing cleanup | `DisposableEffect(key1, ...) { ...; onDispose { } }` | inputs that should re-run setup |
| Publish Compose state to non-Compose code after recomposition | `SideEffect { }` | none |
| Adapt a non-Compose async source (Flow/LiveData/callback) into `State` | `produceState(initial, key1, ...) { }` | inputs that should restart production |
| Convert observed `State` into a cold `Flow` | `snapshotFlow { }` | none |
| Reference a latest value without restarting an effect | `rememberUpdatedState(value)` | none |

## Keying discipline (the most common bug)

- Every mutable or immutable variable read inside the effect block **MUST** be a key, OR be wrapped in `rememberUpdatedState`. There is no third option.
- **Too few keys** → the effect captures stale values and silently misbehaves.
- **Too many keys** → the effect cancels and restarts needlessly (dropped coroutines, re-registered observers, flicker).
- `LaunchedEffect(Unit)` / `LaunchedEffect(true)` runs once per entry into composition; use it **only** when the effect is genuinely lifecycle-scoped, and **MUST** still wrap latched callbacks in `rememberUpdatedState`.

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

## MUST / MUST NOT

- Event-driven work (button taps) **MUST** use `rememberCoroutineScope`, not `LaunchedEffect` — composition is not an event.
- Cleanup-bearing resources **MUST** use `DisposableEffect` with a non-empty `onDispose`; `LaunchedEffect` **MUST NOT** be used where teardown is required.
- `produceState` **SHOULD** be preferred over manually launching a coroutine that writes to a `mutableStateOf`.
- `derivedStateOf` is comparatively expensive and **SHOULD** be reserved for collapsing frequent state changes (e.g., scroll offset → boolean) into fewer recompositions — not for trivial combinations of state. Adopt it only when profiling shows wasted recompositions.
- Prefer hoisting state and side effects into the ViewModel where the work outlives composition; effect APIs are for work bound to the composable's lifetime.
