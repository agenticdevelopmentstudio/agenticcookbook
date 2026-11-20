
- `should-default-to-integer-primary-key`: There is no separate storage and no separate index — it is the fastest possible PK in SQLite.
- `must-not-autoincrement-synced-tables`: IDs will collide across devices.
- `must-use-client-uuids-for-multi-device-sync`: UUIDs enable client-side ID generation without server coordination, which is essential for offline-first sync. Without UUIDs, two offline devices using autoincrement will produce identical IDs that collide on sync.
- `must-not-rely-on-implicit-rowid`: Rowids are not persistent — `VACUUM` may reassign them unless they are aliased by `INTEGER PRIMARY KEY`.
- `must-not-use-without-rowid-below-3-8-2`: `WITHOUT ROWID` requires SQLite 3.8.2+.
- `must-limit-autoincrement`: If the counter reaches `2^63 - 1`, further inserts fail with `SQLITE_FULL`.

