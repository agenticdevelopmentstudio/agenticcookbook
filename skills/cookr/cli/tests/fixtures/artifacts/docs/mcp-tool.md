---
id: 820b832f-6003-4fc1-b4b4-35cd2d57c2e5
title: "MCP tool"
domain: agenticdevelopercookbook://ingredients/developer-tools/mcp-tool
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: "2026 Mike Fullerton"
license: MIT
summary: "A single Model Context Protocol tool — name, JSON Schema input/output, typed result, error and trust hint annotations"
platforms:
  - typescript
  - python
tags:
  - mcp
  - infrastructure
  - ai
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
  - agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security
references:
  - https://modelcontextprotocol.io/
approved-by: "approve-artifact v1.0.0"
approved-date: 2026-06-09
---

# MCP tool

## Overview

A single Model Context Protocol (MCP) tool — the atomic, model-invocable unit of capability that an MCP server composes and exposes over `tools/list` and `tools/call`. A tool is identified by a unique `name`, carries a `description` the model routes on, and declares a JSON Schema `inputSchema` for its arguments and an optional `outputSchema` for typed results. When invoked, the tool returns a result containing a `content` array (unstructured) and, when an output schema is declared, a `structuredContent` value the calling application can consume directly. A server is just a collection of these tools plus transport; get the tool right and the server follows. Use this ingredient whenever you expose a discrete operation — query a database, call an API, run a computation — to a language-model host such as Claude or ChatGPT.

## Behavioral Requirements

### Identity and routing

- **unique-routable-name**: A tool MUST have a `name` that is unique within its server and stable across versions. Names SHOULD be 1–128 characters and SHOULD use only ASCII letters, digits, underscore, hyphen, and dot — no spaces or special characters. The model and host route on this name, so it MUST NOT collide with another tool on the same server.
- **precise-description**: A tool MUST carry a `description` written for the model, not for a human reader: it MUST state what the tool does, when to use it, and any preconditions, because the host selects tools by matching the user's intent against these descriptions. A tool MAY also carry an optional human-readable `title` for display.

### Schemas

- **input-schema-required**: A tool MUST declare an `inputSchema` that is a valid JSON Schema object (never `null`) describing its arguments. For a tool with no parameters it MUST use `{ "type": "object", "additionalProperties": false }`. Each parameter SHOULD have a `description`, and required parameters MUST be listed in the schema's `required` array. The schema defaults to JSON Schema draft 2020-12 when no `$schema` field is present.
- **output-schema-for-typed-results**: A tool that returns structured data SHOULD declare an `outputSchema` (a valid JSON Schema object) describing the shape of its result. When an `outputSchema` is declared, the server MUST return a `structuredContent` value conforming to it, and SHOULD also serialize that value into a text `content` block for backward compatibility with clients that do not consume structured content.
- **structured-content-conforms**: When a tool declares an `outputSchema`, its result's `structuredContent` MUST validate against that schema. Clients SHOULD validate it on receipt; a server that cannot produce conforming output MUST return a tool execution error rather than malformed structured content.

### Errors

- **tool-errors-via-iserror**: Failures the model can act on — API failures, input-validation failures, business-logic errors — MUST be reported inside the tool result with `isError: true` and a human-and-model-readable explanation in the `content` array, NOT as a protocol-level failure. This lets the model self-correct and retry with adjusted arguments.
- **protocol-errors-via-jsonrpc**: Failures with the request structure itself — unknown tool name, a malformed `tools/call` request, internal server faults — MUST be returned as standard JSON-RPC errors (e.g. code `-32602`), NOT as a result with `isError: true`. Protocol errors signal the model is unlikely to recover by retrying.

### Annotations

- **behavior-hint-annotations**: A tool SHOULD declare `annotations` that describe its behavior so hosts can apply appropriate trust and confirmation policy: `readOnlyHint` (true if the tool only reads and does not modify its environment; default `false`); `destructiveHint` (true if the tool may delete or overwrite rather than only add — meaningful only when `readOnlyHint` is `false`; default `true`); `idempotentHint` (true if repeating the call with the same arguments has no additional effect — meaningful only when `readOnlyHint` is `false`; default `false`); and `openWorldHint` (true if the tool interacts with an open world of external entities such as the public internet or third-party APIs).
- **annotations-are-untrusted-hints**: Annotations are informational signals, not enforceable guarantees. A server MUST set them accurately, and a client MUST treat annotations from untrusted servers as unverified — they MUST NOT be relied on as a security control, since a buggy or malicious server can misdeclare a destructive tool as read-only.

### Argument safety

- **arguments-untrusted-and-validated**: Tool arguments MUST be treated as untrusted input. The server MUST validate every call's arguments against the declared `inputSchema` before executing, and MUST reject or report (via `isError: true`) input that fails validation. Validation MUST NOT be skipped because the model "should" have produced conforming arguments.
- **authorize-per-call**: When the server is authenticated, every invocation MUST be authorized against the caller's per-request credentials and scopes — there is no implicit per-connection session. State handles passed as arguments MUST be re-authorized on each call; a handle is a name, not a capability.

## Appearance

Not applicable — an MCP tool is invisible infrastructure with no inherent visual surface. The host application, not the tool, decides how invocations are surfaced to the user (e.g. confirmation prompts for tools with `destructiveHint`).

## States

| State | Behavior |
|-------|----------|
| Registered | Tool appears in the `tools/list` response with its name, description, `inputSchema`, optional `outputSchema`, and `annotations`; not yet invoked |
| Invoked | Host sends `tools/call` with `name` and `arguments`; server validates arguments against `inputSchema` and authorizes the caller, then executes |
| Returns result | Execution succeeds; server returns a result with a `content` array and, if `outputSchema` is declared, a conforming `structuredContent` value; `isError` is absent or `false` |
| Returns isError | Execution fails recoverably (API error, validation error, business-logic error); server returns a result with `isError: true` and an explanatory `content` block for the model to self-correct |

## Accessibility

Not applicable — an MCP tool has no user-facing surface. Accessibility of any confirmation or result presentation is owned by the host application that renders tool invocations.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mcp-tool-001 | unique-routable-name, precise-description | Send `tools/list` | Tool appears once with a unique name and a non-empty, intent-describing `description` |
| mcp-tool-002 | input-schema-required | Inspect the tool's `inputSchema` | A valid JSON Schema object (not `null`); a no-parameter tool uses `{ "type": "object", "additionalProperties": false }` |
| mcp-tool-003 | input-schema-required | Call the tool with an argument that violates the schema | Server rejects it (protocol error) or returns a result with `isError: true`; the handler does not run on invalid input |
| mcp-tool-004 | output-schema-for-typed-results, structured-content-conforms | Call a tool that declares an `outputSchema` with valid arguments | Result includes a `structuredContent` value that validates against `outputSchema`, plus a serialized text `content` block |
| mcp-tool-005 | tool-errors-via-iserror | Call the tool with a future-date-required field set to a past date | Result has `isError: true` and a `content` block explaining the failure; no JSON-RPC error |
| mcp-tool-006 | protocol-errors-via-jsonrpc | Send `tools/call` for a name that does not exist | JSON-RPC error (e.g. code `-32602`, "Unknown tool"); not a result with `isError: true` |
| mcp-tool-007 | behavior-hint-annotations | Inspect the tool's `annotations` | `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` present and consistent with the tool's actual effect |
| mcp-tool-008 | annotations-are-untrusted-hints | Client receives a tool from an untrusted server marked `readOnlyHint: true` | Client does not rely on the hint to skip confirmation for a non-read operation |
| mcp-tool-009 | arguments-untrusted-and-validated | Call the tool with extra, malformed, or injection-style argument values | Arguments are schema-validated before execution; non-conforming input is rejected or reported via `isError: true` |
| mcp-tool-010 | authorize-per-call | Call an authenticated tool with credentials lacking the required scope | Call is denied per request; authorization is not inferred from a prior call on the same connection |

## Edge Cases

- **No-parameter tools**: A tool that takes no arguments MUST still declare an `inputSchema`. Prefer `{ "type": "object", "additionalProperties": false }` so the schema explicitly accepts only the empty object.
- **Structured vs. unstructured content**: A tool with an `outputSchema` SHOULD return both `structuredContent` and a serialized text `content` block; clients that predate structured content fall back to the text block, while newer clients consume the typed object.
- **Name collisions across servers**: Names are unique only within a single server. A host or proxy aggregating tools from multiple servers MUST disambiguate (e.g. prefix with a server identifier) — the server's own name is not guaranteed unique and MUST NOT be relied on for this.
- **Stateful operations**: MCP has no protocol-level session. A tool that needs cross-call state MUST return an explicit handle (an opaque, high-entropy, bounded-lifetime identifier) and accept it as an argument on later calls; calls against an expired or unknown handle MUST return `isError: true` so the model can recover.
- **Sensitive parameters and headers**: Parameters carrying secrets (passwords, API keys, tokens, PII) MUST NOT be marked with the `x-mcp-header` extension, since header values are visible to network intermediaries on the Streamable HTTP transport.
- **Untrusted annotations**: Because annotations may be wrong, a host that uses them to gate confirmation (e.g. always confirm when `destructiveHint` is true) MUST still apply its own policy and SHOULD show tool inputs to the user before invocation.

## Configuration

The following configure a single tool at registration time. Values map to MCP `Tool` fields, not to a separate config system.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | (required) | Unique, stable identifier the model and host route on |
| `title` | string | (none) | Optional human-readable display name |
| `description` | string | (required) | Model-facing explanation of what the tool does and when to use it |
| `inputSchema` | JSON Schema object | (required) | Schema for arguments; `{ "type": "object", "additionalProperties": false }` for no-parameter tools |
| `outputSchema` | JSON Schema object | (none) | Optional schema describing `structuredContent`; when set, results MUST conform |
| `readOnlyHint` | boolean | `false` | True if the tool only reads and does not modify its environment |
| `destructiveHint` | boolean | `true` | True if the tool may delete or overwrite (meaningful only when `readOnlyHint` is false) |
| `idempotentHint` | boolean | `false` | True if repeating with identical arguments has no additional effect (meaningful only when `readOnlyHint` is false) |
| `openWorldHint` | boolean | (unset) | True if the tool interacts with an open world of external entities |

## Logging

Subsystem: `{{server_id}}` | Category: `mcp.tool`

A tool SHOULD log each invocation for audit purposes without recording sensitive argument or result values. Redact secrets and PII before logging.

| Event | Level | Message |
|-------|-------|---------|
| Tool registered | debug | `mcp.tool: registered "{{tool_name}}" (readOnly={{read_only}})` |
| Invocation received | info | `mcp.tool: "{{tool_name}}" invoked by {{caller}}` |
| Argument validation failed | error | `mcp.tool: "{{tool_name}}" rejected — input failed inputSchema validation` |
| Invocation succeeded | info | `mcp.tool: "{{tool_name}}" returned in {{duration}}ms` |
| Tool execution error | error | `mcp.tool: "{{tool_name}}" returned isError — {{reason}}` |

## Platform Notes

### TypeScript (`@modelcontextprotocol/sdk`)

Use the official TypeScript SDK and register a tool with `registerTool`, supplying a Zod `inputSchema` (validated automatically) and an optional `outputSchema`. The handler returns a `content` array and, when an output schema is declared, a `structuredContent` object.

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "weather", version: "1.0.0" });

server.registerTool(
  "get_weather_data",
  {
    title: "Weather Data Retriever",
    description: "Get current weather for a city. Use when the user asks about weather.",
    inputSchema: { location: z.string().describe("City name or zip code") },
    outputSchema: {
      temperature: z.number().describe("Temperature in celsius"),
      conditions: z.string(),
      humidity: z.number(),
    },
    annotations: {
      readOnlyHint: true,
      openWorldHint: true,
    },
  },
  async ({ location }) => {
    try {
      const data = await fetchWeather(location); // arguments already schema-validated
      return {
        content: [{ type: "text", text: JSON.stringify(data) }],
        structuredContent: data, // validated against outputSchema
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `Weather lookup failed: ${String(err)}` }],
        isError: true, // tool execution error — the model can retry
      };
    }
  },
);
```

The SDK validates incoming `arguments` against `inputSchema` and checks `structuredContent` against `outputSchema` before sending the result. An unknown tool name or malformed request surfaces as a JSON-RPC protocol error automatically.

### Python (`mcp`)

Use the official Python SDK's `FastMCP`. Decorating a function with `@mcp.tool` registers it and generates the `inputSchema` from type hints; an `outputSchema` is generated from the return annotation (or supplied explicitly), and object-like returns become `structuredContent`. Raise inside the handler — or return an error payload — for tool execution errors.

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("weather")

class Weather(BaseModel):
    temperature: float  # celsius
    conditions: str
    humidity: float

@mcp.tool(
    annotations={"readOnlyHint": True, "openWorldHint": True},
)
def get_weather_data(location: str) -> Weather:
    """Get current weather for a city. Use when the user asks about weather."""
    # `location` is already validated against the generated inputSchema.
    data = fetch_weather(location)  # raises -> reported as a tool error
    return Weather(**data)  # returned as structuredContent + a text block
```

Returning a Pydantic model, dataclass, or dict yields `structuredContent` that conforms to the generated `outputSchema`, plus a serialized text block for backward compatibility. Validation failures and handler exceptions are surfaced as tool execution errors; unknown-tool and malformed-request failures are returned as JSON-RPC protocol errors by the framework.

### Other languages

Official MCP SDKs also exist for languages including Kotlin, Java, C#, Go, Ruby, Rust, Swift, and PHP. Each exposes the same `Tool` shape — `name`, `description`, `inputSchema`, optional `outputSchema`, and `annotations` — and the same result contract (`content` array, optional `structuredContent`, `isError`). Prefer the official SDK for the target language over hand-rolling the wire protocol.

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [validate-args-against-schema](agenticdevelopercookbook://guidelines/implementing/security/mcp-input-validation) | partial | Security |
| [tools-untrusted-input](agenticdevelopercookbook://guidelines/implementing/security/mcp-server-security) | partial | Security |
| [structured-output-schema](agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete tool implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
