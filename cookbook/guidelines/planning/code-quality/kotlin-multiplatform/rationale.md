
- `should-share-domain-and-data-in-common`: KMP has been Stable since November 2023, so this is durable, low-risk reuse.
- `should-reserve-expect-actual-for-thin-shims`: Most common code needs none.
- `must-match-every-expect-with-actual`: the compiler enforces this.
- `should-prefer-interfaces-over-expect-actual`: interfaces plus dependency injection are easier to test and delete.
- `should-pin-cmp-version`, `should-recheck-cmp-release-notes`: Compose Multiplatform reached **Stable for iOS in CMP 1.8.0 (May 2025)**; current line is **CMP 1.11.0 (May 2026)**.
- `should-forecast-unreleased-ios-parity`, `should-validate-accessibility-on-device`: iOS UI parity (text selection, native scrolling, accessibility/VoiceOver, gestures) is improving release-over-release but **still evolving**.
- `should-design-swift-friendly-api`: Android consumes the shared module directly as a Gradle dependency. iOS consumes it as an Apple framework (XCFramework / CocoaPods / SPM).
- `should-build-every-target-in-ci`: a green Android build does not prove the iOS framework links.
