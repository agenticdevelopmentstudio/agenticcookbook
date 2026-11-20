
- **must-use-appkit-and-uikit**: AppKit (macOS) and UIKit (iOS) MUST be used for all UI code.
- **swiftui-only-where-required**: SwiftUI MUST only be used where Apple requires it (widgets, Live Activities, App Clips).
- **keep-swiftui-layer-thin**: Where SwiftUI is required, the SwiftUI layer SHOULD be kept as thin as possible.
- **pin-target-and-avoid-deprecated-apis**: Where SwiftUI is required, you SHOULD pin the minimum deployment target and avoid deprecated APIs to reduce generation ambiguity.
