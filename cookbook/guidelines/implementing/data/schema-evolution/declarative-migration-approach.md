
For projects where the schema is defined as a canonical DDL file, compare the actual database against an in-memory copy of the target schema:

1. Load the target schema into an in-memory SQLite database
2. Query `sqlite_schema` on both databases
3. Diff the two
4. Apply `ADD COLUMN`, `CREATE INDEX`, `CREATE TABLE` changes automatically
5. Flag column type changes or removals for manual SQL

This works well for additive changes and eliminates the need to write explicit `ADD COLUMN` migrations for new nullable columns.

