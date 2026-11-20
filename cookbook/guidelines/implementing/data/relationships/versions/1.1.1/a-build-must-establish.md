
- `must-index-fk-column`: in every one-to-many relationship, the child table's FK column has an index
- `should-use-junction-table-for-many-to-many`: every many-to-many relationship goes through a junction table with FKs to both parent tables, or the code says why not
- `should-use-composite-junction-pk`: every junction table's PK is the composite of both FKs, or the code says why not
- `should-index-junction-for-each-query-direction`: every direction the junction is queried from is served by an index, or the code says why not
- `must-enforce-generic-fk-integrity-in-application`: every generic FK with a discriminator column has its integrity enforced in application code
- `should-denormalize-display-name-onto-supertype`: a supertype table carries the `display_name` that common display queries need, so they make no subtype join, or the code says why not
- `must-not-use-recursive-cte-below-3-8-3`: no recursive CTE runs against SQLite older than 3.8.3
- `should-start-with-adjacency-list`: a new tree hierarchy is an adjacency list, or the code says why not
- `should-migrate-to-closure-table-only-when-measured`: a closure table replaces an adjacency list only where recursive queries are a measured performance problem, or the code says why not

