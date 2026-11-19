
For one-time bulk loads where crash safety during the load is acceptable:

```sql
PRAGMA journal_mode = OFF;
PRAGMA synchronous = 0;
PRAGMA cache_size = 1000000;
PRAGMA locking_mode = EXCLUSIVE;
PRAGMA temp_store = MEMORY;
```

Restore safe settings immediately after the bulk load completes. MUST NOT use these settings in production code paths.

