
The query planner makes better decisions with current statistics. Without them, it uses heuristics that can pick the wrong index or miss skip-scan opportunities.

```sql
-- Collect statistics for all tables
ANALYZE;

-- Collect for one table (faster)
ANALYZE orders;

-- Limit analysis time (rows examined per index)
PRAGMA analysis_limit = 1000;
ANALYZE;

-- Inspect collected statistics
SELECT * FROM sqlite_stat1;
```

SHOULD run `PRAGMA optimize` on connection open for long-lived connections. SHOULD run `ANALYZE` after bulk inserts or major schema changes. Statistics are stored in `sqlite_stat1` and used on subsequent connections.

