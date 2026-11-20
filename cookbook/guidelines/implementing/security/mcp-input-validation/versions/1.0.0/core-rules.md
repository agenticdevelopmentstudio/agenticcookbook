
- Tool handlers **MUST** validate every argument against the tool's declared `inputSchema` before use, rejecting on mismatch — do not rely on the client or model to have validated.
- Handlers **MUST NOT** trust an argument because it arrived through the model; an argument's provenance grants it no privilege.
- Handlers **MUST** enforce authorization on every call against the authenticated identity, not against anything the model passes.
- Handlers **MUST** sanitize and bound any argument before it reaches a side effect (filesystem, network, DB, shell, downstream API).

