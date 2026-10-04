
SQLite is embedded — there is zero network latency for queries. The N+1 query problem that drives aggressive denormalization in client/server databases (PostgreSQL, MySQL) is far less severe in SQLite. Multiple simple queries often outperform a single complex JOIN.

**Implication:** The threshold for denormalization in SQLite is higher than in networked databases. Prefer normalized schemas unless benchmarks prove otherwise.

Benchmark reference: in one test across 5,000 records, a denormalized schema was 16x faster for one query pattern and 104x faster for another — but was also 50% smaller. In SQLite, denormalization can simultaneously improve speed and reduce size because it eliminates B-tree traversals on join columns.

