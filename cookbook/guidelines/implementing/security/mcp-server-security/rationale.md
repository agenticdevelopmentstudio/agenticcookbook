
- `should-bind-approval-to-tool-hash`, `should-version-tool-definitions`: A server (or a tool it proxies) can present a benign description at approval time and a malicious one later (rug-pull, tool redefinition).
- `should-bind-approval-to-tool-hash`: ACCURACY NOTE: the publicized "MCPoison"/"CurXecute" CVEs were CLIENT-side bugs in an IDE and have been patched. Retain the rug-pull threat class and the hash-bound-approval mitigation; do not cite those CVEs as motivation for server authoring.
- `must-implement-per-client-consent`, `must-show-client-scopes-and-redirect-on-consent`: When the server proxies a third-party API using a static client ID, a stale consent cookie lets an attacker skip the consent screen (confused deputy).
- `must-consider-ssrf-on-oauth-urls`, `should-harden-oauth-url-fetching`: A malicious server can populate discovery fields (`resource_metadata`, `authorization_servers`, `token_endpoint`) with internal URLs.
