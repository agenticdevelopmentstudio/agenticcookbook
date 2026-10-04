
Adapt the same numeric intent to each platform's density-independent unit. Do not ship raw `px` everywhere.

| Platform | Length unit | Type unit | Notes |
|----------|-------------|-----------|-------|
| Apple (Swift/SwiftUI) | points (pt) | pt | Points scale by `@1x/2x/3x`; honor Dynamic Type |
| Android (Kotlin/Compose) | `dp` | `sp` | `sp` respects the user font-size setting |
| Web (TypeScript) | `rem` for type/space, `px` for hairlines | `rem` | `rem` honors the user's root font size |
| Windows (C#/WinUI) | effective pixels (epx) | epx | epx is already density-scaled |

- Dimension tokens **MUST** be emitted in the target's density-independent unit; numeric values usually stay equal (8 → 8pt / 8dp / 0.5rem) but the unit and scaling semantics differ.
- Type sizes **SHOULD** map to `sp` on Android and `rem` on the web so they grow with user accessibility settings; pixel-locking text **MUST NOT** be the default.
- Hairline borders **SHOULD** resolve to the smallest crisp value per device scale rather than a fixed `1px`.

