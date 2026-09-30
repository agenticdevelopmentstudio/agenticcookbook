<!-- leaf: ingredients/developer-tools-mcp-tool · source: ingredients/developer-tools/mcp-tool.md -->

**Rules** (cite as `ingredients/developer-tools-mcp-tool#<slug>`):

- `unique-routable-name` MUST
- `precise-description` MUST
- `input-schema-required` MUST
- `output-schema-for-typed-results` MUST
- `structured-content-conforms` MUST
- `tool-errors-via-iserror` MUST
- `protocol-errors-via-jsonrpc` MUST
- `behavior-hint-annotations` SHOULD
- `annotations-are-untrusted-hints` MUST
- `arguments-untrusted-and-validated` MUST
- `authorize-per-call` MUST

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
