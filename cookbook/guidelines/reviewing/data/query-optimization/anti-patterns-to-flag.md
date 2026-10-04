
1. **Correlated subqueries in SELECT** — rewrite as JOINs
2. **Functions on indexed columns in WHERE** — `WHERE date(col) = '...'` prevents index use; use range comparison instead
3. **UNION when UNION ALL suffices** — 60%+ slower due to unnecessary deduplication sort
4. **SELECT \*** — prevents covering index optimization; select only needed columns
5. **NOT IN with subqueries** — if the subquery returns any NULL, the entire result is empty. Use `NOT EXISTS` instead.
6. **OR without indexes on both sides** — causes full scan unless both columns are indexed

See the implementing copy of this guideline for detailed examples and fix patterns.

