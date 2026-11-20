
For most applications, retrieval **SHOULD** live in the primary relational datastore via the `pgvector` extension rather than a separate vector service.

- Keeping embeddings, source rows, and metadata in **one** transactional store avoids dual-write consistency problems and an extra system to operate (simplicity, yagni).
- A separate dedicated vector database (e.g., a managed ANN service) **SHOULD** be adopted only when measured scale or latency forces it — typically tens of millions of vectors, high write throughput, or strict p99 targets pgvector cannot meet. Treat that migration as a reversible, scale-triggered decision, not a default.
- You **MUST** pin the embedding model and its output dimension as part of the schema. Mixing vectors from different models or dimensions in one column produces meaningless distances.

