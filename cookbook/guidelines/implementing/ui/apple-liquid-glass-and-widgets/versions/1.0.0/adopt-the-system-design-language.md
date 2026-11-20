
- The app **MUST** use standard SwiftUI/UIKit/AppKit components (`NavigationStack`, `TabView`, `List`, `Form`, toolbars, sheets) instead of custom-drawn equivalents. System components inherit current styling, accessibility, and Dynamic Type for free.
- The agent **MUST** follow the [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) for layout, spacing, hit targets, and platform idioms; **MUST NOT** port another platform's navigation model onto Apple.
- Backgrounds and overlays **SHOULD** use system materials (`Material.regular`/`.thin`/`.ultraThin`, `.background(.regularMaterial)`) rather than hardcoded translucent colors, so they adapt to light/dark and vibrancy automatically.
- Color and typography **MUST** use semantic system values (`Color.primary`, `.secondary`, `Color(.systemBackground)`, `Font.body`/`.title`) — not fixed hex colors or fixed point sizes — to preserve contrast, Dark Mode, and accessibility scaling.
- The app **SHOULD** treat the framework choice (SwiftUI vs. UIKit/AppKit) as a deliberate decision: prefer SwiftUI for new surfaces; bridge to UIKit/AppKit only where a capability is missing.

