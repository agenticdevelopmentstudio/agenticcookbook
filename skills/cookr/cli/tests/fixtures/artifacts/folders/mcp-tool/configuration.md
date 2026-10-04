
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

