
New schemas SHOULD start at third normal form (3NF). A normalized schema:

- Eliminates redundancy — each fact is stored once
- Prevents update anomalies — changing one thing means changing it in one place
- Keeps storage compact

3NF requires:
1. Each column depends on the whole primary key (1NF, 2NF)
2. Each non-key column depends only on the primary key, not on other non-key columns

```sql
-- Normalized: artist is stored once, not duplicated per track
CREATE TABLE artists (
    artist_id   INTEGER PRIMARY KEY,
    artist_name TEXT NOT NULL
);

CREATE TABLE tracks (
    track_id   INTEGER PRIMARY KEY,
    track_name TEXT NOT NULL,
    artist_id  INTEGER NOT NULL REFERENCES artists(artist_id)
);
```

