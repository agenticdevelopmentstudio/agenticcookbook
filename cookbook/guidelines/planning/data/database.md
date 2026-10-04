---
id: e3a209f8-1b89-4d6e-bf7f-78a8aecf69cb
title: "Database"
domain: agenticdevelopercookbook://guidelines/planning/data/database
type: guideline
version: 1.0.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use SQLite with WAL mode for concurrent read access. No ORM — use direct SQL via the `sqlite3` standard library module."
platforms:
  - python
languages:
  - python
tags:
  - database
  - language
  - python
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - database-operations
---

# Database

SQLite with WAL mode MUST be used for concurrent read access. An ORM MUST NOT be used — use direct SQL via the `sqlite3` standard library module.

```python
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL")
```

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
