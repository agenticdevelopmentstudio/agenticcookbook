
# Instrumented logging

Every component and flow must be instrumented with structured logging using the platform's best-in-class framework:

- **Apple**: `os.log` (`Logger` from `os`) — subsystem matching bundle ID, category per component
- **Android**: `Timber` (or `android.util.Log`)
- **Web**: `console` with structured prefixes, or `pino`/`winston` in Node
- **Python**: `logging` module with module-level loggers
- **Windows/.NET**: `ILogger<T>` from `Microsoft.Extensions.Logging` — category per class via generic parameter

Use `debug` level for flow instrumentation. Log state transitions, user interactions, async task start/completion/failure, and branching logic.

---

# Logging

Every component and flow must be instrumented with structured logging using the platform's best-in-class framework. Use `debug` level for flow instrumentation. Log state transitions, user interactions, async task start/completion/failure, and branching logic. Never log personally identifiable information, even at debug level.

