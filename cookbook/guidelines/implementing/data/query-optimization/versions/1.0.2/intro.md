
# Query Optimization

SQLite's query planner is good, but it cannot compensate for poorly structured queries. Write queries that cooperate with the planner: let indexes be used, minimize rows examined, and avoid patterns that force sequential scans or per-row subqueries.

