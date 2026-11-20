
Apple mandates SwiftUI for certain surfaces. Use it only there:
- **WidgetKit** extensions (home screen and lock screen widgets)
- **Live Activities** and Dynamic Island presentations
- **App Clips** (SwiftUI is strongly recommended by Apple)

In these cases, the SwiftUI layer SHOULD be kept as thin as possible. Pin the minimum deployment target and avoid deprecated APIs to reduce generation ambiguity.

