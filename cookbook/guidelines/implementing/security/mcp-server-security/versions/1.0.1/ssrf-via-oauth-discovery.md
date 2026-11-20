
A malicious server can populate discovery fields (`resource_metadata`, `authorization_servers`, `token_endpoint`) with internal URLs.

- Server-side deployments **MUST** consider SSRF and apply mitigations when fetching OAuth-related URLs.
- They **SHOULD** require HTTPS (loopback excepted for dev), block private/reserved ranges (`10/8`, `172.16/12`, `192.168/16`, `169.254/16`, `127/8`, `fc00::/7`, `fe80::/10`), and validate redirect targets per hop.
- Prefer an egress proxy and DNS-pinning over hand-rolled IP parsing, which misses octal/hex/IPv4-mapped-IPv6 encodings.

