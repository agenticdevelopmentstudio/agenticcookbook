
MUST paginate sync results. Never request or deliver unbounded result sets.

Use the server-assigned sync version as the cursor — not an offset. Offset-based pagination skips records if new changes arrive during sync.

Recommended batch sizes:

| Context | Batch Size |
|---------|-----------|
| Mobile (unstable network) | 50–100 records |
| Desktop (stable network) | 500–1000 records |
| Initial bootstrap | 1000–5000 records |
| Background sync | 100–500 records |

