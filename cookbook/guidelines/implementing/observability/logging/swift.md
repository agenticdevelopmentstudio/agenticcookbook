
Use `os.log` via `Logger` from the `os` module:

```swift
import os

private let logger = Logger(
    subsystem: "{{bundle_id}}",
    category: "ComponentName"
)

logger.debug("PrimaryButton: tapped, starting async action")
```
