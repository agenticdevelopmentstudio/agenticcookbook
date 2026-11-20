
SQLite stores every table as a B+ tree keyed by rowid. Every index is a separate B+ tree keyed by the indexed columns with rowid appended. A query that uses an index performs two binary searches: one on the index tree to find the rowid, then one on the table tree to retrieve the row. A covering index eliminates the second lookup entirely.

