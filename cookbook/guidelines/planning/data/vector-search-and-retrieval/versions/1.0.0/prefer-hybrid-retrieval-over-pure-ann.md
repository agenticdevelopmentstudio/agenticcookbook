
The key 2026 nuance: **pure approximate-nearest-neighbor (dense vector) search is not enough.** Semantic search reliably misses exact strings, rare tokens, identifiers, and keyword matches. Teams **SHOULD** use **hybrid retrieval**:

1. **Dense** — vector similarity over embeddings (semantic recall).
2. **Lexical** — keyword/BM25 search over the text (exact and rare-term recall). In Postgres this is full-text search or a BM25 extension.
3. **Fuse** — combine the two ranked lists. Reciprocal Rank Fusion (RRF) is the common default because it merges rankings without needing the two score scales to be comparable.
4. **Rerank** — optionally re-score the fused top-N with a cross-encoder reranker for final precision.

Reranking adds latency. **SHOULD** rerank only the top ~20–50 candidates and cache results for repeated queries. The dense-vs-lexical balance is workload-dependent and contested — treat fusion weights and whether to rerank as things to measure on your own eval set, not as fixed constants.

