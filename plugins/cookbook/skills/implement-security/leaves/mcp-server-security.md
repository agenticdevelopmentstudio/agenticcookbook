<!-- leaf: implement-security/mcp-server-security · source: guidelines/implementing/security/mcp-server-security.md -->

**Rules** (cite as `implement-security/mcp-server-security#<slug>`):

- `authorization-carries-normative-statements-below` MUST — A Model Context Protocol (MCP) server exposes tools, resources, and prompts to an AI agent over an untrusted boundary: …
- `server-not-treat-own-tool-descriptions` MUST — The server MUST NOT treat its own tool descriptions, parameter schemas, or returned results as trusted instructions to …
- `external-user-data-returned-clearly-delimited-data` MUST — Tool results that contain external/user data MUST be returned as clearly delimited data, and the server SHOULD strip or …
- `server-keep-tool-descriptions-stable` SHOULD — The server SHOULD keep tool descriptions stable and side-effect-free; surface side effects in the schema, not in prose …
- `approval-tool-approval-bound-hash-tool-full` SHOULD — When a host binds user approval to a tool, that approval SHOULD be bound to a hash of the tool's full content (name, …
- `server-version-tool-definitions-avoid` SHOULD — The server SHOULD version tool definitions and avoid silent semantic changes; changing behavior without a version bump …
- `server-not-accept-token-explicitly-issued` MUST — The server MUST NOT accept any token that was not explicitly issued for it (validate the aud/audience per RFC 8707 …
- `server-not-pass-received-token-through` MUST — The server MUST NOT pass a received token through to a downstream API ("token passthrough" is explicitly forbidden). To …
- `server-validate-inbound-token-before` MUST — The server MUST validate every inbound token before processing the request and reject ones lacking it in the audience.
- `proxy-server-implement-per-client-consent` MUST — A proxy server MUST implement per-client consent: maintain a registry of approved client_id values and check it before …
- `level-consent-page-identify-requesting-client-show` MUST — The MCP-level consent page MUST identify the requesting client, show the third-party scopes and the exact registered …
- `redirect-uri-validated-exact-string-match` MUST — redirect_uri MUST be validated by exact string match (no wildcards). The state value MUST be cryptographically random, …
- `servers-implement-authorization-verify-inbound-requests-use` MUST — Servers that implement authorization MUST verify all inbound requests and MUST NOT use sessions for authentication.
- `session-ids-non-deterministic-csprng-generated` MUST — Session IDs MUST be non-deterministic (CSPRNG-generated, e.g. UUIDv4); avoid sequential or guessable IDs.
- `session-scoped-data-keyed-user-id-session` SHOULD — Session-scoped data SHOULD be keyed as <user_id>:<session_id>, binding the session to identity derived from the token …
- `server-side-deployments-consider-ssrf-apply-mitigations` MUST — Server-side deployments MUST consider SSRF and apply mitigations when fetching OAuth-related URLs.
- `they-require-https-loopback-excepted` SHOULD — They SHOULD require HTTPS (loopback excepted for dev), block private/reserved ranges (10/8, 172.16/12, 192.168/16, …

# MCP server security

A Model Context Protocol (MCP) server exposes tools, resources, and prompts to an AI agent over an untrusted boundary: tool descriptions and tool outputs flow straight into the model's context, and remote servers participate in OAuth flows. Treat every string the server emits as model-influencing input and every token it receives as untrusted. Pin guidance to the MCP spec revision dated **2025-06-18** (Security Best Practices + Authorization), which carries the normative MUST/MUST NOT statements below.

## Threat classes

| Class | Vector | Core mitigation |
|-------|--------|-----------------|
| Tool poisoning | Malicious instructions embedded in a tool's `description`/schema | Treat descriptions as untrusted content; surface them for human review |
| Output prompt injection | Attacker-controlled data returned in tool **results** | Label tool output as data, not instructions; sanitize/escape before returning |
| Rug-pull (tool redefinition) | Tool changes its behavior/description after initial approval | Bind user approval to a hash of the tool's content |
| Confused deputy | OAuth proxy reuses a static client ID + consent cookie | Per-client consent before forwarding to third-party authz |
| Token passthrough | Server forwards client-supplied tokens downstream | FORBIDDEN; reject tokens not issued for this server |
| Session hijacking | Guessed/stolen session ID impersonates a client | Non-deterministic IDs bound to user identity; never authenticate via session |
| SSRF | Malicious discovery URLs point at internal/metadata hosts | Validate/allowlist OAuth discovery URLs; block private ranges |

## Tool definitions and output

- The server **MUST NOT** treat its own tool descriptions, parameter schemas, or returned results as trusted instructions to the agent; an attacker who controls any of these is attempting tool poisoning or output injection.
- Tool results that contain external/user data **MUST** be returned as clearly delimited data, and the server **SHOULD** strip or neutralize embedded directives (e.g., "ignore previous instructions") before returning them.
- The server **SHOULD** keep tool descriptions stable and side-effect-free; surface side effects in the schema, not in prose meant to steer the model.

## Rug-pull / tool redefinition

A server (or a tool it proxies) can present a benign description at approval time and a malicious one later.

- When a host binds user approval to a tool, that approval **SHOULD** be bound to a hash of the tool's full content (name, description, input schema). Any change re-triggers consent.
- The server **SHOULD** version tool definitions and avoid silent semantic changes; changing behavior without a version bump defeats hash-bound approval.
- ACCURACY NOTE: the publicized "MCPoison"/"CurXecute" CVEs were CLIENT-side bugs in an IDE and have been patched. Retain the rug-pull threat class and the hash-bound-approval mitigation; do not cite those CVEs as motivation for server authoring.

## Authorization: token audience and passthrough

Treat a remote MCP server as an OAuth 2.1 **resource server**.

- The server **MUST NOT** accept any token that was not explicitly issued for it (validate the `aud`/audience per RFC 8707 resource indicators).
- The server **MUST NOT** pass a received token through to a downstream API ("token passthrough" is explicitly forbidden). To call a downstream service, use a token-exchange flow to obtain a distinct token, or act as its own client.
- The server **MUST** validate every inbound token before processing the request and reject ones lacking it in the audience.

## Confused deputy (OAuth proxy servers)

When the server proxies a third-party API using a static client ID, a stale consent cookie lets an attacker skip the consent screen.

- A proxy server **MUST** implement per-client consent: maintain a registry of approved `client_id` values and check it **before** initiating the third-party flow.
- The MCP-level consent page **MUST** identify the requesting client, show the third-party scopes and the exact registered `redirect_uri`, and apply CSRF protection.
- `redirect_uri` **MUST** be validated by exact string match (no wildcards). The `state` value **MUST** be cryptographically random, single-use, short-lived, and set only after consent is approved.

## Session hijacking

- Servers that implement authorization **MUST** verify all inbound requests and **MUST NOT** use sessions for authentication.
- Session IDs **MUST** be non-deterministic (CSPRNG-generated, e.g. UUIDv4); avoid sequential or guessable IDs.
- Session-scoped data **SHOULD** be keyed as `<user_id>:<session_id>`, binding the session to identity derived from the token (not client-supplied), so a guessed ID cannot impersonate another user.

## SSRF via OAuth discovery

A malicious server can populate discovery fields (`resource_metadata`, `authorization_servers`, `token_endpoint`) with internal URLs.

- Server-side deployments **MUST** consider SSRF and apply mitigations when fetching OAuth-related URLs.
- They **SHOULD** require HTTPS (loopback excepted for dev), block private/reserved ranges (`10/8`, `172.16/12`, `192.168/16`, `169.254/16`, `127/8`, `fc00::/7`, `fe80::/10`), and validate redirect targets per hop.
- Prefer an egress proxy and DNS-pinning over hand-rolled IP parsing, which misses octal/hex/IPv4-mapped-IPv6 encodings.
