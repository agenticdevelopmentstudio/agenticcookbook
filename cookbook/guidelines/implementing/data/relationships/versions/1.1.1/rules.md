
- **must-index-fk-column**: In a one-to-many relationship, the child table's FK column MUST always be indexed.
- **should-use-junction-table-for-many-to-many**: A many-to-many relationship SHOULD use a junction table with FKs to both parent tables.
- **should-use-composite-junction-pk**: The junction table's PK SHOULD be a composite of both FKs.
- **should-index-junction-for-each-query-direction**: SHOULD add additional indexes if you query the junction from either direction.
- **must-enforce-generic-fk-integrity-in-application**: With a generic FK and a discriminator column, the application MUST enforce FK integrity; SQLite cannot enforce FK integrity across multiple tables even with `PRAGMA foreign_keys = ON` — the application owns that constraint.
- **should-denormalize-display-name-onto-supertype**: With a supertype table, SHOULD denormalize `display_name` onto the supertype to avoid subtype joins for common display queries.
- **must-not-use-recursive-cte-below-3-8-3**: Recursive CTEs MUST NOT be used where the database must be queried by SQLite older than 3.8.3; finding all descendants requires a recursive CTE (SQLite 3.8.3+).
- **should-start-with-adjacency-list**: A tree hierarchy SHOULD start with an adjacency list.
- **should-migrate-to-closure-table-only-when-measured**: SHOULD migrate to a closure table only if recursive queries become a measured performance problem.

