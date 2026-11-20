
**`INT PRIMARY KEY` vs `INTEGER PRIMARY KEY`.** Only the exact keyword `INTEGER` creates a rowid alias. `INT` creates a regular column. Referenced columns must be the PK or have a UNIQUE index.

**ALTER TABLE restrictions.**

```sql
-- Fails
ALTER TABLE tracks ADD COLUMN genre_id INTEGER NOT NULL DEFAULT 1
    REFERENCES genres(genre_id);

-- Works (NULL default is allowed)
ALTER TABLE tracks ADD COLUMN genre_id INTEGER REFERENCES genres(genre_id);
```

