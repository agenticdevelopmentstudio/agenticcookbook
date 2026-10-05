
- **Stored mode is unrecognized**: If the persisted startup behavior value is not one of `newWindow`, `restoreSession`, or `nothing`, the app MUST resolve to the default (`restoreSession`) rather than failing, and the resolution SHOULD be logged with the fallback flag set (see the "Startup behavior resolved" log event).
- **Mode `nothing` on a platform without a menu bar**: The app MUST launch without opening any window and remain reachable through its dock, launcher, or background entry; it MUST NOT quit itself.

