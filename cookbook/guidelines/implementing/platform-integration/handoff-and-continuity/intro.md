
# Handoff and continuity

Apps available on multiple devices SHOULD support continuity features so users can start work on one device and resume on another. Cross-device continuity reduces friction and meets the expectation that data follows the user, not the device.

- Capture enough state to reconstruct the user's context on the receiving device
- Continuity MUST feel instant — pre-transfer the minimum viable state, fetch details on arrival
- Fall back gracefully when the receiving device lacks a feature the originating device had
- Use deep links as the universal handoff payload — every platform can resolve a URL

