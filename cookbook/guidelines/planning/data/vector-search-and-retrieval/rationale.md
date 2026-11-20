
- `should-default-to-pgvector`: Keeping embeddings, source rows, and metadata in **one** transactional store avoids dual-write consistency problems and an extra system to operate (simplicity, yagni).
- `should-default-to-hnsw`: It gives a better speed/recall tradeoff than IVFFlat and needs no training step; the cost is slower build time and higher memory.
- `should-use-hybrid-retrieval`: The key 2026 nuance: **pure approximate-nearest-neighbor (dense vector) search is not enough.** Semantic search reliably misses exact strings, rare tokens, identifiers, and keyword matches.
- `should-rerank-only-top-candidates-and-cache`: Reranking adds latency.
