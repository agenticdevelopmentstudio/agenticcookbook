
- `should-declare-json-columns-as-text`: every JSON column is declared `TEXT`, or the code says why not
- `should-check-json-valid-when-integrity-matters`: every JSON column whose integrity matters carries `CHECK (json_valid(...))`, or the code says why not
- `must-extract-with-double-arrow-for-filtering`: on SQLite 3.38.0+, every JSON value used in a comparison or filter is extracted with `->>`
- `should-use-arrow-for-nested-json-text`: nested objects or arrays wanted as JSON text are extracted with `->`, or the code says why not
- `must-use-json-extract-below-3-38-0`: no query that SQLite older than 3.38.0 must run uses `->>`; those use `json_extract()`
- `should-index-json-via-generated-columns`: JSON fields queried for speed are exposed as generated columns with an index, or the code says why not
- `must-not-add-stored-columns-with-alter-table`: no `ALTER TABLE` adds a `STORED` generated column
- `should-prefer-virtual-generated-columns`: every `STORED` generated column is on a table whose reads vastly outnumber writes and whose extraction is expensive; the rest are `VIRTUAL`, or the code says why not
- `should-not-store-one-to-many-in-json`: no one-to-many relationship is held in a JSON value instead of a separate table, or the code says why not
- `should-not-store-integrity-data-in-json`: no data that needs referential integrity or type enforcement is held in JSON, or the code says why not
- `should-promote-queried-json-fields`: every JSON field queried beyond occasional ad-hoc queries is a real column, or a generated column with an index on the way to one, or the code says why not
- `must-not-send-sqlite-jsonb-to-postgresql`: no SQLite JSONB value is sent to PostgreSQL as JSONB
- `must-validate-json-on-both-sides`: JSON is validated on both the SQLite and the PostgreSQL side

