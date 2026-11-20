
Set `annotations` to describe tool behavior so hosts can apply policy. All are hints with defaults; clients **MUST** treat them as untrusted unless the server is trusted.

| Annotation | Default | Meaning |
|------------|---------|---------|
| `readOnlyHint` | `false` | Tool does not modify its environment. |
| `destructiveHint` | `true` | Updates may be destructive (only meaningful when not read-only). |
| `idempotentHint` | `false` | Repeated calls with same args have no additional effect. |
| `openWorldHint` | `true` | Interacts with an open external world (e.g. the web). |

- You **SHOULD** set these accurately; mislabeling a destructive tool as read-only invites unguarded invocation.
- Annotations inform UI and consent flows; they **MUST NOT** be your only safety control. Validate inputs, enforce access control, and rate-limit on the server.

