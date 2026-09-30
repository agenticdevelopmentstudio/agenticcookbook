<!-- leaf: implement-security/mcp-input-validation · source: guidelines/implementing/security/mcp-input-validation.md -->

**Rules** (cite as `implement-security/mcp-input-validation#<slug>`):

- `tool-handlers-validate-argument-against-tool` MUST — Tool handlers MUST validate every argument against the tool's declared inputSchema before use, rejecting on mismatch — …
- `handlers-not-trust-argument-because-arrived` MUST — Handlers MUST NOT trust an argument because it arrived through the model; an argument's provenance grants it no …
- `handlers-enforce-authorization-call-against` MUST — Handlers MUST enforce authorization on every call against the authenticated identity, not against anything the model …
- `handlers-sanitize-bound-argument-before` MUST — Handlers MUST sanitize and bound any argument before it reaches a side effect (filesystem, network, DB, shell, …
- `numeric-bounds-root-type-object` MUST — Define inputSchema with explicit type, required, enum, pattern, minLength/maxLength, and numeric bounds; the root MUST …
- `validator-handler-boundary-reject-unknown-properties-additionalproperties` MUST — Validate with a JSON Schema 2020-12 validator at the handler boundary and MUST reject unknown properties …
- `implementations-not-auto-dereference-external-ref` MUST — Implementations MUST NOT auto-dereference external $ref URIs and SHOULD bound schema depth and total validation time to …
- `session-authenticated-identity-not-cache-authorization-decision-across` MUST — Re-check the caller's scopes/permissions on every tool invocation against the session's authenticated identity; MUST …
- `must-not` MUST — forward a client-supplied token to a downstream API without validating its audience (see mcp-server-security …
- `into-model-context-validate-against-outputschema-strip` SHOULD — Tool results flow back into model context — SHOULD validate against outputSchema and strip or label untrusted fetched …
- `raw-argument-payloads-not-log-secrets-full-tokens` MUST — Log validation failures and authorization denials with the tool name and caller identity (not raw argument payloads); …
- `stable-error-code-not-echo-internal-paths-stack` MUST — Return structured, non-leaky errors on rejection — fail closed, surface a stable error code, and MUST NOT echo internal …

# MCP tool input validation

Every argument a Model Context Protocol (MCP) tool handler receives is model-supplied, untrusted input — even when the tool's caller is "your own" agent, the model can be steered by injected content. The model is **not** an authorization boundary. Pin guidance to the MCP spec revision dated **2025-06-18** (tool `inputSchema` is JSON Schema **2020-12**). Pairs with `mcp-server-security`, which covers tool poisoning, token passthrough, and confused-deputy.

## Core rules

- Tool handlers **MUST** validate every argument against the tool's declared `inputSchema` before use, rejecting on mismatch — do not rely on the client or model to have validated.
- Handlers **MUST NOT** trust an argument because it arrived through the model; an argument's provenance grants it no privilege.
- Handlers **MUST** enforce authorization on every call against the authenticated identity, not against anything the model passes.
- Handlers **MUST** sanitize and bound any argument before it reaches a side effect (filesystem, network, DB, shell, downstream API).

## Schema validation

- Define `inputSchema` with explicit `type`, `required`, `enum`, `pattern`, `minLength`/`maxLength`, and numeric bounds; the root **MUST** be `type: object`.
- Validate with a JSON Schema 2020-12 validator at the handler boundary and **MUST** reject unknown properties (`additionalProperties: false`) unless a field is intentionally open.
- Implementations **MUST NOT** auto-dereference external `$ref` URIs and **SHOULD** bound schema depth and total validation time to prevent schema-driven DoS.
- A passing schema check proves shape, not safety — it does **not** neutralize malicious instructions embedded in syntactically valid strings.

## Authorization per call

- Re-check the caller's scopes/permissions on **every** tool invocation against the session's authenticated identity; **MUST NOT** cache an authorization decision across a privilege boundary.
- Scope downstream actions to the least privilege the host-process identity holds; never widen privilege based on a tool argument.
- **MUST NOT** forward a client-supplied token to a downstream API without validating its audience (see `mcp-server-security` token-passthrough rules).

## Bound resource access

- **File paths**: canonicalize (resolve symlinks + `..`) and confine to an allowlisted root; reject paths that escape it. Treat path traversal as a primary attack on file tools.
- **URL arguments**: block SSRF — allowlist schemes/hosts, resolve and reject private, loopback, and link-local IP ranges, and disable redirects to disallowed targets.
- **Database**: use parameterized queries only; scope every query to the authorized tenant/row set — never interpolate an argument into SQL or a query path.
- **Shell/OS**: avoid shell invocation; if unavoidable, pass arguments as an argv array (never a concatenated string) and allowlist the executable.

## Output and observability

- Tool results flow back into model context — **SHOULD** validate against `outputSchema` and strip or label untrusted fetched content so it is not read as instructions.
- Log validation failures and authorization denials with the tool name and caller identity (not raw argument payloads); **MUST NOT** log secrets or full tokens.
- Return structured, non-leaky errors on rejection — fail closed, surface a stable error code, and **MUST NOT** echo internal paths or stack traces.
