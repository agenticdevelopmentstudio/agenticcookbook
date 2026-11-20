
- `must-not-order-by-wall-clock-alone`: no multi-device collaborative app orders events by raw wall-clock time alone
- `must-not-use-lamport-for-concurrency-detection`: no conflict detection that must tell concurrent writes from causally ordered ones relies on Lamport timestamps
- `should-not-use-vector-clocks-for-client-side-sync`: no client-side mobile sync across thousands of devices carries vector clocks, or the code says why not
- `should-follow-hlc-update-rules`: the HLC takes `max(local_physical_time, last_hlc_physical)` and bumps the logical counter on a tie when generating, and merges the max of both physical components with a counter adjusted to avoid collision when receiving, or the code says why not
- `should-use-hlc-for-multi-device-sync`: multi-device sync timestamps are HLC values, or the code says why not
- `should-store-hlc-as-sortable-value`: HLC values are stored as a packed `INTEGER` or a fixed-width, lexicographically sortable `TEXT`, or the code says why not
- `must-not-use-server-versions-for-peer-to-peer`: no pure peer-to-peer sync relies on server-assigned versions
- `should-use-server-versions-for-centralized-sync`: centralized sync orders changes by server-assigned monotonic versions, or the code says why not
- `must-not-order-conflicts-by-datetime-now`: no multi-device conflict ordering uses SQLite's `datetime('now')`

