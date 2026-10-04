
1. The expression is evaluated on every INSERT and UPDATE
2. The result is cast to NUMERIC
3. Integer `0` or real `0.0` → constraint violation (`SQLITE_CONSTRAINT_CHECK`)
4. `NULL` → **no violation** (NULL is not zero)
5. Any other non-zero value → no violation

**The NULL gotcha.** `CHECK (status IN ('active', 'inactive'))` permits NULL values because `NULL IN (...)` evaluates to NULL, which is not zero. If NULL should be prohibited, add `NOT NULL` as a separate constraint — it is not implied by CHECK.

