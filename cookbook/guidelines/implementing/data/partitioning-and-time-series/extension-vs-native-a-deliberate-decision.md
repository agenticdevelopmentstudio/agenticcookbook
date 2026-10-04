
A time-series extension (e.g. TimescaleDB/TigerData) automates chunking, retention, columnar compression, and incrementally-maintained aggregates. This is a deliberate trade-off, not a mandate.

- You **SHOULD** stay on native partitioning when its capabilities suffice — fewer operational dependencies.
- You **MAY** adopt an extension ONLY when a measured need (compression ratio, automated lifecycle, query speedup on large history) justifies the added dependency and operational surface.

> FORECAST / version-sensitive: PostgreSQL partition-pruning behavior and extension feature sets evolve per release. Pin to your deployed major version and re-verify `EXPLAIN` plans after upgrades. Specifics above reflect PostgreSQL 18-era docs (current as of 2026-06).

