
- **jsonb-gin**: For containment queries (`@>`, key existence) on JSONB, a GIN index **SHOULD** be used.
- **jsonb-path-ops**: When only containment (`@>`) is needed, the `jsonb_path_ops` operator class **SHOULD** be preferred — it produces a smaller, faster index than the default `jsonb_ops` at the cost of dropping key-existence operators (`?`, `?|`, `?&`).
- **jsonb-write-cost**: GIN maintenance decomposes the whole document on every write, which can materially reduce insert throughput on write-heavy JSONB columns. The author **SHOULD** measure write impact before adding one, and **SHOULD** prefer an expression index on a single extracted scalar key when that is all queries need.

