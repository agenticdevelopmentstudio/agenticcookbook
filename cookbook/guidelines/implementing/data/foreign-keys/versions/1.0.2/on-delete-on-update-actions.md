
Configure what happens to child rows when a referenced parent row is deleted or its key changes. Default is `NO ACTION`.

| Action | Behavior |
|--------|----------|
| `NO ACTION` | Fail if child rows exist (checked at statement end) |
| `RESTRICT` | Fail immediately, even with deferred constraints |
| `SET NULL` | Set child FK column(s) to NULL |
| `SET DEFAULT` | Set child FK column(s) to their DEFAULT value |
| `CASCADE` | Delete children (ON DELETE) or propagate key change (ON UPDATE) |

```sql
CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist_id  INTEGER REFERENCES artists(artist_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
```

`SET DEFAULT` will fail at runtime if the default value does not exist in the parent table. When using `SET DEFAULT`, ensure a row with the default value is always present.

