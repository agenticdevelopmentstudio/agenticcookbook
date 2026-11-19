
- **must-declare-every-column-type**: MUST declare an explicit type on every column, even in non-STRICT tables.
- **must-use-text-for-strings**: MUST use `TEXT` for strings, never `STRING` or `VARCHAR`.
- **must-store-dates-as-iso-8601-text**: MUST use `TEXT` in ISO 8601 format for dates: `'YYYY-MM-DD HH:MM:SS'`.
- **must-use-checked-integer-for-booleans**: MUST use `INTEGER` for booleans with a CHECK constraint: `CHECK (col IN (0, 1))`.
- **must-use-text-for-precise-decimals**: MUST use `TEXT` for decimal values (e.g., money) where precision matters; `REAL` for floats where approximation is acceptable.
- **should-use-strict-tables**: SHOULD use `STRICT` tables for new schemas where type safety is important.
- **must-not-declare-misleading-type-names**: A column's declared type name MUST NOT match an earlier affinity rule than the one intended; order matters — `"FLOATING POINT"` contains `"INT"` (in "POINT"), so affinity is INTEGER, not REAL.
- **must-use-strict-allowed-types**: A STRICT table's columns MUST be declared with only the types allowed in STRICT mode: `INT`, `INTEGER`, `REAL`, `TEXT`, `BLOB`, `ANY`.
- **must-not-use-strict-below-3-37-0**: STRICT tables MUST NOT be used in a database that SQLite before 3.37.0 must open.
- **should-convert-booleans-when-syncing**: When syncing, booleans SHOULD be converted from `0`/`1` to `false`/`true` and back.
- **must-store-sync-timestamps-as-iso-8601-utc**: When syncing, timestamps MUST always be stored as ISO-8601 UTC, and the PostgreSQL column MUST be `TIMESTAMPTZ`, not `TIMESTAMP`.
- **must-not-pass-sqlite-jsonb-to-postgresql**: SQLite JSONB MUST NOT be sent to PostgreSQL as JSONB; SQLite JSONB is NOT binary-compatible with PostgreSQL JSONB — they are different formats.
- **must-validate-json-on-both-sides**: JSON MUST always be validated on both sides; SQLite returns NULL for invalid JSON, PostgreSQL raises an error.

