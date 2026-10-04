
**Storing computed values.** Do not store counts, totals, or derived booleans as columns. Query the rows to compute them. Computed columns become stale and require maintenance triggers.

**Storing summaries or narratives.** Unstructured text that you would not `WHERE`, `JOIN`, or `ORDER BY` does not belong in a column. Use JSON if the structure is needed but not indexed.

**Storing one-to-many relationships as lists in a column.** A comma-separated list of IDs in a single column is a normalization violation. Make it a separate table with one row per item.

