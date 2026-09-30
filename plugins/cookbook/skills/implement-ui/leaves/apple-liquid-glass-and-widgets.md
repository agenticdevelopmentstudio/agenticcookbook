<!-- leaf: implement-ui/apple-liquid-glass-and-widgets · source: guidelines/implementing/ui/apple-liquid-glass-and-widgets.md -->

**Rules** (cite as `implement-ui/apple-liquid-glass-and-widgets#<slug>`):

- `reinventing-chrome-agent-let-platform-supply-materials` SHOULD — Build with Apple's system design language and standard components rather than reinventing chrome. The agent SHOULD let …
- `app-use-standard-swiftui-uikit` MUST — The app MUST use standard SwiftUI/UIKit/AppKit components (NavigationStack, TabView, List, Form, toolbars, sheets) …
- `agent-follow-apple-human-interface` MUST — The agent MUST follow the Apple Human Interface Guidelines for layout, spacing, hit targets, and platform idioms; MUST …
- `backgrounds-overlays-use-system-materials-material` SHOULD — Backgrounds and overlays SHOULD use system materials (Material.regular/.thin/.ultraThin, .background(.regularMaterial)) …
- `color-typography-use-semantic-system-values` MUST — Color and typography MUST use semantic system values (Color.primary, .secondary, Color(.systemBackground), …
- `app-treat-framework-choice-swiftui` SHOULD — The app SHOULD treat the framework choice (SwiftUI vs. UIKit/AppKit) as a deliberate decision: prefer SwiftUI for new …
- `26-sdk-agent-get-new-appearance-using` SHOULD — Standard components adopt the Liquid Glass look automatically when recompiled with the iOS 26 SDK; the agent SHOULD get …
- `recent-code-using-gated-behind-availability-check` MUST — For custom views, the .glassEffect(...) modifier (with variants such as .regular/.clear) applies the material — but …
- `above-content-agent-not-apply-content-itself-lists` MUST — Per Apple guidance, Liquid Glass belongs to the navigation/control layer that floats above content; the agent MUST NOT …
- `widgets-authored-swiftui-widget-extension` MUST — Widgets MUST be authored in SwiftUI in a widget extension and refresh on the system-managed timeline; the agent MUST …
- `widgets-ios-17-drive-actions-button-intent` SHOULD — Interactive widgets (iOS 17+) SHOULD drive actions with Button(intent:) / Toggle(isOn:intent:) backed by an App Intent; …
- `controls-ios-18-reuse-same-app-intents` SHOULD — Controls (iOS 18+) SHOULD reuse the same App Intents via ControlWidgetButton / ControlWidgetToggle so one capability …
- `widgets-support-size-families-they` MUST — Widgets MUST support all required size families they declare and MUST respect widgetRenderingMode (full color, …

# Apple design language and widgets

Build with Apple's system design language and standard components rather than reinventing chrome. The agent SHOULD let the platform supply materials, layout, and behavior, and treat brand-new design APIs as version-gated until the deployment target supports them.

## Adopt the system design language

- The app **MUST** use standard SwiftUI/UIKit/AppKit components (`NavigationStack`, `TabView`, `List`, `Form`, toolbars, sheets) instead of custom-drawn equivalents. System components inherit current styling, accessibility, and Dynamic Type for free.
- The agent **MUST** follow the [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines) for layout, spacing, hit targets, and platform idioms; **MUST NOT** port another platform's navigation model onto Apple.
- Backgrounds and overlays **SHOULD** use system materials (`Material.regular`/`.thin`/`.ultraThin`, `.background(.regularMaterial)`) rather than hardcoded translucent colors, so they adapt to light/dark and vibrancy automatically.
- Color and typography **MUST** use semantic system values (`Color.primary`, `.secondary`, `Color(.systemBackground)`, `Font.body`/`.title`) — not fixed hex colors or fixed point sizes — to preserve contrast, Dark Mode, and accessibility scaling.
- The app **SHOULD** treat the framework choice (SwiftUI vs. UIKit/AppKit) as a deliberate decision: prefer SwiftUI for new surfaces; bridge to UIKit/AppKit only where a capability is missing.

## Liquid Glass — version-recent, evolving (FORECAST-sensitive)

Liquid Glass is the translucent system material direction Apple introduced at WWDC 2025 for iOS 26 / iPadOS 26 / macOS 26 (Tahoe) and siblings. Treat its specifics as recent and evolving — pin to the iOS/macOS 26 cycle (2025–2026) and confirm against current docs before relying on exact API shapes.

- Standard components adopt the Liquid Glass look automatically when recompiled with the iOS 26 SDK; the agent **SHOULD** get the new appearance by using system components, not by hand-rolling glass.
- For custom views, the `.glassEffect(...)` modifier (with variants such as `.regular`/`.clear`) applies the material — but this API is version-recent: code using it **MUST** be gated behind an availability check (`if #available(iOS 26, macOS 26, *)`) with a graceful fallback for earlier targets. (FORECAST: exact modifier names/options may shift across point releases — verify in [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views).)
- Per Apple guidance, Liquid Glass belongs to the navigation/control layer that floats above content; the agent **MUST NOT** apply it to content itself (lists, tables, media) where it harms legibility.

## WidgetKit and glanceable surfaces

- Widgets **MUST** be authored in SwiftUI in a widget extension and refresh on the system-managed timeline; the agent **MUST NOT** assume continuous execution or arbitrary refresh rates.
- Interactive widgets (iOS 17+) **SHOULD** drive actions with `Button(intent:)` / `Toggle(isOn:intent:)` backed by an **App Intent**; the intent's `perform()` runs off-app in the extension, then the timeline reloads.
- Controls (iOS 18+) **SHOULD** reuse the same App Intents via `ControlWidgetButton` / `ControlWidgetToggle` so one capability surfaces in Control Center, the Lock Screen, and the Action button without duplicate logic.
- Widgets **MUST** support all required size families they declare and **MUST** respect `widgetRenderingMode` (full color, accented, vibrant) via the `\.widgetRenderingMode` environment value so they render correctly in tinted and Liquid Glass contexts.
