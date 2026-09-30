<!-- leaf: ingredients/infrastructure-logging--test-vectors · source: ingredients/infrastructure/logging.md -->

# Logging

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
