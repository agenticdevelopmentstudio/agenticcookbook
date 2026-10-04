
**Server-wins:** Discard the client's change when the server version is newer or equal. Safe for admin-pushed configuration and read-only sync scenarios.

**Client-wins:** Always apply the client's change. Equivalent to LWW where the client always has the "later" timestamp. Appropriate for personal data owned exclusively by one user.

Turso/libSQL exposes these as explicit strategies: `DISCARD_LOCAL` (server-wins), `REBASE_LOCAL` (replay client changes on top of server state), and `FAIL_ON_CONFLICT` (reject and surface to the application).

