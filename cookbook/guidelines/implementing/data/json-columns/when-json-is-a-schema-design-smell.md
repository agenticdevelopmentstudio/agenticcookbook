
JSON is appropriate for:
- Variable or unpredictable attribute sets (product catalogs with per-category attributes)
- Configuration or settings blobs where the structure evolves
- Sync payloads and API responses stored verbatim

JSON is NOT appropriate for:
- Any field you would `WHERE`, `JOIN`, or `ORDER BY` regularly — make it a typed column
- One-to-many relationships — use a separate table
- Data that needs referential integrity or type enforcement

