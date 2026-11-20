
- `must-enable-foreign-keys-per-connection`: every code path that opens a database connection runs `PRAGMA foreign_keys = ON` before its first DML statement
- `must-reference-a-key-or-unique-column`: every foreign key references a PRIMARY KEY or a column set with a UNIQUE index
- `must-set-foreign-keys-outside-transactions`: every `PRAGMA foreign_keys` statement runs outside any open transaction
- `must-index-every-fk-column`: every foreign key column on a child table has an index created with the FK declaration
- `must-declare-required-fk-columns-not-null`: every FK column whose row must always have a parent is declared `NOT NULL`
- `must-keep-set-default-parent-row`: for every `ON DELETE SET DEFAULT` or `ON UPDATE SET DEFAULT`, the parent table always holds a row with the default value
- `must-match-composite-fks-exactly`: every composite FK has the same column count, types and collation as the parent's PRIMARY KEY or UNIQUE constraint
- `must-not-add-fk-column-with-non-null-default`: no `ALTER TABLE … ADD COLUMN` adds a FK column with a non-NULL default
- `must-not-reference-attached-databases`: no foreign key references a table in an attached database

