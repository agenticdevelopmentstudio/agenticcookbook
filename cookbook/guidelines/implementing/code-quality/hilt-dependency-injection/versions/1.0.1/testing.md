
- Use `hilt-android-testing` with `kspTest`/`kspAndroidTest`. Annotate tests with `@HiltAndroidTest` and drive injection with `HiltAndroidRule`.
- Replace bindings in tests with `@TestInstallIn` or `@BindValue` rather than mutating production modules.

