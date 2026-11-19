
MUST match the referenced column name when possible. When a table references the same parent table more than once, add a descriptive qualifier:

```sql
-- Single reference: match parent PK name
finding_id INTEGER REFERENCES findings(finding_id)

-- Multiple references to same parent: add qualifier
source_actor_id      INTEGER REFERENCES actors(actor_id),
destination_actor_id INTEGER REFERENCES actors(actor_id)
```

