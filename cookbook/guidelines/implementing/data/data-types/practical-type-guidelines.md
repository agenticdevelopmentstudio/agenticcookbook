
- MUST declare an explicit type on every column, even in non-STRICT tables.
- MUST use `TEXT` for strings, never `STRING` or `VARCHAR`.
- MUST use `TEXT` in ISO 8601 format for dates: `'YYYY-MM-DD HH:MM:SS'`. It sorts correctly lexicographically.
- MUST use `INTEGER` for booleans with a CHECK constraint: `CHECK (col IN (0, 1))`.
- MUST use `TEXT` for decimal values (e.g., money) where precision matters; `REAL` for floats where approximation is acceptable.
- SHOULD use `STRICT` tables for new schemas where type safety is important.

