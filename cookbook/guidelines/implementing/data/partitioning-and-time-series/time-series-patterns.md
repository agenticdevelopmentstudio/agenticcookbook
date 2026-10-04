
- **Range partition by time** (e.g. one partition per day/week/month sized so each holds a workable row count).
- **Retention by dropping partitions**: `DROP TABLE`/`DETACH PARTITION` on an old partition is near-instant and reclaims space, unlike a bulk `DELETE` that bloats the table and stresses autovacuum. You **SHOULD** automate partition creation and dropping (e.g. `pg_partman`).
- **BRIN indexes** on the time column suit naturally-ordered append-only data and are far smaller than B-tree; you **SHOULD** evaluate BRIN for large time-ordered partitions.
- **Rollups / continuous aggregates**: precompute summaries for queries spanning long history instead of scanning raw rows. Plain materialized views require manual refresh; some extensions refresh incrementally.

