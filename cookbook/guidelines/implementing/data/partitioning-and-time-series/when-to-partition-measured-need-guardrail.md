
Per **YAGNI** and **make-it-work-make-it-right-make-it-fast**, do NOT partition by default. A normal indexed table serves most workloads.

- You **MUST** justify partitioning with a concrete, measured need — typically a table at real scale (commonly cited thresholds: tens of millions of rows or roughly 50-100 GB; treat these as rules of thumb, not hard limits — verify against your workload) **or** a retention requirement where you periodically purge old data.
- You **SHOULD** confirm the win with `EXPLAIN (ANALYZE)` before and after: partitioning helps only when queries filter on the partition key so the planner prunes partitions.
- You **SHOULD NOT** create partitions smaller than ~10k rows or accumulate thousands of partitions; both add planning overhead. Aim for a few dozen to a few hundred partitions.

