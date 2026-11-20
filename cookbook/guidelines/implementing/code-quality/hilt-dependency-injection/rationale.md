
- `should-reserve-singleton-for-app-scoped-state`, `should-not-apply-singleton-just-in-case`: Over-scoping is the most common Hilt mistake.
- `should-use-ksp-not-kapt`: KAPT is in maintenance and slower; KSP is the durable choice and supports KSP2 on Kotlin 2.x.
- `must-have-exactly-one-hiltandroidapp`: The `@HiltAndroidApp` `Application` subclass is the root of the dependency graph.
- `should-inject-owned-classes-via-constructor`: Hilt then provides them without a module.
- `must-not-depend-on-shorter-lived-component`: This is a captive-dependency leak.
- `should-annotate-viewmodels-with-hiltviewmodel`, `should-not-construct-hilt-viewmodels-manually`: Hilt supplies the factory.
