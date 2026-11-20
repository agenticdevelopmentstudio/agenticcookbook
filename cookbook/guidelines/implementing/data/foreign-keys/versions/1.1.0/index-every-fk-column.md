
Without an index on the child's FK column, every parent DELETE or UPDATE requires a full table scan of the child table. This is a silent performance trap.

```sql
-- Always create this index alongside the FK declaration
CREATE INDEX ix_tracks_artist_id ON tracks(artist_id);
```

