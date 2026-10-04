
```sql
-- Build a JSON array from rows
SELECT json_group_array(json_object('id', document_id, 'title', title))
FROM documents;
-- Returns: [{"id":1,"title":"..."}, ...]

-- Build a JSON object from rows
SELECT json_group_object(name, score) FROM leaderboard;
-- Returns: {"alice":100, "bob":85}
```

