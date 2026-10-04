
### Centralized structure

- **centralized-logging-type**: The app MUST define a centralized, non-instantiable logging type (enum or static struct, e.g., `enum Log`) that serves as the single source of all logger instances.
- **shared-subsystem-string**: All loggers within the centralized type MUST share a single subsystem string that matches the app's bundle identifier (e.g., `com.temporal.app`).
- **descriptive-category-names**: Each static logger property MUST be initialized with a descriptive category name matching a feature area (e.g., `"sessions"`, `"terminal"`, `"project"`, `"ui"`, `"fileTree"`).
- **no-adhoc-loggers**: Categories SHOULD be defined once in the centralized type and reused throughout the codebase. Ad-hoc logger creation outside this type MUST NOT occur.

### Call-site usage

- **use-centralized-logger**: All call sites MUST use the centralized logger (e.g., `Log.ui.info("loaded")`) and MUST NOT use direct `print()`, `NSLog()`, `console.log()`, `android.util.Log.d()`, or equivalent raw output.
- **platform-log-levels**: Log levels MUST follow platform conventions:
  - **debug**: Development-only information, verbose detail for diagnosing issues.
  - **info**: Noteworthy runtime events (feature used, state transition).
  - **error**: Recoverable failures (network timeout, parse error).
  - **fault** (Apple) / **wtf** (Android) / **error** (Web): Critical, unexpected failures indicating a bug.
- **suppress-debug-production**: Debug-level logs MUST NOT appear in production/release builds. On Apple platforms, `os.Logger` handles this automatically. On Android and Web, the logging implementation MUST strip or gate debug output in release configurations.

### Category naming conventions

- **camelcase-categories**: Category names MUST be camelCase (e.g., `fileTree`, not `file_tree` or `FileTree`).
- **per-feature-categories**: Each major feature area MUST have its own category. At minimum the app SHOULD define categories for: app lifecycle, UI, networking, persistence, and each primary feature.
- **app-category**: App-wide concerns (startup, lifecycle, configuration) SHOULD use an `"app"` category.
- **ui-category**: UI-specific logging (view lifecycle, layout, navigation) SHOULD use a `"ui"` category.

### Extensibility

- **single-property-extension**: Adding a new category MUST require only adding a new static property to the centralized type — no other files or registrations.
- **cross-module-extension**: The centralized type MAY be extended across modules using language-appropriate extension mechanisms (Swift extensions, Kotlin extension properties, TypeScript module augmentation).

