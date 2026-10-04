
The spec distinguishes two error channels — use both correctly (fail-fast at the right layer).

- **Tool execution errors** (API failure, validation, business-logic): return them **in the result** with `isError: true` and an actionable message. The model sees these and can self-correct.
- **Protocol errors** (unknown tool, malformed request): return a JSON-RPC `error`. The model usually cannot fix these.
- Do not throw a protocol error for a recoverable tool failure — the model loses the signal it needs to retry.

