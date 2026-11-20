
- You **MUST** review every snapshot diff before accepting it. Treat an unexpected diff as a potential bug, not a chore to clear.
- You **MUST NOT** reflexively run the update/accept-all command (`jest --updateSnapshot`/`-u`, `vitest -u`, Verify/ApprovalTests "accept all", `cargo insta accept`) to make a red suite green. Update only after confirming each change is intended.
- CI **MUST** run snapshots in non-updating mode (e.g. `--ci`) so a missing or stale snapshot fails rather than silently writing a new one.
- You **SHOULD** review snapshot files in code review as carefully as source. A diff nobody reads asserts nothing.

