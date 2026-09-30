<!-- leaf: implement-platform-integration/handoff-and-continuity · source: guidelines/implementing/platform-integration/handoff-and-continuity.md -->

**Rules** (cite as `implement-platform-integration/handoff-and-continuity#<slug>`):

- `available-multiple-devices-support-continuity-features-so` SHOULD — Apps available on multiple devices SHOULD support continuity features so users can start work on one device and resume …
- `continuity-feel-instant-pre-transfer` MUST — Continuity MUST feel instant — pre-transfer the minimum viable state, fetch details on arrival

# Handoff and continuity

Apps available on multiple devices SHOULD support continuity features so users can start work on one device and resume on another. Cross-device continuity reduces friction and meets the expectation that data follows the user, not the device.

- Capture enough state to reconstruct the user's context on the receiving device
- Continuity MUST feel instant — pre-transfer the minimum viable state, fetch details on arrival
- Fall back gracefully when the receiving device lacks a feature the originating device had
- Use deep links as the universal handoff payload — every platform can resolve a URL

## Apple (iOS / macOS)

Use `NSUserActivity` to advertise the current activity. Set `isEligibleForHandoff = true` and populate `userInfo` with state needed to restore context. Implement `application(_:continue:)` on the receiving device. Activities also appear in Spotlight and Siri Suggestions when `isEligibleForSearch` and `isEligibleForPrediction` are set. Support Universal Clipboard for cross-device copy/paste.

## Android

Use Google Play Services' Nearby Connections API or Chrome's cross-device features for continuity between Android devices. For Android-to-web continuity, use Firebase Dynamic Links or deep links that resolve in both native and web contexts. Support clipboard sync through Google account integration.

## Web

Use shared URLs as the primary continuity mechanism — a well-constructed URL with state parameters is the most universal handoff format. Support the Credential Management API for seamless sign-in across devices. Consider WebSocket or server-sent events for real-time state sync between active sessions.
