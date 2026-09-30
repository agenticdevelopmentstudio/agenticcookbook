<!-- leaf: recipes-developer-tools/mcp-server--part-2 · source: recipes/developer-tools/mcp-server.md -->

# MCP server — continued (part 2)

**Rules** (cite as `recipes-developer-tools/mcp-server--part-2#<slug>`):

- `swiftui` MAY — N/A. An MCP server is invisible infrastructure with no view layer; SwiftUI is a UI framework and is not a server …
- `react-web` MAY — N/A as a server runtime. A web front end MAY be an MCP host UI, but the server itself runs server-side (Node/TypeScript …

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| recipe-001 | at-least-one-tool, negotiate-capabilities-and-revision | Connect a host, send `initialize`, then `tools/list` | Server negotiates a dated revision (default 2025-11-25), declares the `tools` capability, and lists at least one tool with name, description, and `inputSchema` |
| recipe-002 | negotiate-capabilities-and-revision | Send `tools/call` before `initialize` completes | Server refuses the request; tools are not dispatched until initialization finishes |
| recipe-003 | choose-primitives-by-purpose | Inspect a passive contextual dataset the server exposes | It appears under `resources` (URI-addressed), not as a side-effecting tool |
| recipe-004 | declare-structured-output | Call a tool that declares an `outputSchema` with valid arguments | Result includes a `structuredContent` value validating against the schema plus a serialized text `content` block |
| recipe-005 | declare-structured-output | Force a tool that declares an `outputSchema` to produce non-conforming output | Result has `isError: true`; no malformed `structuredContent` is emitted |
| recipe-006 | select-transport-by-deployment | Start the server in local mode | It speaks the stdio transport with no network listener and no auth layer |
| recipe-007 | select-transport-by-deployment | Start the server in remote mode | It serves over Streamable HTTP; the deprecated HTTP+SSE transport is not offered |
| recipe-008 | auth-as-oauth-resource-server | Send a Streamable HTTP request with no `Authorization` header | Server returns `401` with a `WWW-Authenticate` header referencing its protected-resource metadata |
| recipe-009 | validate-token-audience | Send a valid, unexpired token whose `aud` names a different resource | Server rejects the request; the audience mismatch is not accepted |
| recipe-010 | no-token-passthrough | Trigger a tool that calls a downstream API while authenticated | Server uses a distinct, exchanged token downstream; the inbound token is never forwarded |
| recipe-011 | rug-pull-hashed-approval | Approve a tool, then mutate its `description`/`inputSchema` and re-list | Definition hash no longer matches the approval; the host requires fresh user approval before the tool can be called |
| recipe-012 | authorize-per-call | Call an authenticated tool with credentials lacking the required scope | Call is denied per request; authorization is not inherited from a prior call on the same connection |
| recipe-013 | treat-tool-strings-as-untrusted, at-least-one-tool | Call a tool with arguments that violate its `inputSchema` | Arguments are validated before execution; non-conforming input is rejected or reported via `isError: true`, and the handler does not run |

## Platform Notes

- **SwiftUI**: N/A. An MCP server is invisible infrastructure with no view layer; SwiftUI is a UI framework and is not a server runtime. A SwiftUI application MAY act as an MCP *host* that connects to a server, but the server composition described here is authored in TypeScript or Python.
- **Compose**: N/A — same reason as SwiftUI. Jetpack Compose is an Android UI toolkit, not an MCP server runtime. This recipe targets `typescript` and `python` only.
- **React/Web**: N/A as a server runtime. A web front end MAY be an MCP host UI, but the server itself runs server-side (Node/TypeScript or Python), not in the browser.
- **TypeScript (`@modelcontextprotocol/sdk`)**: Create the server with `new McpServer({ name, version })`. Register each `mcp-tool` ingredient with `server.registerTool(name, { description, inputSchema, outputSchema, annotations }, handler)`, returning a result whose `content` array and (when an output schema is declared) `structuredContent` are produced by the handler. For local use, connect a `StdioServerTransport`; for remote use, connect a `StreamableHTTPServerTransport` mounted in an HTTP framework (e.g. Express) behind token-validation middleware that checks the bearer token's audience before the SDK handles the request. The SDK performs the `initialize` handshake and capability negotiation; declare only the capabilities you implement. Treat any pre-release SDK revision as a forecast.
- **Python (`mcp` SDK)**: Use `FastMCP("server-name")` and decorate each `mcp-tool` ingredient's handler with `@mcp.tool()`; the SDK derives `inputSchema` from the function signature and `outputSchema` from the return type annotation, and serializes structured results into both `structuredContent` and a text `content` block. Run with `mcp.run(transport="stdio")` for a local subprocess, or mount the Streamable HTTP app (e.g. via `mcp.streamable_http_app()` behind an ASGI server such as Uvicorn) for a remote service, fronted by middleware that validates the bearer token and its audience. The SDK handles initialization and capability negotiation; pin to the stable revision and gate any release-candidate revision behind explicit opt-in.

## Design Decisions

**Decision**: Make `mcp-tool` the only required ingredient; treat resources and prompts as in-recipe primitive choices rather than separate ingredients.
**Rationale**: A server with no tools has nothing model-invocable to offer, so at least one tool is the floor (yagni — do not require ingredients that may not exist yet). Resources and prompts share the same transport, handshake, and auth surface as tools and are selected by purpose within this recipe; promoting them to separate ingredients now would be speculative structure (design-for-deletion, small-reversible-decisions). They can be extracted into their own ingredients later if their specs grow.
**Approved: pending**

**Decision**: Pin protocol/transport guidance to the 2025-11-25 revision and authorization/security guidance to the 2025-06-18 revision, negotiating the revision at `initialize` rather than hard-coding it.
**Rationale**: The two concern areas stabilized on different dated revisions; citing each to its authoritative revision is explicit-over-implicit and avoids overstating where a single revision governs everything. Negotiating at runtime (rather than baking in a constant) keeps the server portable across hosts and optimizes-for-change as the spec advances. Release-candidate revisions are forecasts and stay behind opt-in to avoid building on unstable ground.
**Approved: pending**
