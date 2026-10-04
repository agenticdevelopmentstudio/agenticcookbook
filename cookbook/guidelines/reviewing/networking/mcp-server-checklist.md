---
id: 555d659d-6272-4ad3-90f7-3efc8ee6031e
title: "MCP server review checklist"
domain: agenticdevelopercookbook://guidelines/reviewing/networking/mcp-server-checklist
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-merge checklist a reviewer runs over an MCP server's primitive design, tool contracts, and authorization."
platforms: []
tags:
  - mcp
  - review
  - checklist
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
  - agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security
references:
  - https://modelcontextprotocol.io/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - code-review
  - security-review
---

# MCP server review checklist

Run this before merging any Model Context Protocol (MCP) server change. Verify each item against the diff and the running server. Pin to MCP spec revision **2025-06-18** (tools, primitives) and **2025-11-25** (authorization). Mark items you cannot verify as blocking, not as passes.

## Primitive design

- **primitive-by-purpose**: Each capability **MUST** use the primitive that matches its purpose — *resources* for read-only context the client/user selects, *prompts* for user-initiated templated workflows, *tools* for model-controlled actions with side effects. Reviewer **MUST** reject a tool that only returns static data (should be a resource).
- **no-overlap**: The same data **SHOULD NOT** be exposed redundantly across primitives without a stated reason.

## Tool contracts

- **precise-names**: Tool `name` values **MUST** be unique, stable, and action-oriented; renaming a tool is a breaking change and **MUST** be called out in the PR.
- **descriptions-grounded**: Each `description` **MUST** state what the tool does, its side effects, and when to call it — and **MUST NOT** contain hidden instructions, embedded credentials, or text that steers the model beyond the tool's function.
- **input-schema**: Every tool **MUST** define an `inputSchema` (JSON Schema) with typed properties and a `required` list. Free-form string bags are a reject.
- **output-schema-and-structured**: Tools returning structured data **SHOULD** declare an `outputSchema` and return `structuredContent` conforming to it; for backward compatibility the server **SHOULD** also serialize that JSON into a text content block.
- **error-channel-correct**: Tool *execution* failures (API down, business-rule violation) **MUST** be returned in the result with `isError: true`, so the model can see and react. *Protocol* failures (unknown tool, malformed arguments) **MUST** be JSON-RPC errors. Reviewer **MUST** reject a server that swallows execution errors into a 200 with no `isError`, or that raises protocol errors for ordinary tool failures.
- **annotations-set**: Each tool **SHOULD** set the four behavior annotations honestly: `readOnlyHint`, `destructiveHint` (default true when not read-only), `idempotentHint` (default false), `openWorldHint` (default true). These are advisory hints — clients **MUST** treat them as untrusted from untrusted servers, so they are documentation, not enforcement.

## Security

- **arguments-validated-and-authorized**: The handler **MUST** re-validate every argument against the schema server-side and **MUST** enforce per-call authorization before acting. Schema validation is not authorization.
- **injection-safe**: Arguments flowing into shells, SQL, paths, or URLs **MUST** be parameterized/escaped. Shell injection and path traversal were the most-filed MCP CVE classes in early 2026 — grep the diff for string-concatenated commands and unbounded path joins.
- **audience-validated**: For HTTP transports the server acts as an OAuth 2.1 **resource server** and **MUST** validate that each access token was issued specifically for it (audience claim per RFC 8707 / RFC 9068), rejecting tokens for other resources with HTTP 401.
- **no-token-passthrough**: The server **MUST NOT** forward a client-presented token to an upstream API. Calls to upstream services **MUST** use a separate token the server obtained as its own OAuth client. Passthrough creates a confused-deputy exfiltration path and is explicitly forbidden.
- **resource-server-metadata**: The server **MUST** implement OAuth 2.0 Protected Resource Metadata (RFC 9728) — advertise `authorization_servers`, return `WWW-Authenticate` with `resource_metadata` (and a `scope` hint) on 401, and serve the well-known document.
- **rug-pull-mitigation**: Because a server can silently change a tool's name/description/schema after first approval, any client-side or gateway approval the change relies on **MUST** be bound to a hash of the tool's content (name + description + schema), so a later mutation re-triggers consent. Reviewer **MUST** confirm tool definitions are stable or version-bumped, not silently edited.
- **transport-config**: STDIO servers **MUST** read credentials from the environment (not the OAuth flow). HTTP servers **MUST** serve all endpoints over HTTPS, require `Authorization: Bearer` on every request, and **MUST NOT** accept tokens in the query string.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
