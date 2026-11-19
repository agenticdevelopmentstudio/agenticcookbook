
- JSON columns justified: not used for data that should be normalized (e.g., comma-separated lists, simple key-value pairs)
- Frequently-queried JSON fields have generated column + B-tree index (e.g., `json_extract(data, '$.status')` as indexed generated column)
- No `json_extract` in WHERE clause without corresponding indexed generated column (prevents table scan)
- Array iteration uses `json_each()` or `json_array_length()`, not application-side parsing
- JSON modification (insert/update/delete) uses `json_insert()`, `json_set()`, `json_remove()` or application layer (not string concatenation)
- JSON structure documented: schema of expected keys/values included in comment
- No application logic relies on exact JSON string representation; always extract via `json_extract()`
- JSON columns optional/nullable unless default JSON object provided; NULL vs empty `{}` distinction understood

