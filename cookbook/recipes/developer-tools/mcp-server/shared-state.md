
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Negotiated protocol revision | Server `initialize` response | Host + every subsequent request | two-way | JSON-RPC `initialize` handshake; both sides agree on a dated revision (default 2025-11-25) |
| Negotiated capabilities | Server `initialize` response | Host (decides which lists/calls to send) | one-way | `capabilities` object declaring `tools`/`resources`/`prompts` actually implemented |
| Tool catalog (name → definition) | Each registered `mcp-tool` ingredient | Host (routing) + dispatcher | one-way | `tools/list` response; dispatcher matches `tools/call` `name` to a registered tool |
| Tool-definition hash | Tool catalog at approval time | Host approval store (rug-pull check) | one-way | Hash over name + description + input/output schema + annotations; re-checked on every `tools/list` |
| Per-request access token | Host (Streamable HTTP `Authorization` header) | Server auth layer + per-call authorization | one-way | OAuth 2.1 bearer token; audience-validated, never passed through to downstream |
| Tool result / structuredContent | Tool handler | Host (model context + application) | one-way | `tools/call` result with `content` array and, when `outputSchema` is declared, a conforming `structuredContent` value |
| Opaque state handle (if any) | A stateful tool's result | A later `tools/call` argument | two-way | High-entropy, bounded-lifetime identifier; re-authorized on each call (no protocol session) |

