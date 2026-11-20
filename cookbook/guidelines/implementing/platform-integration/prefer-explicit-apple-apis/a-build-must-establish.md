
- `must-use-appkit-and-uikit`: all UI code is AppKit on macOS and UIKit on iOS
- `swiftui-only-where-required`: SwiftUI is imported only by WidgetKit extensions, Live Activities and App Clips
- `keep-swiftui-layer-thin`: each required SwiftUI layer holds only presentation, or the code says why not
- `pin-target-and-avoid-deprecated-apis`: each required SwiftUI target pins its minimum deployment target and calls no deprecated API
