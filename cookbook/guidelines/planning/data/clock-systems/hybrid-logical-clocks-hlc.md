
HLC combines physical wall-clock time with a logical counter in a single 64-bit value:

```
HLC timestamp = [48-bit physical time ms] + [16-bit logical counter]
```

**Properties:**
- Stays close to wall-clock time (within a bounded drift of physical time)
- Guarantees causal ordering (strictly monotonic per node)
- Self-stabilizing: NTP corrections that move the clock backward do not violate monotonicity
- Single 64-bit value — no per-device array growth
- Human-readable: can be truncated to a millisecond timestamp for debugging

**Update rules:** When generating an event, take `max(local_physical_time, last_hlc_physical)`. If equal, increment the logical counter. When receiving a message with an HLC, merge: take the max of both physical components, then adjust the counter to avoid collision.

SHOULD use HLC as the default timestamp mechanism for multi-device sync. It provides the ordering guarantees of logical clocks while remaining close to physical time and fitting in a single `INTEGER` or `TEXT` column.

Store HLC values in SQLite as `INTEGER` (milliseconds + counter packed) or as `TEXT` with a fixed-width format that sorts lexicographically.

