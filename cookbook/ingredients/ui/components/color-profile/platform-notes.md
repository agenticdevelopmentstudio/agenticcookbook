
- **Swift**: `struct ColorProfile: Codable, Identifiable, Equatable` with `TerminalColorPalette` sub-struct. Store profiles in `UserDefaults` as JSON or in app's document package. Use `NSColor(hex:)` extension for parsing. Apply to SwiftTerm via `installColors()`.
- **Kotlin**: `data class ColorProfile` with `@Serializable`. Store in SharedPreferences as JSON. Parse hex with `Color(android.graphics.Color.parseColor("#rrggbb"))`.
- **TypeScript**: Interface with hex string fields. Store in localStorage as JSON. Parse with CSS `color` property directly.

