
Every SQLite table (unless `WITHOUT ROWID`) has a hidden 64-bit signed integer `rowid` that is the actual B-tree key. It is accessible via the aliases `rowid`, `_rowid_`, or `oid`. Rowids are not persistent — `VACUUM` may reassign them unless they are aliased by `INTEGER PRIMARY KEY`.

