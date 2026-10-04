
- **SwiftUI (iOS)**: Present as `.sheet`. Trigger via `UIDevice` shake notification. Guard entire file with `#if DEBUG`.
- **SwiftUI (macOS)**: Present as a floating `Window` scene. Add Debug menu item via `.commands`. Guard with `#if DEBUG`.
- **Compose (Android)**: Present as a `ModalBottomSheet` or `Dialog`. Trigger via `ShakeDetector` (accelerometer). Guard with `if (BuildConfig.DEBUG)`.
- **React (Web)**: Render as a slide-in overlay panel. Route to `/debug` in dev mode only. Guard with `process.env.NODE_ENV === 'development'`.

