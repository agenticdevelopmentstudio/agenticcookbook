
Choose a specialist primary store **only** when a requirement below is concrete and, where possible, measured:

| Need | Signal that justifies it | Candidate store |
|------|--------------------------|-----------------|
| Relational, transactional, mixed queries | Default — entities with relationships, joins, integrity | Relational (Postgres) |
| Schema-fluid documents, per-record variance | Shapes genuinely differ per record AND joins are rare | Document store |
| Simple key lookups, cache, session, ultra-low latency | Access is `get`/`set` by key at high throughput | Key-value store |
| Full-text / faceted search at scale | Relevance ranking, fuzzy match beyond DB full-text | Search engine |
| High-frequency time-stamped writes + time-range queries | Metrics/telemetry/IoT with retention and downsampling | Time-series store |
| Deep multi-hop relationship traversal | Queries are mostly graph walks (friend-of-friend, paths) | Graph store |
| Semantic / embedding similarity | Vector search is core; `pgvector` insufficient at scale | Vector store |

