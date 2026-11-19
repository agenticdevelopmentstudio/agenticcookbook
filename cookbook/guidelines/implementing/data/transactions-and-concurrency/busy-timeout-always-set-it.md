
Without `busy_timeout`, any lock contention returns `SQLITE_BUSY` immediately. This causes needless errors and retry storms in multi-connection setups.

```sql
PRAGMA busy_timeout = 5000;  -- wait up to 5 seconds before returning BUSY
```

