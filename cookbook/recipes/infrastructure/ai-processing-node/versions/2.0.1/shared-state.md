
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Supported job types | Handler registry built at startup | Job worker claim request | one-way | The set is derived once from registered handlers and sent with every claim |
| Claimed job (id, type, payload, lease duration) | Backend claim response | Job worker, handler, heartbeat timer | one-way | Held in the worker's local tracking until the terminal call is acknowledged |
| Lease validity | Backend heartbeat response | Job worker | one-way | A lease-invalid response cancels the handler and suppresses complete and fail |
| LLM backend configuration | Environment variable or config file | LLM backend, injected into the handler | one-way | Read once at startup; no code change needed to switch |
| Handler result | Categorize and tag handler | Job worker | one-way | The validated `{ category, tags, confidence? }` object returned from the handler |

