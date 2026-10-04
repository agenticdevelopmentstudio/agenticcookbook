
**Mini variant only (v1.0.0)**: The initial spec covers only the mini variant (fixed 200pt height, embedded in settings). The full variant (flexible height, standalone window, conversation management) is deferred to a future version.

**Decision**: No streaming support in v1.0.0.
**Rationale**: Streaming adds complexity (SSE parsing, incremental rendering) without significant benefit at 256 max tokens. The full variant SHOULD add streaming.
**Approved**: pending

**Decision**: Conversation history is ephemeral (not persisted).
**Rationale**: The primary use case is quick verification of AI configuration. Persistent history adds storage and privacy concerns without matching the use case.
**Approved**: pending

