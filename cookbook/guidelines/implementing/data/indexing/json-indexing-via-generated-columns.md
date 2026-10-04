
To query JSON fields at B-tree speed, extract them as virtual generated columns and index those columns.

```sql
ALTER TABLE events ADD COLUMN event_type TEXT
  GENERATED ALWAYS AS (json_extract(data, '$.type')) VIRTUAL;

CREATE INDEX idx_event_type ON events(event_type);

-- Now uses index:
SELECT * FROM events WHERE event_type = 'click';
```

Use VIRTUAL (not STORED) unless reads vastly outnumber writes. VIRTUAL columns are computed on read, carry no storage cost, and can be added with `ALTER TABLE`.

