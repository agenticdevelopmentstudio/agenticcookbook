
**Application lifecycle callbacks:**

- iOS/macOS: `UIApplicationDelegate` methods — `application(_:didFinishLaunchingWithOptions:)`, `applicationDidBecomeActive`, `applicationWillResignActive`, `applicationDidEnterBackground`, `applicationWillTerminate`; `SceneDelegate` equivalents for multi-window
- Android: `Activity.onCreate/onStart/onResume/onPause/onStop/onDestroy`, `Service.onCreate/onStartCommand`, `Application.onCreate`, `ContentProvider.onCreate`
- Web: `DOMContentLoaded`, `load`, `beforeunload`, `unload`, `visibilitychange`, `pageshow`/`pagehide`; Service Worker lifecycle (`install`, `activate`, `fetch`)
- Windows: `OnLaunched`, `OnSuspending`, `OnResuming` (UWP); `Application_Startup`, `Application_Exit` (WPF); `Main()` entry point with message loop

**Background execution:**

- iOS: `BGTaskScheduler.submit()`, `beginBackgroundTask(withName:)`, `URLSession` background download/upload tasks, `WKExtensionDelegate` background fetch
- Android: `WorkManager`, `JobScheduler`, `AlarmManager`, `Service` with `START_STICKY`, `BroadcastReceiver` for system events
- Web: Service Worker `sync` event, `BackgroundFetch API`, `Periodic Background Sync`
- Windows: Background tasks via `IBackgroundTask`, `AppService` connections

**Interprocess communication (IPC):**

- iOS: App Extensions communicate via shared containers or `NSXPCConnection`; `openURL` to other apps; `CFMessagePort`; Pasteboard for cross-process data
- Android: `Intent` system (explicit and implicit); `ContentProvider` for structured data sharing; `AIDL` interfaces; `Messenger`
- Windows: Named pipes (`NamedPipeServerStream`/`NamedPipeClientStream`); COM/DCOM; WCF (Windows Communication Foundation); `MemoryMappedFile` for shared memory
- Web: `window.postMessage` cross-origin; `SharedWorker`; `BroadcastChannel`; `MessageChannel`; Service Worker message passing

**Push notifications and remote events:**

- iOS: `UNUserNotificationCenter` delegate methods; `application(_:didReceiveRemoteNotification:)` in AppDelegate; `UNNotificationServiceExtension` for content modification
- Android: `FirebaseMessagingService.onMessageReceived()`; notification channel creation; `PendingIntent` for notification actions
- Web: `ServiceWorkerRegistration.showNotification()`; `push` event in Service Worker; `notificationclick` handler
- Windows: `ToastNotification`; `BadgeUpdateManager`; `TileUpdateManager`

**URL schemes and deep links:**

- iOS: `application(_:open:options:)` for custom URL schemes; `application(_:continue:restorationHandler:)` for Universal Links; `UIApplicationShortcutItem` for home screen quick actions
- Android: `Intent` filters with `ACTION_VIEW` and URI patterns in `AndroidManifest.xml`; `onNewIntent()` handling
- Web: Protocol handlers (`registerProtocolHandler`); Progressive Web App URL handling in `manifest.json`
- Windows: Protocol activation in `Package.appxmanifest`; `OnActivated` handler in App class

**File system and OS integration:**

- Document provider extensions (iOS `UIDocumentPickerViewController`, Android Storage Access Framework, Windows `FileOpenPicker`)
- File watching / directory monitoring (`FSEvents`, `inotify`, `FileSystemWatcher`, `ReadDirectoryChangesW`)
- Socket communication (Unix domain sockets, TCP sockets for localhost IPC)

**Keyboard, accessibility, and input system integration:**

- Custom keyboard extensions (iOS `UIInputViewController`)
- Accessibility tree callbacks (`UIAccessibility`, `AccessibilityService` on Android)
- Input Method Editor (IME) integration
- Global keyboard shortcut registration

