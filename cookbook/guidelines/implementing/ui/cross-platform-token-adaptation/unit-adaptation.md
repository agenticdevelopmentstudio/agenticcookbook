
| Platform | Length unit | Type unit | Notes |
|----------|-------------|-----------|-------|
| Apple (Swift/SwiftUI) | points (pt) | pt | Points scale by `@1x/2x/3x`; honor Dynamic Type |
| Android (Kotlin/Compose) | `dp` | `sp` | `sp` respects the user font-size setting |
| Web (TypeScript) | `rem` for type/space, `px` for hairlines | `rem` | `rem` honors the user's root font size |
| Windows (C#/WinUI) | effective pixels (epx) | epx | epx is already density-scaled |
