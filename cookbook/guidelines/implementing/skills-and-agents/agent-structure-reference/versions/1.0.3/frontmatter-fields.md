
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | filename | Display name for the agent |
| `description` | string | — | When to use this agent; helps Claude select the right agent |
| `tools` | list | all tools | Allowlist of tools the agent can use |
| `disallowedTools` | list | none | Denylist of tools (mutually exclusive with `tools`) |
| `model` | string | parent model | Override the model for this agent |
| `permissionMode` | string | inherit | `plan` (read-only), `bypassPermissions` (no prompts), or inherit from parent |
| `maxTurns` | number | unlimited | Maximum turns before the agent stops |
| `skills` | list | none | Skills preloaded into the agent's context |
| `mcpServers` | list | none | MCP servers available to the agent |
| `hooks` | object | — | Lifecycle hooks |
| `memory` | string | — | Memory scope for the agent |
| `background` | boolean | `false` | Whether the agent runs in the background |
| `effort` | string | inherit | Override effort level |
| `isolation` | string | — | Set to `worktree` for git worktree isolation |

