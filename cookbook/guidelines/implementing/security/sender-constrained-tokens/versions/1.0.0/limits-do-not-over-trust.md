
- Sender-constraining fails if the attacker steals **both** the token and the key material (e.g., full client compromise or XSS reading key storage); per RFC 9700 it is one layer, not a substitute for protecting the key.
- It does not replace short token lifetimes, refresh-token rotation, audience restriction, or PKCE — combine them.
- Performance and architecture (TLS-terminating CDNs, certificate provisioning) **MAY** block a mechanism in some deployments; choose the mechanism that fits the topology rather than forcing one.

