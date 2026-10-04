
An array of counters, one per device. When Device A sends a message, it includes its full vector. The recipient merges by taking the element-wise maximum.

**Property:** Can definitively distinguish "happened-before" from "concurrent." Two events are concurrent if neither vector dominates the other.

**Limitation:** Storage and transmission cost grows O(n) where n is the number of devices. With 10 devices, each record carries 10 counters. With thousands of devices (consumer apps), this is impractical.

**When to use:** Systems with a small, fixed set of replicas (e.g., 3–5 database nodes in a cluster). Well-suited for server-side distributed databases, not client-side mobile sync.

