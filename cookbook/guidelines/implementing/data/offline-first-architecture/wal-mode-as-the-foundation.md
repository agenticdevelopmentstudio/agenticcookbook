
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;  -- safe for app crashes; use FULL only for power-loss safety
PRAGMA busy_timeout = 5000;   -- wait up to 5s instead of returning SQLITE_BUSY immediately
```

