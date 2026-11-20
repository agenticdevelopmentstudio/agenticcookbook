
- You **MUST** treat documents entering the vector store as untrusted (they can carry indirect-injection payloads); validate provenance and apply per-document access controls at query time.
- You **SHOULD** account for embedding-inversion and membership-inference risk: embeddings can leak source content, so protect the vector store like the underlying data.

