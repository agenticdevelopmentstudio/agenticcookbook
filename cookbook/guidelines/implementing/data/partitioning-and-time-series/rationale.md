
- `should-stay-on-native-partitioning-when-sufficient`, `may-adopt-extension-only-on-measured-need`: A time-series extension (e.g. TimescaleDB/TigerData) automates chunking, retention, columnar compression, and incrementally-maintained aggregates. This is a deliberate trade-off, not a mandate.
- `should-pin-and-reverify-after-upgrades`: FORECAST / version-sensitive: PostgreSQL partition-pruning behavior and extension feature sets evolve per release. Specifics above reflect PostgreSQL 18-era docs (current as of 2026-06).
