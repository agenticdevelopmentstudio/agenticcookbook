<!-- leaf: recipes-developer-tools/mcp-server · source: recipes/developer-tools/mcp-server.md -->

**Rules** (cite as `recipes-developer-tools/mcp-server#<slug>`):

- `practices-carries-normative-statements-oauth-resource-servers` MUST — All protocol and transport guidance here is pinned to the MCP specification revision dated 2025-11-25 (the stable …
- `at-least-one-tool` MUST
- `choose-primitives-by-purpose` MUST
- `declare-structured-output` MUST
- `select-transport-by-deployment` MUST
- `negotiate-capabilities-and-revision` MUST
- `auth-as-oauth-resource-server` MUST
- `validate-token-audience` MUST
- `no-token-passthrough` MUST
- `rug-pull-hashed-approval` MUST
- `authorize-per-call` MUST
- `treat-tool-strings-as-untrusted` MUST

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

