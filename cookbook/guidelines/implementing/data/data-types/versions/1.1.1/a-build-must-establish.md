
- `must-declare-every-column-type`: every column in every `CREATE TABLE` and `ADD COLUMN` declares an explicit type
- `must-use-text-for-strings`: every string column is declared `TEXT`; no column is declared `STRING` or `VARCHAR`
- `must-store-dates-as-iso-8601-text`: every date column is `TEXT` and every value written to it is ISO 8601 (`'YYYY-MM-DD HH:MM:SS'`)
- `must-use-checked-integer-for-booleans`: every boolean column is `INTEGER` with `CHECK (col IN (0, 1))`
- `must-use-text-for-precise-decimals`: every decimal value where precision matters (such as money) is stored as `TEXT`, and `REAL` holds only floats where approximation is acceptable
- `should-use-strict-tables`: every new table where type safety is important is `STRICT`, or the code says why not
- `must-not-declare-misleading-type-names`: every declared type name gets the affinity its column intends under the five rules in order (no `FLOATING POINT`-style names)
- `must-use-strict-allowed-types`: every column of every STRICT table is declared `INT`, `INTEGER`, `REAL`, `TEXT`, `BLOB` or `ANY`
- `must-not-use-strict-below-3-37-0`: every database holding a STRICT table is only opened by SQLite 3.37.0+
- `should-convert-booleans-when-syncing`: the sync layer converts booleans between `0`/`1` and `false`/`true` in both directions, or the code says why not
- `must-store-sync-timestamps-as-iso-8601-utc`: every synced timestamp is stored as ISO-8601 UTC, and its PostgreSQL column is `TIMESTAMPTZ`
- `must-not-pass-sqlite-jsonb-to-postgresql`: no sync path sends SQLite JSONB to PostgreSQL as JSONB
- `must-validate-json-on-both-sides`: JSON is validated on both the SQLite side and the PostgreSQL side

