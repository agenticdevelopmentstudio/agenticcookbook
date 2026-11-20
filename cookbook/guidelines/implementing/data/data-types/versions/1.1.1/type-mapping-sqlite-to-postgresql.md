
When syncing or migrating between SQLite and PostgreSQL:

| Data concept | SQLite DDL | PostgreSQL |
|-------------|------------|------------|
| UUID | `id TEXT PRIMARY KEY` | `UUID` |
| Boolean | `is_active INTEGER DEFAULT 0` | `BOOLEAN` |
| Timestamp (UTC) | `created_at TEXT` | `TIMESTAMPTZ` |
| Date only | `birth_date TEXT` | `DATE` |
| Integer | `count INTEGER` | `INTEGER` / `BIGINT` |
| Decimal (precise) | `price TEXT` | `NUMERIC(10,2)` |
| Float | `latitude REAL` | `DOUBLE PRECISION` |
| Short text | `name TEXT` | `VARCHAR(255)` |
| Long text | `description TEXT` | `TEXT` |
| JSON | `metadata TEXT` | `JSONB` |
| Binary data | `avatar BLOB` | `BYTEA` |
| Enum | `status TEXT CHECK(...)` | `VARCHAR` + CHECK |

Key conversion rules when syncing:
- Booleans: convert `0`/`1` to `false`/`true` and back
- Timestamps: always store as ISO-8601 UTC; PostgreSQL uses `TIMESTAMPTZ` not `TIMESTAMP`
- SQLite JSONB is NOT binary-compatible with PostgreSQL JSONB — they are different formats
- Always validate JSON on both sides; SQLite returns NULL for invalid JSON, PostgreSQL raises an error

