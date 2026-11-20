
- Use **KSP** (`com.google.devtools.ksp`) for the Hilt compiler, not the legacy KAPT. KAPT is in maintenance and slower; KSP is the durable choice and supports KSP2 on Kotlin 2.x.
- Apply the `com.google.dagger.hilt.android` Gradle plugin and add `hilt-android` plus the compiler via `ksp(...)`.
- Annotate the `Application` subclass with `@HiltAndroidApp`. This is the root of the dependency graph and **MUST** exist exactly once.
- Annotate Android entry points (`Activity`, `Fragment`, `Service`) needing field injection with `@AndroidEntryPoint`.

