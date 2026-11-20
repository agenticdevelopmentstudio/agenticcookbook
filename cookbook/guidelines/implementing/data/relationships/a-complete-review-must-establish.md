
- One-to-many modeled as FK on child table, never as repeating group or array
- Many-to-many always uses explicit join table (with composite PK of both FKs or own PK + unique constraint)
- Polymorphic relationships justified: discriminator column approach chosen over supertype table with rationale
- Polymorphic discriminator column has CHECK constraint listing allowed types
- If supertype table used for polymorphic: base table PK correctly referenced by all subtypes
- Self-referential FKs (e.g., `parent_id` in same table) have index on FK column and ON DELETE documented
- Tree hierarchies approach documented: adjacency list (parent pointer), closure table, or nested sets
- Adjacency list used for shallow trees; closure table for querying deep hierarchies; nested sets only if frequent hierarchical queries

A review passes when it establishes every item above.
