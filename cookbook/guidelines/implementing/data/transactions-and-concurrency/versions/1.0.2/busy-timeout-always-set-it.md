
Without `busy_timeout`, any lock contention returns `SQLITE_BUSY` immediately. This causes needless errors and retry storms in multi-connection setups.

```sql
PRAGMA busy_timeout = 5000;  -- wait up to 5 seconds before returning BUSY
```

MUST set `busy_timeout` on every connection in any multi-connection or concurrent access scenario. A value of 5000ms (5 seconds) is a safe default. Set it lower (500–1000ms) for interactive UI operations where a 5-second wait would be visible to the user.

