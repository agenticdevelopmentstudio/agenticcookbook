
- **SwiftUI (macOS)**: Use `FileManager` for directory enumeration. Use `OperationQueue` with `maxConcurrentOperationCount` for parallel scanning.
- **SwiftUI (iOS / visionOS)**: Surgical updates may need to rescan entire directories because file-level change granularity is limited. Consider `NSFilePresenter` / `NSFileCoordinator` for coordinated file access.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms and TypeScript services using a local filesystem.

