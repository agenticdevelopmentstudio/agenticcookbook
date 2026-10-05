
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `llmBackendKind` | enum | (required) | One of `openai-compatible` or `cli` |
| `llmBackendUrl` | string | (none) | Endpoint for the `openai-compatible` kind |
| `llmBackendCommand` | string | (none) | Executable for the `cli` kind |
| `llmBackendModel` | string | (backend default) | Model identifier passed to the backend |

