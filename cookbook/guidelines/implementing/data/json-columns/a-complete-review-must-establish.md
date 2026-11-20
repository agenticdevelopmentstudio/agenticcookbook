
- JSON columns justified: not used for data that should be normalized (e.g., comma-separated lists, simple key-value pairs)
- Frequently-queried JSON fields have generated column + B-tree index (e.g., `json_extract(data, '$.status')` as indexed generated column)
- No `json_extract` in WHERE clause without corresponding indexed generated column (prevents table scan)
- Array iteration uses `json_each()` or `json_array_length()`, not application-side parsing
- JSON modification (insert/update/delete) uses `json_insert()`, `json_set()`, `json_remove()` or application layer (not string concatenation)
- JSON structure documented: schema of expected keys/values included in comment
- No application logic relies on exact JSON string representation; always extract via `json_extract()`
- JSON columns optional/nullable unless default JSON object provided; NULL vs empty `{}` distinction understood
- Every rule is kept, or the change says why not: `should-declare-json-columns-as-text`, `should-check-json-valid-when-integrity-matters`, `must-extract-with-double-arrow-for-filtering`, `should-use-arrow-for-nested-json-text`, `must-use-json-extract-below-3-38-0`, `should-index-json-via-generated-columns`, `must-not-add-stored-columns-with-alter-table`, `should-prefer-virtual-generated-columns`, `should-not-store-one-to-many-in-json`, `should-not-store-integrity-data-in-json`, `should-promote-queried-json-fields`, `must-not-send-sqlite-jsonb-to-postgresql`, `must-validate-json-on-both-sides`


A review passes when it establishes every item above.
