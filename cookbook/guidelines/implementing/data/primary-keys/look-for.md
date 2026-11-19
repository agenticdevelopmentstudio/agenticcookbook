
Validates primary key strategy selection, ensures INTEGER PRIMARY KEY is used correctly as rowid alias, assesses AUTOINCREMENT necessity (gap-free sequences only), evaluates UUID strategies (TEXT vs BLOB, v4 vs v7), determines WITHOUT ROWID appropriateness, and confirms cross-database PK compatibility for synced tables.

