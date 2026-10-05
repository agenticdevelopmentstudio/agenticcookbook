
- **SwiftUI (macOS) with AppDelegate**: Use `@NSApplicationDelegateAdaptor` to bridge an `AppDelegate` into the SwiftUI app. Scene declarations (`WindowGroup`, `DocumentGroup`, `Settings`) go in the `@main` App struct's `body`. Apply the `.commands` modifier on the primary `WindowGroup` for custom menu items.
- **UIKit (iOS/visionOS) with SceneDelegate**: Scene-level wiring uses the `UISceneDelegate`; the ingredients' platform notes define the per-concern hooks.
- **Compose (Android)**: Scenes correspond to activities; hold lifecycle wiring in the `Application` class and the activity lifecycle callbacks described by the ingredients.
- **React/Web**: There is a single page; scene declarations do not apply. Wire the ingredients from the page's `load`, `visibilitychange`, and `beforeunload` handlers.

