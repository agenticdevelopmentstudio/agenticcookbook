---
id: ae9559b5-4829-4349-b018-986e98c31d39
title: "Apple design language and widgets"
domain: agenticdevelopercookbook://guidelines/implementing/ui/apple-liquid-glass-and-widgets
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adopt the system Apple design language and materials over custom chrome, and version-gate brand-new design APIs like Liquid Glass."
platforms:
  - swift
  - ios
  - macos
tags:
  - apple
  - design
  - widgets
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/ui/platform-design-languages
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/widgets-and-glanceable-surfaces
references:
  - https://developer.apple.com/design/human-interface-guidelines
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
  - platform-integration
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
