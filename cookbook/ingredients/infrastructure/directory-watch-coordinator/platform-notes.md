
- **SwiftUI (macOS)**: Publish `isSyncing` via `@Published` on an `@Observable` or `ObservableObject` coordinator. Apply tree updates on the main actor.
- **SwiftUI (iOS / visionOS)**: The same publication pattern applies; the watcher and scanner ingredients document the platform differences in change monitoring.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms; other UI frameworks would expose the same `isSyncing` and tree state through their own observable primitives.

