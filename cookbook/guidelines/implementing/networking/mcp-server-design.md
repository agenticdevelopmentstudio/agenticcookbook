---
id: 788f1c1d-69af-4570-a279-748d89fcc0e0
title: "MCP server design"
domain: agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Design MCP servers by choosing the right primitive and giving each tool a precise name, output schema, and annotations."
platforms: []
tags:
  - mcp
  - api
  - ai
depends-on: []
related:
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/fail-fast
references:
  - https://modelcontextprotocol.io/
  - https://modelcontextprotocol.io/specification/draft/server/tools
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://workos.com/blog/mcp-features-guide
  - https://modelcontextprotocol.io/specification/2025-11-25/changelog
  - https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - api-integration
  - ai-api-integration
---

# MCP server design

Guidance for authoring a Model Context Protocol (MCP) server — the side that exposes context and capabilities to an LLM host. (Consuming MCP servers is covered elsewhere.) The model routes on the names, descriptions, and schemas you publish, so treat them as the public contract.

**Pin to a dated spec revision.** Default to the stable **2025-11-25** revision unless the host requires an older one. Negotiate the revision during initialization rather than hard-coding it. Treat any release-candidate or draft revision as a forecast and gate it behind explicit opt-in.

## Choose the right primitive

A server offers three primitives. Pick by purpose, not convenience.

| Primitive | Control model | Use for |
|-----------|---------------|---------|
| **Resource** | App/user-driven | Read-only context the host or user attaches (files, records, docs). No side effects. |
| **Prompt** | User-invoked | Templated, user-triggered workflows (slash commands, canned interactions). |
| **Tool** | Model-driven | Actions and side effects the model decides to invoke (queries, API calls, writes). |

- You **SHOULD** prefer a **resource** for anything read-only that the user or host selects as context.
- You **SHOULD** prefer a **prompt** for workflows a human explicitly invokes.
- You **SHOULD** model **tools** for operations the model chooses autonomously — and only those.
- Do not expose read-only context as a tool merely because tools are easier to wire up; that puts routing load on the model and invites accidental invocation.

## Tool design

The host's model selects tools from their `name` and `description` alone, so these are load-bearing.

- Each tool **MUST** have a precise, action-oriented `name` and a `description` that states what it does, when to use it, and what it returns.
- Tool names **SHOULD** be 1–128 chars, case-sensitive, and limited to `[A-Za-z0-9_.-]` (no spaces). Keep them unique within the server.
- Use the optional `title` for a human-readable display label; keep `name` stable as the machine identifier.
- Define a strict `inputSchema` (JSON Schema, defaults to 2020-12). For zero-parameter tools, use `{ "type": "object", "additionalProperties": false }`.
- Keep the tool surface small. Many overlapping tools degrade routing accuracy; consolidate or parameterize instead.

## Structured output

- A tool **SHOULD** declare an `outputSchema` and return matching `structuredContent`. This gives the model and client typed, validatable results.
- When `outputSchema` is present, the server **MUST** return `structuredContent` conforming to it; clients **SHOULD** validate it. The schema root is restricted to `type: "object"`.
- For backward compatibility, also serialize the structured result as JSON in a `text` content block.
- Sanitize outputs and never leak secrets or internal identifiers the host should not see.

## Error handling

The spec distinguishes two error channels — use both correctly (fail-fast at the right layer).

- **Tool execution errors** (API failure, validation, business-logic): return them **in the result** with `isError: true` and an actionable message. The model sees these and can self-correct.
- **Protocol errors** (unknown tool, malformed request): return a JSON-RPC `error`. The model usually cannot fix these.
- Do not throw a protocol error for a recoverable tool failure — the model loses the signal it needs to retry.

## Annotations (untrusted hints)

Set `annotations` to describe tool behavior so hosts can apply policy. All are hints with defaults; clients **MUST** treat them as untrusted unless the server is trusted.

| Annotation | Default | Meaning |
|------------|---------|---------|
| `readOnlyHint` | `false` | Tool does not modify its environment. |
| `destructiveHint` | `true` | Updates may be destructive (only meaningful when not read-only). |
| `idempotentHint` | `false` | Repeated calls with same args have no additional effect. |
| `openWorldHint` | `true` | Interacts with an open external world (e.g. the web). |

- You **SHOULD** set these accurately; mislabeling a destructive tool as read-only invites unguarded invocation.
- Annotations inform UI and consent flows; they **MUST NOT** be your only safety control. Validate inputs, enforce access control, and rate-limit on the server.

## Security baseline

- Servers **MUST** validate all tool inputs, enforce access controls, rate-limit invocations, and sanitize outputs.
- Assume a human-in-the-loop may gate invocations; write descriptions and errors that make consent decisions clear.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
