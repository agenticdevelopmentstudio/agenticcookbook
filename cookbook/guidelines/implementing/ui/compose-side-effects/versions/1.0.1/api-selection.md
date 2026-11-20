
| Need | Use | Keys |
|------|-----|------|
| Run a `suspend` block tied to composition lifecycle | `LaunchedEffect(key1, ...)` | inputs that should cancel + restart |
| Launch a coroutine in response to a UI event (callback, not composition) | `rememberCoroutineScope()` | none (scope cancels on leaving composition) |
| Register/acquire a resource needing cleanup | `DisposableEffect(key1, ...) { ...; onDispose { } }` | inputs that should re-run setup |
| Publish Compose state to non-Compose code after recomposition | `SideEffect { }` | none |
| Adapt a non-Compose async source (Flow/LiveData/callback) into `State` | `produceState(initial, key1, ...) { }` | inputs that should restart production |
| Convert observed `State` into a cold `Flow` | `snapshotFlow { }` | none |
| Reference a latest value without restarting an effect | `rememberUpdatedState(value)` | none |

