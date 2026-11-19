
# Use AppKit and UIKit, not SwiftUI

AppKit (macOS) and UIKit (iOS) MUST be used for all UI code. SwiftUI MUST only be used where Apple requires it (widgets, Live Activities, App Clips). SwiftUI exists to make writing UI code easier for humans — agentic development doesn't need that. Go straight to the best tool for the LLM.

- SwiftUI is a convenience layer designed for human ergonomics: less boilerplate, live previews, reduced cognitive load. An LLM has none of these needs.
- AppKit/UIKit have 15+ years of training data, stable APIs, and explicit imperative patterns that LLMs generate reliably
- SwiftUI's API churn (NavigationView → NavigationStack, @ObservedObject → @Observable) causes version-specific generation errors that waste debugging cycles
- SwiftUI's implicit behavior (modifier ordering, view diffing, opaque layout resolution) creates bugs that are hard for agents to diagnose
- Cross-platform code sharing between iOS and macOS via SwiftUI is a compromise — the cookbook's philosophy is native code per platform, not cross-platform abstraction

