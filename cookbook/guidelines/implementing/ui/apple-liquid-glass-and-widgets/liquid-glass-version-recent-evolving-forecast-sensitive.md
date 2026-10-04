
Liquid Glass is the translucent system material direction Apple introduced at WWDC 2025 for iOS 26 / iPadOS 26 / macOS 26 (Tahoe) and siblings. Treat its specifics as recent and evolving — pin to the iOS/macOS 26 cycle (2025–2026) and confirm against current docs before relying on exact API shapes.

- Standard components adopt the Liquid Glass look automatically when recompiled with the iOS 26 SDK; the agent **SHOULD** get the new appearance by using system components, not by hand-rolling glass.
- For custom views, the `.glassEffect(...)` modifier (with variants such as `.regular`/`.clear`) applies the material — but this API is version-recent: code using it **MUST** be gated behind an availability check (`if #available(iOS 26, macOS 26, *)`) with a graceful fallback for earlier targets. (FORECAST: exact modifier names/options may shift across point releases — verify in [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views).)
- Per Apple guidance, Liquid Glass belongs to the navigation/control layer that floats above content; the agent **MUST NOT** apply it to content itself (lists, tables, media) where it harms legibility.

