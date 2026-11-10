
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

