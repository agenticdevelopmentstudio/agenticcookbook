
- No `STRING` type used anywhere; all text columns use `TEXT`
- Type affinity explicitly understood for each column (INTEGER, TEXT, REAL, BLOB, NUMERIC)
- STRICT mode enabled on tables requiring strict type enforcement
- NUMERIC columns used only for decimal precision work (not boolean, not enum)
- Boolean columns use `INTEGER` or `TEXT` with CHECK constraint, never `BOOLEAN`
- Datetime columns use `TEXT` (ISO 8601) or `INTEGER` (Unix timestamp) with rationale documented
- For synced tables: cross-database type mapping documented (SQLite ↔ PostgreSQL equivalence)
- No reliance on implicit type coercion in queries
- Every MUST rule is kept, with no exception: `must-declare-every-column-type`, `must-use-text-for-strings`, `must-store-dates-as-iso-8601-text`, `must-use-checked-integer-for-booleans`, `must-use-text-for-precise-decimals`, `must-not-declare-misleading-type-names`, `must-use-strict-allowed-types`, `must-not-use-strict-below-3-37-0`, `must-store-sync-timestamps-as-iso-8601-utc`, `must-not-pass-sqlite-jsonb-to-postgresql`, `must-validate-json-on-both-sides`
- Every SHOULD rule is kept, or the change says why not: `should-use-strict-tables`, `should-convert-booleans-when-syncing`


A review passes when it establishes every item above.
