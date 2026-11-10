
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| MCP tool | [adc.ingredient.developer-tools.mcp-tool](cookbook:820b832f-6003-4fc1-b4b4-35cd2d57c2e5) | Each model-invocable operation the server exposes over `tools/list` and `tools/call` | Yes | One instance per tool. Each configures `name`, `description`, `inputSchema`, optional `outputSchema`, and behavior-hint `annotations`. At least one tool MUST be registered for the server to declare the `tools` capability. |

