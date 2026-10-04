---
id: 355028de-c329-48dd-b609-41aba903e01c
title: "MCP tool input validation"
domain: agenticdevelopercookbook://guidelines/implementing/security/mcp-input-validation
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Treat every MCP tool argument as untrusted model-supplied input: schema-validate, authorize per call, and bound resource access."
platforms: []
tags:
  - mcp
  - security
  - validation
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
  - agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security
references:
  - https://modelcontextprotocol.io/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ai-api-integration
  - input-handling
  - security-review
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
