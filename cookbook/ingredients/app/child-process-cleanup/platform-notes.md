
- **SwiftUI (macOS) with AppDelegate**: Implement `applicationWillTerminate(_:)` for process cleanup. For `SIGHUP` delivery, call `kill(0, SIGHUP)` to signal the entire process group, then iterate tracked child PIDs for any survivors.
- **UIKit (iOS/visionOS) with SceneDelegate**: In `applicationWillTerminate(_:)` on the `UIApplicationDelegate`, perform final cleanup. On iOS, background tasks should be cancelled via their task handles rather than POSIX signals. On visionOS, scene management follows the same pattern as iOS.
- **Android (Activity lifecycle, Compose)**: Child processes (if any) should be terminated in `onDestroy`.
- **Web (SPA with beforeunload)**: Web Workers or child processes (via `Worker` API) should be terminated with `worker.terminate()` in the `beforeunload` handler.

