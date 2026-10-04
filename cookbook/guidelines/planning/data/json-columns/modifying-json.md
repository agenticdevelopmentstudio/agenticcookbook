
```sql
-- json_set: creates or overwrites a key
UPDATE documents SET body = json_set(body, '$.status', 'processed');

-- json_insert: creates only (will not overwrite existing key)
UPDATE documents SET body = json_insert(body, '$.new_field', 42);

-- json_replace: overwrites only (will not create missing key)
UPDATE documents SET body = json_replace(body, '$.status', 'done');

-- Append to an array ($[#] is the end position)
UPDATE documents SET body = json_set(body, '$.tags[#]', 'new-tag');

-- Remove a key
UPDATE documents SET body = json_remove(body, '$.temp_field');
```

