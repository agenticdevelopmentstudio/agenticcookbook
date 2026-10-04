
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

