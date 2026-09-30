<!-- leaf: implement-data/data-types · source: guidelines/implementing/data/data-types.md -->

**Rules** (cite as `implement-data/data-types#<slug>`):

- `declare-explicit-type-column` MUST — MUST declare an explicit type on every column, even in non-STRICT tables.
- `use-text-strings-never` MUST — MUST use TEXT for strings, never STRING or VARCHAR.
- `use-text-iso-8601` MUST — MUST use TEXT in ISO 8601 format for dates: 'YYYY-MM-DD HH:MM:SS'. It sorts correctly lexicographically.
- `use-integer-booleans-check` MUST — MUST use INTEGER for booleans with a CHECK constraint: CHECK (col IN (0, 1)).
- `use-text-decimal-values` MUST — MUST use TEXT for decimal values (e.g., money) where precision matters; REAL for floats where approximation is …
- `use-strict-tables-new` SHOULD — SHOULD use STRICT tables for new schemas where type safety is important.

# Data types and type affinity

SQLite uses dynamic typing: the value determines the type, not the column declaration. A column's declared type is a preference called "affinity," not a hard constraint (unless STRICT mode is used). Understanding this is essential to writing correct schemas.

## The five storage classes

Every value belongs to exactly one storage class:

| Storage Class | Description |
|---------------|-------------|
| `NULL` | Null value |
| `INTEGER` | Signed integer (1–8 bytes, variable) |
| `REAL` | IEEE 754 float (8 bytes) |
| `TEXT` | UTF-8 string |
| `BLOB` | Raw bytes |

There is no `BOOLEAN`, `DATE`, or `DATETIME` type. These must be represented as `INTEGER` or `TEXT`.

## Type affinity rules

SQLite assigns affinity from the declared type name using these rules in order:

| Rule | If declared type contains... | Affinity |
|------|------------------------------|----------|
| 1 | `"INT"` | INTEGER |
| 2 | `"CHAR"`, `"CLOB"`, `"TEXT"` | TEXT |
| 3 | `"BLOB"` or no type | BLOB |
| 4 | `"REAL"`, `"FLOA"`, `"DOUB"` | REAL |
| 5 | Otherwise | NUMERIC |

Order matters. `"FLOATING POINT"` contains `"INT"` (in "POINT"), so affinity is INTEGER, not REAL.

## The STRING gotcha

`STRING` does NOT give TEXT affinity. Rule 5 (NUMERIC) applies because "STRING" contains neither "CHAR", "CLOB", nor "TEXT". This causes silent data corruption:

```sql
CREATE TABLE demo (val STRING);
INSERT INTO demo VALUES ('007');
SELECT typeof(val), val FROM demo;
-- Returns: integer, 7   <-- leading zeros silently lost
```

**Rule: NEVER use `STRING`. Always use `TEXT`.**

## NUMERIC affinity behavior

NUMERIC affinity aggressively converts text-like values to numbers:

```sql
CREATE TABLE demo (val NUMERIC);
INSERT INTO demo VALUES ('3.0e+5');
SELECT typeof(val), val FROM demo;
-- Returns: integer, 300000
```

## Practical type guidelines

- MUST declare an explicit type on every column, even in non-STRICT tables.
- MUST use `TEXT` for strings, never `STRING` or `VARCHAR`.
- MUST use `TEXT` in ISO 8601 format for dates: `'YYYY-MM-DD HH:MM:SS'`. It sorts correctly lexicographically.
- MUST use `INTEGER` for booleans with a CHECK constraint: `CHECK (col IN (0, 1))`.
- MUST use `TEXT` for decimal values (e.g., money) where precision matters; `REAL` for floats where approximation is acceptable.
- SHOULD use `STRICT` tables for new schemas where type safety is important.

## STRICT tables (SQLite 3.37.0+)

STRICT tables enforce rigid typing at the column level:

```sql
CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY,
    sensor_name    TEXT NOT NULL,
    reading        REAL NOT NULL,
    raw_data       BLOB
) STRICT;
```

Allowed types in STRICT mode: `INT`, `INTEGER`, `REAL`, `TEXT`, `BLOB`, `ANY`.

- Inserting the wrong type raises `SQLITE_CONSTRAINT_DATATYPE`
- `ANY` preserves values exactly as inserted with no coercion — useful for truly polymorphic columns
- `INTEGER PRIMARY KEY` still aliases rowid; `INT PRIMARY KEY` does not

```sql
CREATE TABLE demo (val ANY) STRICT;
INSERT INTO demo VALUES ('007');
SELECT typeof(val), val FROM demo;
-- Returns: text, 007   <-- preserved exactly
```

**Compatibility note:** Databases with STRICT tables cannot be opened by SQLite before 3.37.0.

You can combine `STRICT` with `WITHOUT ROWID`:

```sql
CREATE TABLE lookups (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT, WITHOUT ROWID;
```

## Type mapping: SQLite to PostgreSQL

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
