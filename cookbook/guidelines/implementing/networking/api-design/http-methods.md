
| Method | Semantics | Idempotent | Success Code |
|--------|-----------|------------|-------------|
| GET | Read | Yes | 200 |
| POST | Create | No | 201 + Location |
| PUT | Full replace | Yes | 200 |
| PATCH | Partial update | No | 200 |
| DELETE | Remove | Yes | 204 (no body) |
