<!-- leaf: ingredients/infrastructure-logging--logging · source: ingredients/infrastructure/logging.md -->

# Logging

## Logging

Subsystem: `{{bundle_id}}` | Category: `logging`

This is the meta-case: the logging infrastructure itself. In practice the centralized type does not log about itself. If diagnostic logging of the logging system is needed (e.g., confirming initialization), use the `"app"` category at debug level.

| Event | Level | Message |
|-------|-------|---------|
| Subsystem initialized | debug | `Log: subsystem "{{bundle_id}}" initialized with {{count}} categories` |
