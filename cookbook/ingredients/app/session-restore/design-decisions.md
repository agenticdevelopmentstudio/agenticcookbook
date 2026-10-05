
**Decision**: Maintain the restore list separately from the platform recent-documents list.
**Rationale**: The recent list is user-visible and clearable independently; the restore list must reflect exactly what was open at quit.
**Approved**: pending

**Decision**: Skip missing, moved, or renamed files silently instead of tracking moved files. File-system-level bookmarks (Security-Scoped Bookmarks on macOS) MAY be used in a future version to track moved files, but this is out of scope for v1.
**Rationale**: Silent skipping keeps restore non-blocking; bookmark tracking adds complexity not yet needed.
**Approved**: pending

