
- `must-reference-a-key-or-unique-column`: Otherwise, table creation fails.
- `must-enable-foreign-keys-per-connection`: `PRAGMA foreign_keys` does not persist in the database file.
- `must-index-every-fk-column`: Without an index on the child's FK column, every parent DELETE or UPDATE requires a full table scan of the child table. This is a silent performance trap.

