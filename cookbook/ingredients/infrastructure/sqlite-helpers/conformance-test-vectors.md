
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| sqlite-helpers-001 | temp-database-url-helper | Call `tempDatabaseURL()` twice | Both URLs are in the temp directory, have `.db` extension, and are unique (different UUIDs) |
| sqlite-helpers-002 | exec-with-bindings | Call `exec("INSERT INTO settings (key, value) VALUES (?, ?)", [.text("k"), .text("v")])` | Row is inserted; no SQL injection is possible with parameterized bindings |
| sqlite-helpers-003 | query-functions | Call `queryRow("SELECT value FROM settings WHERE key = ?", [.text("k")])` | Returns single row with value `"v"` |
| sqlite-helpers-004 | last-insert-row-id | Insert a row and call `lastInsertRowID()` | Returns the integer row ID of the just-inserted row |
| sqlite-helpers-005 | sqlite-error-type | Attempt to open a non-existent database path | Throws error of type `.cannotOpen` |
| sqlite-helpers-006 | sqlite-error-type | Execute invalid SQL | Throws error of type `.execFailed` |
| sqlite-helpers-007 | query-functions | Call `queryAll` on a table with three rows | Returns all three rows in order |

