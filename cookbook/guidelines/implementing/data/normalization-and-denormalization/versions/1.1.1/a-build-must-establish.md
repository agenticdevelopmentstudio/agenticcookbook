
- `should-start-at-3nf`: every new table is in third normal form: each non-key column depends on the whole primary key and only on it, or the code says why not
- `must-denormalize-only-when-measured-read-heavy-and-synced`: every denormalized column copies data whose join was measured as a bottleneck, which is read far more than written, and which has a stated way of being kept in sync
- `should-prefer-normalized-unless-benchmarked`: every SQLite denormalization is backed by a benchmark, or the code says why not
- `must-propagate-source-writes-to-denormalized-copies`: in a synced schema, every write to source data also reaches each denormalized copy
- `must-maintain-denormalized-column-via-trigger`: in a sync-capable schema, every denormalized column is kept current by a trigger on its source
- `must-include-denormalized-column-in-sync-payloads`: in a sync-capable schema, every denormalized column is in the sync payload
- `should-treat-normalized-source-as-authoritative`: in a sync-capable schema, the normalized source is the authoritative value and the denormalized copy is only derived from it, or the code says why not
- `should-prefer-denormalizing-stable-data`: in a sync-capable schema, the denormalized columns copy immutable or rarely-changing data (names, labels), or the code says why not
- `must-not-store-computed-values`: no column stores a count, total or derived boolean; those are computed by querying the rows
- `should-not-store-narratives-in-columns`: no column holds unstructured text that is never filtered, joined or sorted on, except as JSON whose structure is needed but not indexed, or the code says why not
- `should-not-store-lists-in-a-column`: no column holds a list (such as comma-separated IDs) for a one-to-many relationship; each item is a row in a separate table, or the code says why not

