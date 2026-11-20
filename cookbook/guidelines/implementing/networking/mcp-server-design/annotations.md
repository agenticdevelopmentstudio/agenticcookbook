
| Annotation | Default | Meaning |
|------------|---------|---------|
| `readOnlyHint` | `false` | Tool does not modify its environment. |
| `destructiveHint` | `true` | Updates may be destructive (only meaningful when not read-only). |
| `idempotentHint` | `false` | Repeated calls with same args have no additional effect. |
| `openWorldHint` | `true` | Interacts with an open external world (e.g. the web). |
