
- `must-not-duplicate-index-prefix`: Redundant indexes waste write budget with no read benefit.
- `should-not-index-unqueried-columns`, `should-not-index-low-cardinality-columns`, `should-not-index-write-heavy-tables`: Every index is maintained on every INSERT, UPDATE, and DELETE. The number of indexes on a table is the dominant factor for insert performance — heavily indexed tables can see 5x slower inserts.
- `should-use-virtual-generated-columns`: VIRTUAL columns are computed on read, carry no storage cost, and can be added with `ALTER TABLE`.
- `must-not-use-partial-indexes-below-3-8-0`: Partial indexes require SQLite 3.8.0+. Databases with partial indexes cannot be read by older SQLite versions.
- `must-not-use-expression-indexes-below-3-9-0`: Expression indexes require SQLite 3.9.0+.
- `should-use-covering-indexes-on-hot-paths`: A covering index includes every column the query reads, so SQLite never has to touch the table. This roughly halves the number of disk lookups.

