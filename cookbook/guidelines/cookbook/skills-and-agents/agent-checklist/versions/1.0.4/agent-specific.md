
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| A01 | `name` and `description` frontmatter present | Agent .md file has both fields | FAIL |
| A02 | Tool access appropriately restricted | `tools` or `disallowedTools` limits access for specialized agents | WARN |
| A03 | `model` field specified if beneficial | Agent benefits from a specific model for its task | INFO |
| A04 | System prompt is clear and focused | Markdown body gives the agent a clear role and scope | WARN |
| A05 | `permissionMode` set appropriately | `plan` for read-only agents, `bypassPermissions` for fully automated | WARN |
| A06 | `maxTurns` set for bounded tasks | Simple agents that should finish quickly have a turn limit | WARN |
| A07 | `skills` lists preloaded skills if needed | Agent that needs domain knowledge has relevant skills preloaded | INFO |
| A08 | `memory` scope appropriate | If agent accumulates knowledge, memory is scoped correctly | INFO |

