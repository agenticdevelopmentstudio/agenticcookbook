
- **SwiftUI (macOS) with AppDelegate**: Implement `applicationShouldOpenUntitledFile(_:)` in the `AppDelegate` to control untitled window creation based on the startup behavior setting.
- **UIKit (iOS/visionOS) with SceneDelegate**: Implement `scene(_:willConnectTo:options:)` in the `UISceneDelegate` to handle startup behavior.
- **Android (Activity lifecycle, Compose)**: Map startup behavior to `onCreate` / `onRestoreInstanceState`.
- **Web (React/SPA)**: Resolve the startup behavior from `localStorage` on page load before rendering the first view.

