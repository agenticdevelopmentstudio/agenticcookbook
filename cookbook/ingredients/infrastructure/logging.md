---
id: 7c2049c7-89d9-4135-b657-dbd03cdd19a0
title: "Logging"
domain: agenticdevelopercookbook://ingredients/infrastructure/logging
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Centralized logging infrastructure with per-category static logger instances sharing one subsystem"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - infrastructure
  - logging
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

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

## Appearance

Not applicable — this component is invisible infrastructure.

## States

| State | Behavior |
|-------|----------|
| App launch | All static loggers initialized lazily or eagerly with shared subsystem |
| Debug build | All log levels emitted including debug |
| Release build | Debug-level logs suppressed; info, error, fault still emitted |
| New category added | New static property added to centralized type; no other changes needed |

## Accessibility

Not applicable — logging has no user-facing surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| log-001 | centralized-logging-type, shared-subsystem-string | Inspect `Log` type | Non-instantiable type exists with static logger properties sharing one subsystem |
| log-002 | descriptive-category-names | Inspect each static property | Each logger has a unique, descriptive category string |
| log-003 | use-centralized-logger | Call `Log.project.info("opened")` | Log entry appears with subsystem = bundle ID, category = "project", level = info |
| log-004 | use-centralized-logger | Search codebase for raw `print(` / `NSLog(` / `console.log(` | Zero hits outside of test helpers or logging infrastructure |
| log-005 | platform-log-levels | Call `Log.app.debug("verbose detail")` | Entry logged at debug level |
| log-006 | platform-log-levels | Call `Log.app.error("network timeout")` | Entry logged at error level |
| log-007 | suppress-debug-production | Run release build, call `Log.app.debug("hidden")` | Debug entry does NOT appear in log output |
| log-008 | suppress-debug-production | Run release build, call `Log.app.info("visible")` | Info entry DOES appear in log output |
| log-009 | camelcase-categories | Inspect all category strings | All are camelCase |
| log-010 | single-property-extension | Add `static let payments = Logger(subsystem: subsystem, category: "payments")` | New category works immediately with no other changes |

## Edge Cases

- **High-frequency logging**: Logging in tight loops (e.g., per-frame rendering) SHOULD use debug level so it is automatically suppressed in release. If logging cannot be avoided, consider rate-limiting or sampling.
- **Sensitive data**: Log messages MUST NOT contain passwords, tokens, or PII. Use `privacy: .private` on Apple (os.Logger interpolation) or redact explicitly on other platforms.
- **Module boundaries**: In a multi-module project, each module MAY define its own `Log` enum, but all MUST share the same subsystem string so filtering by subsystem captures everything.
- **Thread safety**: Platform logging APIs (os.Logger, android.util.Log, console) are thread-safe. The centralized type's static properties are initialized once and are read-only, so no synchronization is needed.
- **Logger initialization cost**: On Apple, `os.Logger` is lightweight. Static `let` properties ensure each logger is created exactly once.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `logging`

This is the meta-case: the logging infrastructure itself. In practice the centralized type does not log about itself. If diagnostic logging of the logging system is needed (e.g., confirming initialization), use the `"app"` category at debug level.

| Event | Level | Message |
|-------|-------|---------|
| Subsystem initialized | debug | `Log: subsystem "{{bundle_id}}" initialized with {{count}} categories` |

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

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |
| [no-pii-in-logs](agenticdevelopercookbook://compliance/privacy-and-data#no-pii-in-logs) | partial | Privacy |
| [health-observability](agenticdevelopercookbook://compliance/reliability#health-observability) | partial | Reliability |
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
