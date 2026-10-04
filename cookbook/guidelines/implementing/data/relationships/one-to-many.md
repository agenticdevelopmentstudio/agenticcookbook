
The standard relationship pattern. A child table holds a FK column referencing the parent's PK:

```sql
CREATE TABLE artists (
    artist_id   INTEGER PRIMARY KEY,
    artist_name TEXT NOT NULL
);

CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist_id  INTEGER NOT NULL REFERENCES artists(artist_id)
);

-- Always index the FK column
CREATE INDEX ix_tracks_artist_id ON tracks(artist_id);
```

