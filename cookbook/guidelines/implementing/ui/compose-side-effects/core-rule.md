
- A composable function **MUST** be side-effect-free during composition. Network calls, observer registration, logging, and mutation of external objects **MUST NOT** run directly in the body — they run on every recomposition, an unpredictable count.
- Side effects **MUST** be launched via the appropriate effect API, **keyed to the inputs the effect reads**.
- Keys **MUST** include every value whose change should restart the effect. Values that should be read freshly but **MUST NOT** restart the effect **MUST** be wrapped with `rememberUpdatedState`.

