
- `must-use-uuid-primary-keys`: Never use `INTEGER PRIMARY KEY AUTOINCREMENT` for synced tables — auto-incremented integers are generated locally by each device and will collide across devices when syncing.
- `should-use-uuidv7`: UUIDv7 embeds a timestamp prefix, preserving roughly-chronological insert ordering while guaranteeing global uniqueness.
- `must-add-version-column`: The version column is the authoritative signal for conflict detection.
- `must-not-hard-delete`: Hard deletes cannot be propagated — there is nothing left to sync.

