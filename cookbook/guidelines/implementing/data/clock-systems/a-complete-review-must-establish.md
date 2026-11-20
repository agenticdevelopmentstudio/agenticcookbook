
- Clock system chosen and justified for the architecture
- Limitations of physical clocks acknowledged (skew, leap seconds)
- HLC preferred and implemented for peer-to-peer or multi-device scenarios
- Server-assigned monotonic versions used for client-server (simpler, no clock skew)
- Clock implementation format specified (e.g., 64-bit for HLC: 32-bit counter + 32-bit clock ID)
- Clock synchronization or drift tolerance documented
- Every MUST rule is kept, with no exception: `must-not-order-by-wall-clock-alone`, `must-not-use-lamport-for-concurrency-detection`, `must-not-use-server-versions-for-peer-to-peer`, `must-not-order-conflicts-by-datetime-now`
- Every SHOULD rule is kept, or the change says why not: `should-not-use-vector-clocks-for-client-side-sync`, `should-follow-hlc-update-rules`, `should-use-hlc-for-multi-device-sync`, `should-store-hlc-as-sortable-value`, `should-use-server-versions-for-centralized-sync`


A review passes when it establishes every item above.
