
| State | Behavior |
|-------|----------|
| App launch | All static loggers initialized lazily or eagerly with shared subsystem |
| Debug build | All log levels emitted including debug |
| Release build | Debug-level logs suppressed; info, error, fault still emitted |
| New category added | New static property added to centralized type; no other changes needed |

