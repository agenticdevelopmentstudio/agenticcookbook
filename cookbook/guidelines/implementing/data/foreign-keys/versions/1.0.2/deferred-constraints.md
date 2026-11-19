
By default, FK constraints are checked at the end of each statement. Deferred constraints delay checking until `COMMIT`, which allows inserting in any order within a transaction:

```sql
CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist_id  INTEGER REFERENCES artists(artist_id)
        DEFERRABLE INITIALLY DEFERRED
);

BEGIN;
INSERT INTO tracks VALUES (1, 'My Song', 5);  -- artist 5 doesn't exist yet
INSERT INTO artists VALUES (5, 'New Artist'); -- now it does
COMMIT;                                        -- constraint checked here -- passes
```

For session-wide deferral during bulk imports or migrations:

```sql
PRAGMA defer_foreign_keys = ON;
```

