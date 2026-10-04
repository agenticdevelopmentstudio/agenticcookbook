
- Persist each decision as an **append-only, immutable** record. **MUST NOT** overwrite or delete prior entries — withdrawal is a new event, not a mutation.
- Each record **MUST** capture: subject id, purpose(s), grant/withdraw action, timestamp (UTC), the **policy/notice version** shown, and the capture mechanism (e.g., banner, settings page).
- Store the exact consent-notice text or a content hash so you can prove what the user saw. Pin the policy to a dated, versioned revision.
- The log **SHOULD** be queryable to answer "does subject X currently consent to purpose Y?" without replaying history at read time (maintain a derived current-state view alongside the event log).

