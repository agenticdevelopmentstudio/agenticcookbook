
- Widgets **MUST** be authored in SwiftUI in a widget extension and refresh on the system-managed timeline; the agent **MUST NOT** assume continuous execution or arbitrary refresh rates.
- Interactive widgets (iOS 17+) **SHOULD** drive actions with `Button(intent:)` / `Toggle(isOn:intent:)` backed by an **App Intent**; the intent's `perform()` runs off-app in the extension, then the timeline reloads.
- Controls (iOS 18+) **SHOULD** reuse the same App Intents via `ControlWidgetButton` / `ControlWidgetToggle` so one capability surfaces in Control Center, the Lock Screen, and the Action button without duplicate logic.
- Widgets **MUST** support all required size families they declare and **MUST** respect `widgetRenderingMode` (full color, accented, vibrant) via the `\.widgetRenderingMode` environment value so they render correctly in tinted and Liquid Glass contexts.

