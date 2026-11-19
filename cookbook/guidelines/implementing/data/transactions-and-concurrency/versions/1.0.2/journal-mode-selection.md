
| Mode | Concurrent Reads | Write Speed | Durability | Use When |
|------|-----------------|-------------|------------|----------|
| WAL | Yes | Fast (sequential) | Full (with NORMAL) | Default for most apps |
| DELETE | No | Slow | Full | Network file systems, max compatibility |
| MEMORY | No | Fast | None | Ephemeral/rebuildable data only |
| OFF | No | Fastest | None | Bulk load where crash safety is irrelevant |

MUST NOT use `MEMORY` or `OFF` journal modes in production databases where data loss on crash is unacceptable.

