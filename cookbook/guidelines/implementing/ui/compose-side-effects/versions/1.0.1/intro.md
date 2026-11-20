
# Jetpack Compose side effects

A side effect is any change to state outside the scope of a composable function. Composition can run, re-run, and abandon at any time, so side effects MUST be launched through a Compose effect API keyed to their inputs — never inline in the composable body. Choosing the right API and the right keys is what separates a leak-free effect from one that restarts on every recomposition or captures stale values.

