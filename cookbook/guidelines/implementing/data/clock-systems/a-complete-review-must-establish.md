
- Clock system chosen and justified for the architecture
- Limitations of physical clocks acknowledged (skew, leap seconds)
- HLC preferred and implemented for peer-to-peer or multi-device scenarios
- Server-assigned monotonic versions used for client-server (simpler, no clock skew)
- Clock implementation format specified (e.g., 64-bit for HLC: 32-bit counter + 32-bit clock ID)
- Clock synchronization or drift tolerance documented
- Every rule is kept, or the change says why not: `must-not-order-by-wall-clock-alone`, `must-not-use-lamport-for-concurrency-detection`, `should-not-use-vector-clocks-for-client-side-sync`, `should-follow-hlc-update-rules`, `should-use-hlc-for-multi-device-sync`, `should-store-hlc-as-sortable-value`, `must-not-use-server-versions-for-peer-to-peer`, `should-use-server-versions-for-centralized-sync`, `must-not-order-conflicts-by-datetime-now`


A review passes when it establishes every item above.
