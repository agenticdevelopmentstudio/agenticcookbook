
- **Corrupt cache file**: The loader MUST handle malformed JSON gracefully (handle-missing-cache) — log a warning and proceed as if no cache exists.
- **Cache file missing or unreadable**: Same behavior as a corrupt cache — empty/loading state.
- **Concurrent cache writes**: If a save is requested while a previous save is still in progress, the implementation SHOULD coalesce or serialize writes to avoid conflicts.
- **Orphaned entries**: An entry whose `parentPath` matches no entry in the array SHOULD be dropped on load rather than attached to the wrong parent.

