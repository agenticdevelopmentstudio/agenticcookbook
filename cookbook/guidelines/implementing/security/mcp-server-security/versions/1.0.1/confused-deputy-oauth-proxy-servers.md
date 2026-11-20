
When the server proxies a third-party API using a static client ID, a stale consent cookie lets an attacker skip the consent screen.

- A proxy server **MUST** implement per-client consent: maintain a registry of approved `client_id` values and check it **before** initiating the third-party flow.
- The MCP-level consent page **MUST** identify the requesting client, show the third-party scopes and the exact registered `redirect_uri`, and apply CSRF protection.
- `redirect_uri` **MUST** be validated by exact string match (no wildcards). The `state` value **MUST** be cryptographically random, single-use, short-lived, and set only after consent is approved.

