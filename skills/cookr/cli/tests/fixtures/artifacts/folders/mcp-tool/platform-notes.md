
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

