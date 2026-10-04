---
id: 26a1a47f-f749-4477-ae04-c54c9a4c5117
title: "Query Optimization"
domain: agenticdevelopercookbook://guidelines/reviewing/data/query-optimization
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-04-06
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Query review checklist: anti-patterns to flag, EXPLAIN QUERY PLAN red flags, and common performance issues in SQLite queries."
platforms:
  - sqlite
  - postgresql
tags:
  - database
  - query-optimization
  - performance
  - query-planning
depends-on: []
related:
  - guidelines/data/sqlite-best-practices.md
  - guidelines/data/indexing.md
references:
  - https://sqlite.org/optoverview.html
  - https://www.sqlite.org/eqp.html
  - https://sqlite.org/queryplanner.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-06"
triggers:
  - database-operations
  - performance-optimization
---

# Query Optimization

When reviewing database queries, check EXPLAIN QUERY PLAN output and flag these anti-patterns.

## EXPLAIN QUERY PLAN red flags

Run `EXPLAIN QUERY PLAN` on any new query touching large tables. Flag these in review:

- `SCAN` — full table scan; needs an index
- `USE TEMP B-TREE FOR ORDER BY` — missing index on ORDER BY columns
- `AUTOMATIC INDEX` — SQLite created a temporary index; needs a permanent one
- `CORRELATED SCALAR SUBQUERY` — executes once per outer row; rewrite as JOIN
- `MATERIALIZE` — CTE materialized when a subquery would allow index use

## Anti-patterns to flag

1. **Correlated subqueries in SELECT** — rewrite as JOINs
2. **Functions on indexed columns in WHERE** — `WHERE date(col) = '...'` prevents index use; use range comparison instead
3. **UNION when UNION ALL suffices** — 60%+ slower due to unnecessary deduplication sort
4. **SELECT \*** — prevents covering index optimization; select only needed columns
5. **NOT IN with subqueries** — if the subquery returns any NULL, the entire result is empty. Use `NOT EXISTS` instead.
6. **OR without indexes on both sides** — causes full scan unless both columns are indexed

See the implementing copy of this guideline for detailed examples and fix patterns.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for reviewing use case — trim to anti-pattern checklist |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-04-06 | Mike Fullerton | Initial version |
