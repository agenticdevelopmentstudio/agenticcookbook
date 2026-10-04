
A monotonically increasing integer counter. Each event increments the counter by one. When a message arrives from another device with a higher counter value, the local counter jumps to that value.

**Property:** If event `e` happened before `f`, then `L(e) < L(f)`. But the converse is NOT guaranteed — `L(e) < L(f)` does NOT mean `e` happened before `f`. Lamport timestamps cannot distinguish "happened-before" from "concurrent."

**When to use:** Systems that only need causal ordering (not concurrency detection). Extremely low overhead — a single integer column. Suitable for server-to-client replication where the server serializes all writes.

**When NOT to use:** Conflict detection that requires distinguishing concurrent writes from causally ordered writes.

