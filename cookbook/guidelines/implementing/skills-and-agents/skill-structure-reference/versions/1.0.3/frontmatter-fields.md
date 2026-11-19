
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | directory name | Display name and slash-command trigger (kebab-case, lowercase, ≤64 chars) |
| `description` | string | — | When to use this skill; shown in context for auto-invocation matching |
| `argument-hint` | string | — | Hint for expected arguments (e.g., `<path>`, `<issue-number>`) |
| `disable-model-invocation` | boolean | `false` | If `true`, Claude will not auto-invoke; user must use `/name` |
| `user-invocable` | boolean | `true` | If `false`, skill is hidden from slash-command menu (background knowledge only) |
| `allowed-tools` | list | all tools | Restrict which tools the skill can use |
| `model` | string | session model | Override the model for this skill |
| `effort` | string | session effort | Override effort level |
| `context` | string | — | Set to `fork` to run in an isolated subagent context |
| `agent` | string | — | Specify subagent type when using `context: fork` |
| `hooks` | object | — | Lifecycle hooks (preInvoke, postInvoke) |
| `paths` | list | — | Glob patterns limiting auto-activation to matching file paths |
| `shell` | string | `bash` | Shell for inline commands (`bash` or `powershell`) |

