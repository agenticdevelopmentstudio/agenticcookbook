
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Supported job types | Handler registry built at startup | Job worker claim request | one-way | The set is derived once from registered handlers and sent with every claim |
| Claimed job (id, type, payload, lease duration) | Backend claim response | Job worker, handler, heartbeat timer | one-way | Held in the worker's local tracking until the terminal call is acknowledged |
| Lease validity | Backend heartbeat response | Job worker | one-way | A lease-invalid response cancels the handler and suppresses complete and fail |
| LLM backend configuration | Environment variable or config file | LLM backend, injected into the handler | one-way | Read once at startup; no code change needed to switch |
| `claude-code` availability | The CLI's answer to `--version` | The claim's `capabilities` and the `claude-code` runner | one-way | A yes is kept for the life of the process; a no is asked again after 60 seconds (machine-mode) |
| Handler result | Categorize and tag handler | Job worker | one-way | The validated `{ category, tags, confidence? }` object returned from the handler |
| Step result | `jobs.step.ai` or `jobs.step.script` handler | Job worker | one-way | `{ output, toolCalls }` or `{ output, exitCode }`, reported on complete with the step's usage |
| Acting token | Backend claim response (`actingToken`) | `jobs.step.ai` tool loop | one-way | The bearer on `/mcp`, valid only while the lease holds; never logged or shipped |
| Machine capabilities | Handler registry, provider probes | Backend claim request | one-way | `{ jobTypes, providers, scripts }`, rebuilt and sent with every claim in machine mode |

