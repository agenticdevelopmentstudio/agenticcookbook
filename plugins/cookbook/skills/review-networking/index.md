# review-networking — leaves

- [`implement-networking/rate-limiting`](../implement-networking/leaves/rate-limiting.md) — Rate Limiting · Respect server rate limits. Handle 429 responses gracefully. · triggers: api-integration, networking · rules: 1 MUST 1 SHOULD
- [`implement-networking/timeouts`](../implement-networking/leaves/timeouts.md) — Timeouts · Always set both connection and read timeouts. Never use infinite timeouts. · triggers: api-integration, networking · rules: 1 MUST
- [`review-networking/mcp-server-checklist`](leaves/mcp-server-checklist.md) — MCP server review checklist · Pre-merge checklist a reviewer runs over an MCP server's primitive design, tool contracts, and authorization. · triggers: code-review, security-review · rules: 13 MUST 2 SHOULD
- [`review-networking/observable-behavior-contract`](leaves/observable-behavior-contract.md) — Hyrum's Law: all observable behavior becomes contract · Treat every observable behavior of an interface as a contract a consumer may depend on: document guarantees, constrain incidental behavior, and never depend on the unspecified. · triggers: api-integration, code-review · rules: 1 MUST 9 SHOULD
