
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

