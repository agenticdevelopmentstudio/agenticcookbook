
The SQLite helpers are the minimal utility layer a document storage format needs to talk to SQLite safely: create a unique temporary database path, execute SQL with parameterized bindings, read single or multiple rows, retrieve the last inserted row ID, and report failures through a dedicated error type. They keep raw `sqlite3` calls out of document code and make SQL injection impossible by construction, because values only ever travel as bindings. Use them wherever code reads or writes SQLite files directly.

