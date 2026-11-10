
- The app **MUST** use a single-activity architecture: one `Activity` hosts the Compose UI; screens are composables, not separate activities.
- Navigation state (the `NavHostController`) **SHOULD** be created once at the top of the UI tree via `rememberNavController()` and passed down, or wrapped in narrow callbacks (`onNavigateToProfile: (id) -> Unit`) so leaf composables stay navigation-agnostic and testable.
- Screen composables **MUST NOT** read or mutate the back stack directly; they emit navigation events upward. This follows unidirectional data flow — see [adc.guideline.implementing.ui.compose-state-and-udf](cookbook:736fac9a-56e0-449d-8dc0-b95cbfba7884).

