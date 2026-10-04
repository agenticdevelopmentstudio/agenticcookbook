
```sql
-- Find documents tagged with 'urgent'
SELECT DISTINCT d.document_id
FROM documents d, json_each(d.body, '$.tags') t
WHERE t.value = 'urgent';

-- Find users with a 704 area code phone number
SELECT DISTINCT user.name
FROM user, json_each(user.phone)
WHERE json_each.value LIKE '704-%';
```

`json_each` is a table-valued function that returns one row per array element or object property.

