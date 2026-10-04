
- **No-parameter tools**: A tool that takes no arguments MUST still declare an `inputSchema`. Prefer `{ "type": "object", "additionalProperties": false }` so the schema explicitly accepts only the empty object.
- **Structured vs. unstructured content**: A tool with an `outputSchema` SHOULD return both `structuredContent` and a serialized text `content` block; clients that predate structured content fall back to the text block, while newer clients consume the typed object.
- **Name collisions across servers**: Names are unique only within a single server. A host or proxy aggregating tools from multiple servers MUST disambiguate (e.g. prefix with a server identifier) — the server's own name is not guaranteed unique and MUST NOT be relied on for this.
- **Stateful operations**: MCP has no protocol-level session. A tool that needs cross-call state MUST return an explicit handle (an opaque, high-entropy, bounded-lifetime identifier) and accept it as an argument on later calls; calls against an expired or unknown handle MUST return `isError: true` so the model can recover.
- **Sensitive parameters and headers**: Parameters carrying secrets (passwords, API keys, tokens, PII) MUST NOT be marked with the `x-mcp-header` extension, since header values are visible to network intermediaries on the Streamable HTTP transport.
- **Untrusted annotations**: Because annotations may be wrong, a host that uses them to gate confirmation (e.g. always confirm when `destructiveHint` is true) MUST still apply its own policy and SHOULD show tool inputs to the user before invocation.

