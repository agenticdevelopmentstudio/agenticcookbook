
- `must-use-appkit-and-uikit`: UI code on macOS not built on AppKit, or on iOS not built on UIKit
- `swiftui-only-where-required`: a SwiftUI view outside a WidgetKit extension, a Live Activity or Dynamic Island presentation, or an App Clip
- `keep-swiftui-layer-thin`: logic, state or data access inside a required SwiftUI layer that could live in shared non-SwiftUI code
- `pin-target-and-avoid-deprecated-apis`: a required SwiftUI surface with no pinned minimum deployment target, or calling a deprecated SwiftUI API
