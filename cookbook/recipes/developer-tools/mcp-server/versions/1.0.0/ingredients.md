
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| MCP tool | `agenticdevelopercookbook://ingredients/developer-tools/mcp-tool` | Each model-invocable operation the server exposes over `tools/list` and `tools/call` | Yes | One instance per tool. Each configures `name`, `description`, `inputSchema`, optional `outputSchema`, and behavior-hint `annotations`. At least one tool MUST be registered for the server to declare the `tools` capability. |

