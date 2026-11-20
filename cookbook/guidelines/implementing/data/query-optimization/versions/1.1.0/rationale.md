
- `should-select-only-needed-columns`: This enables covering index optimization and reduces data transfer.
- `must-use-not-exists-over-not-in`: The NULL behavior of `NOT IN` causes silent data loss.
- `should-analyze-before-evaluating-plans`: Without statistics, the planner uses heuristics that may not reflect actual row counts.
- `should-use-union-all`: `UNION` can be 60%+ slower on large datasets due to the sort and deduplication pass.
- `should-index-both-sides-of-or`: SQLite uses `MULTI-INDEX OR` if both columns are indexed independently. Without indexes on both columns, it falls back to a full scan.

