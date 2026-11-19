
Declare a JSON column as `TEXT`. Validate at insert time if needed:

```sql
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    body        TEXT NOT NULL CHECK (json_valid(body))
);
```

`json_valid()` returns 1 for valid JSON, 0 for invalid. Use this CHECK constraint when data integrity matters.

