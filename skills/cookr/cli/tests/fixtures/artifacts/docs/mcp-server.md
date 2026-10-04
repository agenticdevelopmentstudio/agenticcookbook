---
id: ad61ee7f-47cf-4c48-a17a-9d7d3d6b7116
title: "MCP server"
domain: agenticdevelopercookbook://recipes/developer-tools/mcp-server
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: "2026 Mike Fullerton"
license: MIT
summary: "Compose one or more MCP tools into a working Model Context Protocol server with chosen primitives, transport, capability negotiation, and OAuth resource-server auth"
platforms:
  - typescript
  - python
tags:
  - mcp
  - ai
  - infrastructure
ingredients:
  - agenticdevelopercookbook://ingredients/developer-tools/mcp-tool
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
  - agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security
  - agenticdevelopercookbook://guidelines/reviewing/networking/mcp-server-checklist
references:
  - https://modelcontextprotocol.io/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
---

# MCP server

## Overview

A Model Context Protocol (MCP) server exposes capabilities to a language-model host such as Claude or ChatGPT by composing one or more MCP tools (and, optionally, resources and prompts) behind a single transport and a single capability-negotiation handshake. This recipe wires the `mcp-tool` ingredient into a coherent, deployable server: it selects the protocol primitives by purpose, declares structured output where tools return typed data, chooses a transport (stdio for a local subprocess, Streamable HTTP for a remote service), negotiates capabilities and the protocol revision during initialization, and — for any remote server — authenticates as an OAuth 2.1 resource server with audience validation, no token passthrough, and rug-pull mitigation through hashed approval of tool definitions. Use this recipe whenever you need to take one or more discrete operations and make them invocable by an LLM host over the wire, rather than just defining the operations in the abstract.

All protocol and transport guidance here is pinned to the MCP specification revision dated **2025-11-25** (the stable revision for the protocol lifecycle, capabilities, and transports). Authorization and security guidance is pinned to the revision dated **2025-06-18** (Authorization + Security Best Practices), which carries the normative MUST/MUST NOT statements for OAuth resource servers. Any release-candidate or draft revision is treated as a forecast and MUST be gated behind explicit opt-in rather than assumed.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| MCP tool | `agenticdevelopercookbook://ingredients/developer-tools/mcp-tool` | Each model-invocable operation the server exposes over `tools/list` and `tools/call` | Yes | One instance per tool. Each configures `name`, `description`, `inputSchema`, optional `outputSchema`, and behavior-hint `annotations`. At least one tool MUST be registered for the server to declare the `tools` capability. |

## Integration Requirements

- **at-least-one-tool**: The server MUST register at least one `mcp-tool` ingredient and expose it through `tools/list` and `tools/call`. A server that declares the `tools` capability MUST return every registered tool's name, description, `inputSchema`, optional `outputSchema`, and `annotations` on `tools/list`, and MUST route each `tools/call` to the matching tool by its unique `name`.
- **choose-primitives-by-purpose**: The server MUST select protocol primitives by the purpose of each capability, not by convenience. Model-invocable operations with side effects MUST be `tools` (chosen by the model). Read-only contextual data the application attaches to context MUST be `resources` (application-controlled, addressed by URI). Reusable, user-initiated interaction templates MUST be `prompts` (user-controlled). A capability MUST NOT be exposed as a tool merely to make it model-callable when it is in fact passive context.
- **declare-structured-output**: For every tool that returns typed data, the server MUST declare an `outputSchema` on the tool and MUST return a `structuredContent` value that validates against it, and SHOULD also serialize that value into a text `content` block for clients that do not consume structured content. A tool that cannot produce conforming output MUST return a result with `isError: true` rather than malformed `structuredContent`.
- **select-transport-by-deployment**: The server MUST choose exactly one transport per deployment. It MUST use the **stdio** transport when running as a local subprocess of the host (no network surface, no auth), and MUST use the **Streamable HTTP** transport when running as a remote service. The deprecated HTTP+SSE transport MUST NOT be used for new servers; Streamable HTTP supersedes it.
- **negotiate-capabilities-and-revision**: The server MUST complete the `initialize` handshake before serving any other request, MUST negotiate the protocol revision (defaulting to **2025-11-25**) rather than hard-coding it, and MUST declare only the capabilities it actually implements (`tools`, and `resources`/`prompts` only if used). The server MUST NOT respond to `tools/call`, `resources/read`, or `prompts/get` before initialization completes.
- **auth-as-oauth-resource-server**: A remote (Streamable HTTP) server MUST act as an OAuth 2.1 **resource server**. It MUST validate every inbound access token before processing the request and MUST reject any request lacking a valid token with `401 Unauthorized` plus a `WWW-Authenticate` header pointing at its protected-resource metadata. The stdio transport, having no network surface, MUST NOT implement this and inherits the trust of the local host.
- **validate-token-audience**: The server MUST validate the token audience per RFC 8707 resource indicators and MUST reject any token whose `aud` does not name this server. A token issued for a different resource MUST NOT be accepted, even if it is otherwise valid and unexpired.
- **no-token-passthrough**: The server MUST NOT forward a received access token to a downstream API. To call a downstream service it MUST obtain a distinct token via a token-exchange flow or act as its own client; passing the inbound token through ("token passthrough") is explicitly forbidden and creates a confused-deputy vulnerability.
- **rug-pull-hashed-approval**: When a host or proxy persists user approval of a tool, the approval MUST be bound to a hash of the tool's full definition (name, description, `inputSchema`, `outputSchema`, `annotations`). If a server later mutates a previously approved tool definition, the hash MUST no longer match and the change MUST require fresh user approval, mitigating the rug-pull threat class where an approved tool silently redefines itself.
- **authorize-per-call**: When the server is authenticated, every tool invocation MUST be authorized against the caller's per-request credentials and scopes. There is no implicit per-connection session; a state handle passed as an argument MUST be re-authorized on each call, since a handle is a name and not a capability.
- **treat-tool-strings-as-untrusted**: The server MUST treat every tool description and tool result it emits as model-influencing input. Tool output that embeds external or user-derived content SHOULD NOT be interpreted by the server as instructions, and the server MUST validate all tool arguments against each tool's `inputSchema` before execution (delegated to the `mcp-tool` ingredient's `arguments-untrusted-and-validated` requirement).

## Layout

The server is the composition point: the host speaks the protocol to the server over one transport, and the server dispatches each request to the appropriate primitive. Tools are the primary primitive; resources and prompts are optional and chosen by purpose.

```
                         protocol (JSON-RPC 2.0)
                    revision negotiated at initialize
                          default: 2025-11-25
  ┌──────────────┐  ───────────────────────────────▶  ┌────────────────────────────┐
  │  LLM Host    │   initialize / capabilities         │        MCP Server          │
  │ (Claude,     │   tools/list, tools/call            │                            │
  │  ChatGPT,    │   resources/list, resources/read    │  ┌──────────────────────┐  │
  │  IDE agent)  │   prompts/list, prompts/get         │  │ capability negotiation│  │
  │              │  ◀───────────────────────────────  │  │ + protocol revision   │  │
  └──────┬───────┘   results / structuredContent       │  └──────────┬───────────┘  │
         │           JSON-RPC errors                   │             │              │
         │                                             │   ┌─────────▼──────────┐   │
   transport (one of):                                 │   │  request dispatch  │   │
   ┌─────────────────────┐                             │   └──┬─────────┬───────┘   │
   │ stdio (local subproc)│  no network, no auth        │      │         │           │
   │   — or —             │                             │   tools/    resources/    │
   │ Streamable HTTP      │  OAuth 2.1 resource server  │   call      prompts        │
   │   (remote service)   │  validate aud, no passthru  │      │         │           │
   └─────────────────────┘                             │  ┌───▼───┐ ┌───▼────────┐   │
                                                        │  │ MCP   │ │ resources  │   │
   For Streamable HTTP only:                            │  │ tool  │ │ / prompts  │   │
   ┌───────────────────────────────┐                    │  │ #1..N │ │ (optional) │   │
   │ Authorization Server (OAuth)  │◀── token issuance  │  └───┬───┘ └────────────┘   │
   │ issues aud-scoped tokens      │                    │      │ per-call authorize  │
   └───────────────────────────────┘                    │      ▼ + schema validate   │
                                                         │  downstream API (distinct  │
                                                         │  token via exchange, never │
                                                         │  the inbound token)        │
                                                         └────────────────────────────┘
```

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Negotiated protocol revision | Server `initialize` response | Host + every subsequent request | two-way | JSON-RPC `initialize` handshake; both sides agree on a dated revision (default 2025-11-25) |
| Negotiated capabilities | Server `initialize` response | Host (decides which lists/calls to send) | one-way | `capabilities` object declaring `tools`/`resources`/`prompts` actually implemented |
| Tool catalog (name → definition) | Each registered `mcp-tool` ingredient | Host (routing) + dispatcher | one-way | `tools/list` response; dispatcher matches `tools/call` `name` to a registered tool |
| Tool-definition hash | Tool catalog at approval time | Host approval store (rug-pull check) | one-way | Hash over name + description + input/output schema + annotations; re-checked on every `tools/list` |
| Per-request access token | Host (Streamable HTTP `Authorization` header) | Server auth layer + per-call authorization | one-way | OAuth 2.1 bearer token; audience-validated, never passed through to downstream |
| Tool result / structuredContent | Tool handler | Host (model context + application) | one-way | `tools/call` result with `content` array and, when `outputSchema` is declared, a conforming `structuredContent` value |
| Opaque state handle (if any) | A stateful tool's result | A later `tools/call` argument | two-way | High-entropy, bounded-lifetime identifier; re-authorized on each call (no protocol session) |

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

## Edge Cases

- **Zero registered tools**: A server with no tools MUST NOT declare the `tools` capability. If it also exposes no resources or prompts, it has nothing to offer and SHOULD fail fast at startup with a clear error rather than completing a useless handshake.
- **Tool name collision across composed sources**: Names are unique only within a single server. A server that aggregates tools from multiple sources (or a host proxy combining several servers) MUST disambiguate, since the server's own name is not guaranteed unique and MUST NOT be relied on for routing.
- **Transport mismatch**: A server started for stdio MUST NOT attempt to bind a network port, and a Streamable HTTP server MUST NOT skip its auth layer. Configuring auth on a stdio transport is a misconfiguration — the local host's trust boundary already applies.
- **Revision downgrade**: If the host requests an older protocol revision than the server's default, the server MAY accept it only if it implements that revision; otherwise it MUST fail the `initialize` rather than silently misbehaving. A release-candidate or draft revision MUST be treated as a forecast and gated behind explicit opt-in.
- **Token valid but wrong audience**: A token that is structurally valid and unexpired but issued for another resource MUST be rejected (validate-token-audience). Accepting it would make this server a confused deputy for the audience the token was actually minted for.
- **Approved tool silently mutated (rug-pull)**: A server that changes a previously approved tool's definition MUST cause the host's hashed approval to fail to match, forcing re-approval. The host MUST NOT carry forward approval across a definition change.
- **Stateful tool with expired handle**: A tool that issues an opaque state handle MUST return `isError: true` (not a protocol error) when called with an expired or unknown handle, so the model can recover by re-establishing state. The handle MUST be re-authorized on each call.
- **Downstream API failure**: When a tool's downstream call fails, the server MUST surface it as a tool-level `isError: true` result the model can act on, not as a JSON-RPC protocol error, and MUST NOT leak downstream credentials or internal stack traces into the result.
- **Capability declared but unimplemented**: A server MUST NOT declare a capability it does not implement; doing so causes the host to send requests the server cannot serve. Declared capabilities MUST match the actual dispatcher.

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

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [no-token-passthrough](agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security) | partial | Security |
| [validate-token-audience](agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security) | partial | Security |
| [rug-pull-hashed-approval](agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security) | partial | Security |
| [mcp-server-checklist](agenticdevelopercookbook://guidelines/reviewing/networking/mcp-server-checklist) | partial | Review |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete server implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
