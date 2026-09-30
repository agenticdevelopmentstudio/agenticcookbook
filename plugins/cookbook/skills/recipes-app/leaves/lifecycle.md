<!-- leaf: recipes-app/lifecycle · source: recipes/app/lifecycle.md -->

**Rules** (cite as `recipes-app/lifecycle#<slug>`):

- `configurable-startup-modes` MUST
- `startup-behavior-setting` MUST
- `default-restore-session` MUST
- `save-restore-urls` MUST
- `url-list-storage` SHOULD
- `filter-registered-types` MUST
- `validate-file-exists` MUST
- `preserve-restore-order` SHOULD
- `fallback-to-new-window` SHOULD
- `terminate-child-processes` MUST
- `sighup-process-group` SHOULD (macOS)
- `track-child-handles` MUST
- `cleanup-timeout-sigkill` MUST
- `suppress-untitled-file` MUST (macOS)
- `allow-untitled-new-window` MUST (macOS)
- `suppress-untitled-relaunch` MUST (macOS)
- `multi-window-scenes` MUST (macOS/SwiftUI)
- `per-type-document-group` SHOULD
- `dedicated-settings-scene` SHOULD
- `commands-modifier` SHOULD
- `static-scene-declarations` MUST

# App Lifecycle

## Overview

Pattern for managing desktop and mobile app lifecycle: what happens on startup, how sessions and documents are restored, and how processes are cleaned up on quit. Covers multi-window scene wiring for SwiftUI apps, UIKit scene delegates, Android activity lifecycle, and Web page lifecycle. Derived from scratching-post CatnipApp.swift and AppDelegate.swift.

## Terminology

| Term | Definition |
|------|-----------|
| Startup behavior | The configurable action the app takes when it first becomes active after launch |
| Session restore | The process of reopening previously open documents or windows from a saved URL list |
| Child process | Any process spawned by the app (terminal sessions, background tasks, language servers) that must be cleaned up on quit |
| Orphaned process | A child process that continues running after the parent app has terminated |
| Scene | A SwiftUI construct (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`) that declares a window type the app can display |
| Untitled file | A new, unsaved document window that macOS may open automatically on launch |
| Process group | A set of processes sharing a PGID, allowing bulk signal delivery |

## Behavioral Requirements

### Startup behavior

- **configurable-startup-modes**: The app MUST support configurable startup behavior with at least the following modes:
  - `newWindow` — open the default window (e.g., new document or welcome screen)
  - `restoreSession` — reopen previously open documents/windows
  - `nothing` — launch silently to the menu bar (macOS) or dock/background without opening any window
- **startup-behavior-setting**: Startup behavior MUST be a user-configurable setting stored via the platform's standard persistence layer (per `settings-window.md` abstract-persistence). The setting key MUST be centralized in the app's settings key constants (per `settings-window.md` centralized-keys).
- **default-restore-session**: The startup behavior setting MUST default to `restoreSession` on first launch (no prior user preference).

### Session restore

- **save-restore-urls**: When startup behavior is `restoreSession`, the app MUST save the list of open document URLs on quit and reopen them on the next launch.
- **url-list-storage**: The URL list SHOULD be stored in `UserDefaults` (or platform equivalent) as an array of path strings, under a centralized settings key.
- **filter-registered-types**: On restore, the app SHOULD filter saved URLs to only include files whose extensions match the app's registered document types. Unrecognized extensions MUST be silently skipped.
- **validate-file-exists**: On restore, the app MUST validate that each saved URL points to an existing file. Missing files MUST be silently skipped and removed from the saved list.
- **preserve-restore-order**: On restore, the app SHOULD open documents in the same order they were saved (matching the order they were open at quit time).
- **fallback-to-new-window**: If no saved URLs exist (first launch in `restoreSession` mode, or all saved URLs are invalid), the app SHOULD fall back to the `newWindow` behavior.

### Process cleanup

- **terminate-child-processes**: On app termination, the app MUST terminate all child processes (terminal sessions, background tasks, language servers, build processes).
- **sighup-process-group** (macOS): The app SHOULD send `SIGHUP` to its process group on `applicationWillTerminate` to ensure child processes receive a termination signal.
- **track-child-handles**: The app MUST NOT leave orphaned processes after quitting. All child process handles MUST be tracked and cleaned up.
- **cleanup-timeout-sigkill**: Child process cleanup MUST complete within a reasonable timeout (5 seconds). After the timeout, remaining processes SHOULD be sent `SIGKILL`.

### Untitled window suppression

- **suppress-untitled-file** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `false` when startup behavior is `nothing` or `restoreSession`.
- **allow-untitled-new-window** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `true` when startup behavior is `newWindow`.
- **suppress-untitled-relaunch** (macOS): This method MUST also return `false` when the app is being relaunched by the system after a logout/restart and `restoreSession` is active, to avoid duplicating restored windows with an additional untitled window.

### Multi-window scene wiring

- **multi-window-scenes** (macOS/SwiftUI): The app MUST support multiple window types via scene declarations (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`).
- **per-type-document-group**: Each document type SHOULD have its own `DocumentGroup` scene with the appropriate content type and file extensions registered.
- **dedicated-settings-scene**: Settings SHOULD use a dedicated `Settings` scene (macOS 14+) or `Window` scene with `.handlesExternalEvents(matching:)` for older macOS versions.
- **commands-modifier**: Custom menu commands SHOULD be applied via the `.commands` modifier on the primary `WindowGroup`.
- **static-scene-declarations**: The `@main` App struct MUST compose all scene declarations in its `body` property. Scene declarations MUST NOT be generated dynamically at runtime.

## Platform Notes

- **SwiftUI (macOS) with AppDelegate**: Use `@NSApplicationDelegateAdaptor` to bridge an `AppDelegate` into the SwiftUI app. Implement `applicationShouldOpenUntitledFile(_:)` in the `AppDelegate` to control untitled window creation based on the startup behavior setting. Implement `applicationWillTerminate(_:)` for process cleanup and URL list saving. Use `NSApp.windows` to enumerate open document windows and collect their file URLs before quit. Scene declarations (`WindowGroup`, `DocumentGroup`, `Settings`) go in the `@main` App struct's `body`. Apply `.commands` modifier on the primary `WindowGroup` for custom menu items. Use `NSDocumentController.shared.recentDocumentURLs` as a reference but maintain the restore list separately in `UserDefaults`. For `SIGHUP` delivery, call `kill(0, SIGHUP)` to signal the entire process group, then iterate tracked child PIDs for any survivors.

- **UIKit (iOS/visionOS) with SceneDelegate**: Implement `scene(_:willConnectTo:options:)` in the `UISceneDelegate` to handle startup behavior. Use `NSUserActivity` or `UserDefaults` to persist and restore the document URL list. In `sceneDidDisconnect(_:)`, save the current document state. In `applicationWillTerminate(_:)` on the `UIApplicationDelegate`, perform final cleanup. On iOS, background tasks should be cancelled via their task handles rather than POSIX signals. On visionOS, scene management follows the same pattern as iOS.

- **Android (Activity lifecycle)**: Map startup behavior to `onCreate` / `onRestoreInstanceState`. Store the document URL list in `SharedPreferences`. In `onStop` or `onDestroy`, save the current state. Use `ProcessLifecycleOwner` to detect app-level lifecycle events. Child processes (if any) should be terminated in `onDestroy`. Android's activity back stack provides some built-in restore behavior, but explicit URL list management is needed for document-centric apps.

- **Web (SPA with beforeunload)**: Use the `beforeunload` event to save the document URL list to `localStorage`. On page load, check `localStorage` for saved URLs and restore them. Use `navigator.sendBeacon` or synchronous `localStorage` writes in the `beforeunload` handler to ensure data is saved. Web Workers or child processes (via `Worker` API) should be terminated with `worker.terminate()` in the `beforeunload` handler. The `visibilitychange` event with `document.visibilityState === 'hidden'` is more reliable than `beforeunload` on mobile browsers.
