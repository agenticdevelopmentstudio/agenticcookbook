
Non-deterministic snapshots produce noisy diffs that train reviewers to accept blindly (`fail-fast` erodes when failures are routine).

- You **MUST** strip or normalize non-deterministic values before serializing: timestamps, dates, durations, random IDs/UUIDs, hostnames, absolute paths, and ports.
- You **MUST** stabilize ordering of sets, maps, and query results — sort before snapshotting rather than depending on iteration order.
- You **SHOULD** use property matchers for unavoidable dynamics (Jest/Vitest `expect.any(...)` in `toMatchSnapshot({ id: expect.any(String) })`; ApprovalTests scrubbers; `insta` filters) instead of regenerating the snapshot each run.

