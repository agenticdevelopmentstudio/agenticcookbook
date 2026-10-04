
| Term | Definition |
|------|-----------|
| Node | A single running instance of this worker |
| Job | A unit of work queued on the backend, identified by a UUID `id` and a string `type` |
| Claim | The act of atomically reserving one or more jobs for exclusive processing |
| Lease | A server-managed time window during which the node has exclusive ownership of a claimed job |
| Heartbeat | A periodic renewal call that extends the current lease |
| Handler | A function registered for a specific job type that accepts a typed payload and returns a typed result |
| Dead-letter | A terminal failure state the backend applies after a job exceeds its max retry attempts |
| LLM backend | The inference provider a handler uses: a local model server, a hosted API, or a CLI tool |

