
- **MUST** maintain a labeled retrieval eval set and measure recall/precision before and after changes to chunking, indexing, or fusion.
- **SHOULD** start with pgvector + hybrid retrieval and only adopt a dedicated vector database when an eval or load test demonstrates pgvector cannot meet the target.

