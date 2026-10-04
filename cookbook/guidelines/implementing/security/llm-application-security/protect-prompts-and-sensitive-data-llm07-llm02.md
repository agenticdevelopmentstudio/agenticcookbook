
- You **MUST NOT** place secrets, credentials, or controls you rely on for security inside the system prompt — assume the system prompt can leak (LLM07: System Prompt Leakage).
- You **MUST** filter PII and sensitive data from both inputs and outputs, and avoid logging raw prompts/completions containing secrets (LLM02: Sensitive Information Disclosure).
- You **SHOULD** scope retrieved context to what the current user is authorized to see — never let RAG return another tenant's documents.

