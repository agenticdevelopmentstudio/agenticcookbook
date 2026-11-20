
# No blocking the main thread

All lengthy work must run on background threads/tasks using platform async primitives. The main/UI thread MUST NOT be blocked.
