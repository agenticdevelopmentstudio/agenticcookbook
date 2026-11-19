
This is the key pattern for JSON performance. Virtual generated columns expose JSON fields as real columns that can be indexed:

```sql
CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    body        TEXT NOT NULL
);

-- Add virtual generated columns (no disk space used; computed on read)
ALTER TABLE documents ADD COLUMN doc_type TEXT
    GENERATED ALWAYS AS (body ->> '$.type') VIRTUAL;

ALTER TABLE documents ADD COLUMN author TEXT
    GENERATED ALWAYS AS (body ->> '$.author') VIRTUAL;

-- Index the generated columns for B-tree performance
CREATE INDEX ix_documents_doc_type ON documents(doc_type);
CREATE INDEX ix_documents_author ON documents(author);

-- Queries now use the indexes
SELECT * FROM documents WHERE doc_type = 'report' AND author = 'alice';
```

**VIRTUAL vs STORED:**
- `VIRTUAL`: computed on read, no disk space, can be added with `ALTER TABLE`
- `STORED`: computed on write, uses disk space, cannot be added with `ALTER TABLE`

SHOULD prefer `VIRTUAL` unless reads vastly outnumber writes and the extraction expression is expensive.

You can also index JSON fields directly without generated columns:

```sql
CREATE INDEX ix_documents_color ON documents(body ->> '$.color');
```

This works but makes the index expression visible in queries. Named generated columns are clearer and reusable.

