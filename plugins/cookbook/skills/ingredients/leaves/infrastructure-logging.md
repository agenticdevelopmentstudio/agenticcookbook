<!-- leaf: ingredients/infrastructure-logging · source: ingredients/infrastructure/logging.md -->

**Rules** (cite as `ingredients/infrastructure-logging#<slug>`):

- `centralized-logging-type` MUST
- `shared-subsystem-string` MUST
- `descriptive-category-names` MUST
- `no-adhoc-loggers` MUST
- `use-centralized-logger` MUST
- `platform-log-levels` MUST
- `suppress-debug-production` MUST
- `camelcase-categories` MUST
- `per-feature-categories` MUST
- `app-category` SHOULD
- `ui-category` SHOULD
- `single-property-extension` MUST
- `cross-module-extension` MAY

# Logging

## Overview

A centralized logging infrastructure pattern that defines a single enum or struct (e.g., `enum Log`) with static `Logger` instances per category, all sharing one subsystem. Provides clean call-site syntax such as `Log.project.info("message")`. This is the implementation pattern for Rule 9 (instrumented logging). Every feature area gets its own named category so that log output can be filtered by subsystem + category in Console.app, Logcat, or browser dev tools.

## Behavioral Requirements

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

## Configuration

This ingredient has no configurable options.

## Platform Notes

### Apple (SwiftUI / UIKit / AppKit)

Use `os.Logger` from the `os` framework. Each category gets one `Logger` instance.

```swift
import os

enum Log {
    private static let subsystem = Bundle.main.bundleIdentifier ?? "com.temporal.app"

    static let app      = Logger(subsystem: subsystem, category: "app")
    static let ui       = Logger(subsystem: subsystem, category: "ui")
    static let project  = Logger(subsystem: subsystem, category: "project")
    static let sessions = Logger(subsystem: subsystem, category: "sessions")
    static let terminal = Logger(subsystem: subsystem, category: "terminal")
    static let fileTree = Logger(subsystem: subsystem, category: "fileTree")
}

// Usage:
Log.project.info("Opened project at \(path, privacy: .public)")
Log.terminal.error("PTY spawn failed: \(error.localizedDescription)")
Log.ui.debug("Layout pass took \(duration)ms")
```

Debug-level messages are automatically excluded from production log streams by the os subsystem. Use `privacy:` modifiers on interpolated values to control redaction in Console.app.

### Android (Compose / Views)

Use `Timber` (recommended) or raw `android.util.Log` with a tag-per-category pattern.

```kotlin
// With Timber
object Log {
    private const val SUBSYSTEM = "com.temporal.app"

    fun app()      = Timber.tag("$SUBSYSTEM/app")
    fun ui()       = Timber.tag("$SUBSYSTEM/ui")
    fun project()  = Timber.tag("$SUBSYSTEM/project")
    fun sessions() = Timber.tag("$SUBSYSTEM/sessions")
    fun terminal() = Timber.tag("$SUBSYSTEM/terminal")
    fun fileTree() = Timber.tag("$SUBSYSTEM/fileTree")
}

// Usage:
Log.project().i("Opened project at %s", path)
Log.terminal().e(exception, "PTY spawn failed")

// In Application.onCreate — plant debug tree only in debug builds:
if (BuildConfig.DEBUG) {
    Timber.plant(Timber.DebugTree())
}
// In release, plant no tree or a crash-reporting tree (Crashlytics, etc.)
```

Without Timber, wrap `android.util.Log` in a similar object with tag constants and a `BuildConfig.DEBUG` guard for debug-level calls.

### Web (React / TypeScript)

Use a structured logger (e.g., `pino` for Node/SSR, or a lightweight browser wrapper). Fall back to `console` with category prefixes if no library is used.

```typescript
// logger.ts
type LogLevel = "debug" | "info" | "warn" | "error";

interface CategoryLogger {
    debug(msg: string, ...args: unknown[]): void;
    info(msg: string, ...args: unknown[]): void;
    warn(msg: string, ...args: unknown[]): void;
    error(msg: string, ...args: unknown[]): void;
}

const IS_PRODUCTION = process.env.NODE_ENV === "production";

function createCategoryLogger(category: string): CategoryLogger {
    const prefix = `[${category}]`;
    return {
        debug: (msg, ...args) => {
            if (!IS_PRODUCTION) console.debug(prefix, msg, ...args);
        },
        info: (msg, ...args) => console.info(prefix, msg, ...args),
        warn: (msg, ...args) => console.warn(prefix, msg, ...args),
        error: (msg, ...args) => console.error(prefix, msg, ...args),
    };
}

export const Log = {
    app:      createCategoryLogger("app"),
    ui:       createCategoryLogger("ui"),
    project:  createCategoryLogger("project"),
    sessions: createCategoryLogger("sessions"),
    terminal: createCategoryLogger("terminal"),
    fileTree: createCategoryLogger("fileTree"),
} as const;

// Usage:
Log.project.info("Opened project", { path });
Log.terminal.error("PTY spawn failed", error);
Log.ui.debug("Layout recalculated in", duration, "ms");
```

In production builds, `debug()` calls are no-ops. For server-side rendering, replace the console-based implementation with `pino` or `winston` for structured JSON output.
