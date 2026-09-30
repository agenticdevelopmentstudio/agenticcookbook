<!-- leaf: ingredients/developer-tools-mcp-tool--states · source: ingredients/developer-tools/mcp-tool.md -->

# MCP tool

## States

| State | Behavior |
|-------|----------|
| Registered | Tool appears in the `tools/list` response with its name, description, `inputSchema`, optional `outputSchema`, and `annotations`; not yet invoked |
| Invoked | Host sends `tools/call` with `name` and `arguments`; server validates arguments against `inputSchema` and authorizes the caller, then executes |
| Returns result | Execution succeeds; server returns a result with a `content` array and, if `outputSchema` is declared, a conforming `structuredContent` value; `isError` is absent or `false` |
| Returns isError | Execution fails recoverably (API error, validation error, business-logic error); server returns a result with `isError: true` and an explanatory `content` block for the model to self-correct |
