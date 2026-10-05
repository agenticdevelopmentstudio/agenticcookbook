
**Decision**: LLM backend selected by configuration, not by handler code.
**Rationale**: Handlers must run unmodified on both the Swift dev node (local model) and the TypeScript prod node (hosted API). Injecting the backend as a configured dependency keeps handler code platform-agnostic and testable with a stub.
**Approved**: pending

