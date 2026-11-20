
- **partial-index**: When queries filter on a stable predicate (e.g. `WHERE status = 'active'`), a partial index (`CREATE INDEX ... WHERE status = 'active'`) **SHOULD** be used to shrink the index and skip indexing irrelevant rows.
- **expression-index**: When a query filters on a computed value (`lower(email)`, `(payload->>'tenant')`), the author **MUST** index the matching expression — a plain column index will not be used.
- **composite-column-order**: In a multi-column B-tree, columns **MUST** be ordered most-selective-and-equality-first; the leading column(s) must appear in the predicate for the index to apply.
- **covering-index**: To enable index-only scans for hot read paths, you **MAY** add `INCLUDE (...)` columns so the heap is not visited; confirm the gain with `EXPLAIN` showing `Index Only Scan`.

