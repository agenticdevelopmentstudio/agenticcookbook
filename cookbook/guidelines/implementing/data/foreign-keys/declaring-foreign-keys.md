
**Inline (column-level):**

```sql
CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist_id  INTEGER NOT NULL REFERENCES artists(artist_id)
);
```

**Table-level (required for composite FKs):**

```sql
CREATE TABLE songs (
    song_id     INTEGER PRIMARY KEY,
    song_artist TEXT NOT NULL,
    song_album  TEXT NOT NULL,
    FOREIGN KEY (song_artist, song_album)
        REFERENCES albums(album_artist, album_name)
);
```

The referenced column(s) MUST be the PRIMARY KEY or have a UNIQUE index. Otherwise, table creation fails.

