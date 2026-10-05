
- **SwiftUI (macOS)**: Use `FSEventStreamCreate` with `kFSEventStreamCreateFlagFileEvents` and `kFSEventStreamCreateFlagUseCFTypes`. Schedule on a `DispatchQueue` with `.utility` QoS.
- **SwiftUI (iOS / visionOS)**: FSEvents is not available on iOS or visionOS. Use `DispatchSource.makeFileSystemObjectSource` for directory-level monitoring on individual directories, or poll on a timer. File-level granularity is limited. On visionOS, the same iOS limitations apply.
- **Compose / React/Web**: Not applicable — FSEvents is an Apple kernel facility; other platforms would substitute their native file-watching API (inotify, ReadDirectoryChangesW) behind the same requirements.

