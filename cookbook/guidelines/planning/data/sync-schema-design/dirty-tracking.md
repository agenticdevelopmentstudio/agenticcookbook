
SHOULD add `is_dirty INTEGER NOT NULL DEFAULT 0` to each synced table (or a central change-log table fed by triggers). Set to `1` on every local insert or update; clear to `0` after the sync worker confirms the server accepted the change.

For apps needing operation-type awareness (INSERT vs UPDATE vs DELETE), use a change-log table with triggers instead of the flag column.

