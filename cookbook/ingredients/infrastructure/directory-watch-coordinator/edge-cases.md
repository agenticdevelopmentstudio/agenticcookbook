
- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Rapid filesystem changes**: If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Cache save in flight during update**: A surgical update that completes while a previous save is still running SHOULD coalesce or serialize the saves.
- **Workspace with zero entries**: The workspace manager holds no coordinators and its aggregate `isSyncing` is `false`.

