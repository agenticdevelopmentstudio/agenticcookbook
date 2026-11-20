
- No `STRING` type used anywhere; all text columns use `TEXT`
- Type affinity explicitly understood for each column (INTEGER, TEXT, REAL, BLOB, NUMERIC)
- STRICT mode enabled on tables requiring strict type enforcement
- NUMERIC columns used only for decimal precision work (not boolean, not enum)
- Boolean columns use `INTEGER` or `TEXT` with CHECK constraint, never `BOOLEAN`
- Datetime columns use `TEXT` (ISO 8601) or `INTEGER` (Unix timestamp) with rationale documented
- For synced tables: cross-database type mapping documented (SQLite ↔ PostgreSQL equivalence)
- No reliance on implicit type coercion in queries

A review passes when it establishes every item above.
