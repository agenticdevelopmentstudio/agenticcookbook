
- One-to-many modeled as FK on child table, never as repeating group or array
- Many-to-many always uses explicit join table (with composite PK of both FKs or own PK + unique constraint)
- Polymorphic relationships justified: discriminator column approach chosen over supertype table with rationale
- Polymorphic discriminator column has CHECK constraint listing allowed types
- If supertype table used for polymorphic: base table PK correctly referenced by all subtypes
- Self-referential FKs (e.g., `parent_id` in same table) have index on FK column and ON DELETE documented
- Tree hierarchies approach documented: adjacency list (parent pointer), closure table, or nested sets
- Adjacency list used for shallow trees; closure table for querying deep hierarchies; nested sets only if frequent hierarchical queries
- Every MUST rule is kept, with no exception: `must-index-fk-column`, `must-enforce-generic-fk-integrity-in-application`, `must-not-use-recursive-cte-below-3-8-3`
- Every SHOULD rule is kept, or the change says why not: `should-use-junction-table-for-many-to-many`, `should-use-composite-junction-pk`, `should-index-junction-for-each-query-direction`, `should-denormalize-display-name-onto-supertype`, `should-start-with-adjacency-list`, `should-migrate-to-closure-table-only-when-measured`


A review passes when it establishes every item above.
