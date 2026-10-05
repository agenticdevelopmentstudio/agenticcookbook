
**Decision**: Parallelize only the top-level directories, with a small clamped worker count.
**Rationale**: Top-level parallelism captures most of the speedup on large trees while keeping disk contention and thread counts bounded; clamping stops a bad configuration from starving the machine.
**Approved**: pending

