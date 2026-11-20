
- Compose Multiplatform reached **Stable for iOS in CMP 1.8.0 (May 2025)**; current line is **CMP 1.11.0 (May 2026)**. Pin the CMP version explicitly in the build and re-check the release notes before relying on a specific UI feature.
- iOS UI parity (text selection, native scrolling, accessibility/VoiceOver, gestures) is improving release-over-release but **still evolving** — FORECAST any unreleased item against the version you pin, and validate accessibility on-device.
- Choose shared CMP UI **only** when the team accepts current iOS maturity and values UI reuse over fully native look-and-feel; otherwise keep SwiftUI on iOS and Compose on Android while still sharing all non-UI logic. Present this as a deliberate decision per app, not a mandate.

