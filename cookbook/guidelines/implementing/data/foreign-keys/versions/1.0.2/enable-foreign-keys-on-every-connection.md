
```sql
PRAGMA foreign_keys = ON;
```

This MUST be executed on every database connection before any DML. It does not persist in the database file. It cannot be changed mid-transaction.

To verify the current state:

```sql
PRAGMA foreign_keys;  -- Returns 0 (off) or 1 (on)
```

