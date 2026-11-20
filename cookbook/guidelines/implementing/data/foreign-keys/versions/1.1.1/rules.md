
- **must-enable-foreign-keys-per-connection**: `PRAGMA foreign_keys = ON` MUST be executed on every database connection before any DML.
- **must-reference-a-key-or-unique-column**: The referenced column(s) MUST be the PRIMARY KEY or have a UNIQUE index.
- **must-set-foreign-keys-outside-transactions**: `PRAGMA foreign_keys` MUST be issued outside a transaction; it cannot be changed mid-transaction.
- **must-index-every-fk-column**: MUST create an index on the child's FK column alongside the FK declaration.
- **must-declare-required-fk-columns-not-null**: If a FK column must always have a parent, it MUST be declared `NOT NULL`; `NULL` in any FK column means no parent row is required — the constraint is not evaluated.
- **must-keep-set-default-parent-row**: When using `SET DEFAULT`, a row with the default value MUST always be present in the parent table; `SET DEFAULT` will fail at runtime if the default value does not exist in the parent table.
- **must-match-composite-fks-exactly**: Composite FKs MUST match exactly: column count, types, and collation must match the parent's PRIMARY KEY or UNIQUE constraint precisely.
- **must-not-add-fk-column-with-non-null-default**: `ALTER TABLE` MUST NOT add a column with a FK constraint and a non-NULL default; it fails (a NULL default is allowed).
- **must-not-reference-attached-databases**: Foreign keys MUST NOT reference tables in attached databases; cross-schema FKs are not supported.

