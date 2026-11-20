
- **should-declare-json-columns-as-text**: SHOULD declare a JSON column as `TEXT`.
- **should-check-json-valid-when-integrity-matters**: SHOULD use the `CHECK (json_valid(...))` constraint to validate JSON at insert time when data integrity matters.
- **must-extract-with-double-arrow-for-filtering**: MUST use `->>` when you want the value for comparison or filtering.
- **should-use-arrow-for-nested-json-text**: SHOULD use `->` when you need the JSON text of a nested object or array.
- **must-use-json-extract-below-3-38-0**: For SQLite older than 3.38.0, code MUST use `json_extract()` instead of `->>`.
- **should-index-json-via-generated-columns**: Code that queries JSON fields at B-tree speed SHOULD expose them as generated columns and index the generated columns.
- **must-not-add-stored-columns-with-alter-table**: `ALTER TABLE` MUST NOT add a `STORED` generated column; `STORED` columns cannot be added with `ALTER TABLE`.
- **should-prefer-virtual-generated-columns**: SHOULD prefer `VIRTUAL` unless reads vastly outnumber writes and the extraction expression is expensive.
- **should-not-store-one-to-many-in-json**: One-to-many relationships SHOULD NOT be stored as JSON — use a separate table.
- **should-not-store-integrity-data-in-json**: Data that needs referential integrity or type enforcement SHOULD NOT be stored as JSON.
- **should-promote-queried-json-fields**: If a JSON field is queried in more than occasional ad-hoc queries, SHOULD promote it to a real column (any field you would `WHERE`, `JOIN`, or `ORDER BY` regularly). Add a generated column + index as the intermediate step before full promotion.
- **must-not-send-sqlite-jsonb-to-postgresql**: SQLite JSONB MUST NOT be sent to PostgreSQL as JSONB; SQLite JSONB is NOT binary-compatible with PostgreSQL JSONB — they are different on-disk formats.
- **must-validate-json-on-both-sides**: JSON MUST be validated on both sides; SQLite's `json1` returns NULL for invalid JSON, PostgreSQL raises an error.

