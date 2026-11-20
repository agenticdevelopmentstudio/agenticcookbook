
- `must-use-appkit-and-uikit`, `swiftui-only-where-required`: SwiftUI is a convenience layer designed for human ergonomics: less boilerplate, live previews, reduced cognitive load. An LLM has none of these needs.
- `must-use-appkit-and-uikit`, `swiftui-only-where-required`: AppKit/UIKit have 15+ years of training data, stable APIs, and explicit imperative patterns that LLMs generate reliably
- `must-use-appkit-and-uikit`, `swiftui-only-where-required`: SwiftUI's API churn (NavigationView → NavigationStack, @ObservedObject → @Observable) causes version-specific generation errors that waste debugging cycles
- `must-use-appkit-and-uikit`, `swiftui-only-where-required`: SwiftUI's implicit behavior (modifier ordering, view diffing, opaque layout resolution) creates bugs that are hard for agents to diagnose
- `must-use-appkit-and-uikit`, `swiftui-only-where-required`: Cross-platform code sharing between iOS and macOS via SwiftUI is a compromise — the cookbook's philosophy is native code per platform, not cross-platform abstraction
