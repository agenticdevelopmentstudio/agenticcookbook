
Two operators for extracting values:

```sql
-- ->> always returns a SQL type (TEXT, INTEGER, REAL, or NULL)
SELECT body ->> '$.author' FROM documents;

-- -> always returns a JSON text representation
SELECT body -> '$.tags' FROM documents;
-- For {"tags": [1,2]} returns: '[1,2]'

-- json_extract: equivalent to ->> for scalars, returns JSON text for objects/arrays
SELECT json_extract(body, '$.author') FROM documents;
```

