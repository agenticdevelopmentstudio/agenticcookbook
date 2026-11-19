
JSON is appropriate for:
- Variable or unpredictable attribute sets (product catalogs with per-category attributes)
- Configuration or settings blobs where the structure evolves
- Sync payloads and API responses stored verbatim

JSON is NOT appropriate for:
- Any field you would `WHERE`, `JOIN`, or `ORDER BY` regularly — make it a typed column
- One-to-many relationships — use a separate table
- Data that needs referential integrity or type enforcement

**The rule:** if a JSON field is queried in more than occasional ad-hoc queries, promote it to a real column. Add a generated column + index as the intermediate step before full promotion.

