
- Re-check the caller's scopes/permissions on **every** tool invocation against the session's authenticated identity; **MUST NOT** cache an authorization decision across a privilege boundary.
- Scope downstream actions to the least privilege the host-process identity holds; never widen privilege based on a tool argument.
- **MUST NOT** forward a client-supplied token to a downstream API without validating its audience (see `mcp-server-security` token-passthrough rules).

