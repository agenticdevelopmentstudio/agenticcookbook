
- **should-start-at-3nf**: New schemas SHOULD start at third normal form (3NF).
- **must-denormalize-only-when-measured-read-heavy-and-synced**: MUST NOT denormalize unless a join has been measured as a performance bottleneck, the data is read far more than written, and you have a strategy for keeping the redundant copy in sync.
- **should-prefer-normalized-unless-benchmarked**: In SQLite, SHOULD prefer normalized schemas unless benchmarks prove otherwise.
- **must-propagate-source-writes-to-denormalized-copies**: When syncing SQLite with a server database, each write to the source data MUST also propagate to denormalized copies.
- **must-maintain-denormalized-column-via-trigger**: In sync-capable schemas, code MUST maintain the denormalized column via trigger so it stays in sync within the local database.
- **must-include-denormalized-column-in-sync-payloads**: In sync-capable schemas, code MUST include the denormalized column in sync payloads so the server stays consistent.
- **should-treat-normalized-source-as-authoritative**: In sync-capable schemas, code SHOULD treat the authoritative value as the normalized source; the denormalized copy is derived.
- **should-prefer-denormalizing-stable-data**: In sync-capable schemas, SHOULD prefer denormalizing immutable or rarely-changing data (names, labels) over frequently-changing values.
- **must-not-store-computed-values**: MUST NOT store counts, totals, or derived booleans as columns. Query the rows to compute them.
- **should-not-store-narratives-in-columns**: SHOULD NOT store unstructured text that you would not `WHERE`, `JOIN`, or `ORDER BY` in a column; use JSON if the structure is needed but not indexed.
- **should-not-store-lists-in-a-column**: SHOULD NOT store one-to-many relationships as lists in a column. Make it a separate table with one row per item.

