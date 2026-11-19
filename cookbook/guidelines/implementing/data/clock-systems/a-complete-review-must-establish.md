
- Clock system chosen and justified for the architecture
- Limitations of physical clocks acknowledged (skew, leap seconds)
- HLC preferred and implemented for peer-to-peer or multi-device scenarios
- Server-assigned monotonic versions used for client-server (simpler, no clock skew)
- Clock implementation format specified (e.g., 64-bit for HLC: 32-bit counter + 32-bit clock ID)
- Clock synchronization or drift tolerance documented

