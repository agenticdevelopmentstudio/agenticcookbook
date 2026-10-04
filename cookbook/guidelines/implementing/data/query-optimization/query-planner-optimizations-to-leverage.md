
**Skip-scan:** When the leftmost index column has few distinct values, the planner can skip-scan the index using a later constrained column. Requires `ANALYZE` to have been run (planner needs statistics showing 18+ duplicate values in the leftmost column).

**MIN/MAX optimization:** `SELECT MIN(col)` or `SELECT MAX(col)` on the leftmost column of an index executes as a single index lookup, not a full scan.

**LIKE range optimization:** `WHERE col LIKE 'prefix%'` on a column with BINARY collation is rewritten as a range scan: `col >= 'prefix' AND col < 'prefiy'`. Wildcards at the start (`LIKE '%suffix'`) prevent this optimization.

**Constant propagation:** `WHERE a = b AND b = 5` implies `a = 5`, letting the planner use an index on `a`.

**OR-to-IN conversion:** `WHERE x = 1 OR x = 2 OR x = 3` is rewritten as `WHERE x IN (1, 2, 3)` for index use.

**Subquery flattening:** SQLite merges FROM-clause subqueries into the outer query where possible, enabling index use on the underlying tables. This does not always apply — check `MATERIALIZE` in EXPLAIN output to see when it does not.

