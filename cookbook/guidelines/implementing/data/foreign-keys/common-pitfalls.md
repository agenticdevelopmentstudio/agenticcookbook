
**NULL bypasses FK checks.** `NULL` in any FK column means no parent row is required — the constraint is not evaluated. If a FK column must always have a parent, declare it `NOT NULL`.

**`INT PRIMARY KEY` vs `INTEGER PRIMARY KEY`.** Only the exact keyword `INTEGER` creates a rowid alias. `INT` creates a regular column. Referenced columns must be the PK or have a UNIQUE index.

**Composite FKs must match exactly.** Column count, types, and collation must match the parent's PRIMARY KEY or UNIQUE constraint precisely.

**ALTER TABLE restrictions.** You cannot add a column with a FK constraint and a non-NULL default:

```sql
-- Fails
ALTER TABLE tracks ADD COLUMN genre_id INTEGER NOT NULL DEFAULT 1
    REFERENCES genres(genre_id);

-- Works (NULL default is allowed)
ALTER TABLE tracks ADD COLUMN genre_id INTEGER REFERENCES genres(genre_id);
```

**Cross-schema FKs are not supported.** Foreign keys cannot reference tables in attached databases.

