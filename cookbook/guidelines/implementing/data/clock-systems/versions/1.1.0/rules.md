
- **must-not-order-by-wall-clock-alone**: MUST NOT use raw wall-clock time as the sole ordering mechanism in multi-device collaborative apps.
- **must-not-use-lamport-for-concurrency-detection**: Lamport timestamps MUST NOT be used for conflict detection that requires distinguishing concurrent writes from causally ordered writes; Lamport timestamps cannot distinguish "happened-before" from "concurrent."
- **should-not-use-vector-clocks-for-client-side-sync**: Vector clocks SHOULD NOT be used for client-side mobile sync with thousands of devices (consumer apps); storage and transmission cost grows O(n) where n is the number of devices, and with thousands of devices this is impractical.
- **should-follow-hlc-update-rules**: An HLC implementation SHOULD follow the update rules: when generating an event, take `max(local_physical_time, last_hlc_physical)`; if equal, increment the logical counter; when receiving a message with an HLC, merge: take the max of both physical components, then adjust the counter to avoid collision.
- **should-use-hlc-for-multi-device-sync**: SHOULD use HLC as the default timestamp mechanism for multi-device sync.
- **should-store-hlc-as-sortable-value**: SHOULD store HLC values in SQLite as `INTEGER` (milliseconds + counter packed) or as `TEXT` with a fixed-width format that sorts lexicographically.
- **must-not-use-server-versions-for-peer-to-peer**: Server-assigned monotonic versions MUST NOT be used for pure peer-to-peer sync; they require server connectivity to assign versions.
- **should-use-server-versions-for-centralized-sync**: Server-assigned monotonic versions SHOULD be the default choice for centralized sync.
- **must-not-order-conflicts-by-datetime-now**: MUST NOT rely on SQLite's `datetime('now')` for conflict ordering in multi-device scenarios. Use HLC or server-assigned versions instead.

