
Use these prefixes for all named objects:

```sql
-- Indexes: ix_tablename_purpose
CREATE INDEX ix_findings_workflow_run_id ON findings(workflow_run_id);
CREATE UNIQUE INDEX ux_actors_email ON actors(email);

-- Check constraints: ck_tablename_column
CONSTRAINT ck_employees_salary CHECK (salary > 0)

-- Triggers: tr_tablename_event_purpose
CREATE TRIGGER tr_documents_after_update_audit ...
```

The prefix makes object type immediately clear in schema dumps and `sqlite_schema` queries.

