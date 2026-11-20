
Use `os.log` via `Logger` from the `os` module:

```swift
import os

private let logger = Logger(
    subsystem: "{{bundle_id}}",
    category: "ComponentName"
)

logger.debug("PrimaryButton: tapped, starting async action")
```

- Subsystem MUST match the bundle ID
- Category MUST be one per component or flow
- Use `debug` level for UI flow instrumentation

