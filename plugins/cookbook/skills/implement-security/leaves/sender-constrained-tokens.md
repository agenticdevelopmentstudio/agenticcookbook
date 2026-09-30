<!-- leaf: implement-security/sender-constrained-tokens · source: guidelines/implementing/security/sender-constrained-tokens.md -->

**Rules** (cite as `implement-security/sender-constrained-tokens#<slug>`):

- `public-client-apis-issue-sender-constrained-access` SHOULD — High-value or public-client APIs SHOULD issue sender-constrained access tokens rather than plain bearer tokens.
- `proxies-browser-code-sender-constrained-because-hop` SHOULD — Tokens that traverse intermediaries (gateways, proxies, browser code) SHOULD be sender-constrained, because each hop is …
- `confidential-client-flows-stay-bearer-threat-model` MAY — Low-value, short-lived, single-confidential-client flows MAY stay bearer when the threat model and operational cost do …
- `client-generate-key-pair-send` MUST — The client MUST generate a key pair and send a DPoP proof JWT on token requests and on every protected resource …
- `proof-jwt-include-htm-http-method` MUST — The proof JWT MUST include htm (HTTP method), htu (HTTP URI), iat, and a unique jti; for resource requests it MUST …
- `authorization-server-bind-token-proof-key` MUST — The authorization server MUST bind the token to the proof key via the jkt (JWK SHA-256 thumbprint) confirmation claim …
- `resource-servers-reject-replayed-proofs-enforce` MUST — Resource servers MUST reject replayed proofs — enforce a jti/iat freshness window with a server-provided nonce where …
- `private-keys-stay-non-exportable-storage` MUST — Private keys MUST stay in non-exportable storage (WebCrypto non-extractable keys, OS keystore); never persist them …
- `client-present-tls-client-certificate` MUST — The client MUST present a TLS client certificate; the authorization server MUST record its SHA-256 fingerprint in the …
- `resource-server-confirm-tls-connection-client` MUST — The resource server MUST confirm the TLS connection's client certificate matches the bound fingerprint before honoring …
- `certificate-rotation-revocation-operationally-handled-constrained-token` MUST — Certificate rotation and revocation MUST be operationally handled; a constrained token outliving its certificate trust …
- `cdns-certificate-provisioning-block-mechanism-some-deployments` MAY — Performance and architecture (TLS-terminating CDNs, certificate provisioning) MAY block a mechanism in some …

# Sender-constrained access tokens

A plain bearer token grants access to whoever presents it: steal it, replay it. Sender-constraining binds the token to a key the legitimate client holds, so a leaked token alone is useless. The OAuth 2.0 Security Best Current Practice (RFC 9700, January 2025) recommends this for high-value APIs and public clients.

## When to apply

- High-value or public-client APIs **SHOULD** issue sender-constrained access tokens rather than plain bearer tokens.
- Tokens that traverse intermediaries (gateways, proxies, browser code) **SHOULD** be sender-constrained, because each hop is a leak surface.
- Low-value, short-lived, single-confidential-client flows **MAY** stay bearer when the threat model and operational cost do not justify constraint — this is a deliberate decision, not a default to skip.

## Two mechanisms

| Mechanism | Spec | Binds via | Best fit |
|-----------|------|-----------|----------|
| DPoP | RFC 9449 (Sep 2023) | Per-request signed proof header at the application layer | Public clients, SPAs, mobile, no TLS-layer control |
| mTLS-bound tokens | RFC 8705 (Feb 2021) | Client TLS certificate fingerprint bound into the token | Confidential clients in controlled infra, service-to-service |

- Pick **one** mechanism per API surface and apply it consistently; do not mix bearer and constrained acceptance on the same endpoint without an explicit migration plan.
- Present the choice as a deliberate trade-off: DPoP needs no PKI but adds per-request signing; mTLS reuses transport identity but needs certificate provisioning and TLS termination you control.

## DPoP requirements

- The client **MUST** generate a key pair and send a `DPoP` proof JWT on token requests and on every protected resource request, signed with the private key.
- The proof JWT **MUST** include `htm` (HTTP method), `htu` (HTTP URI), `iat`, and a unique `jti`; for resource requests it **MUST** include `ath` (access-token hash).
- The authorization server **MUST** bind the token to the proof key via the `jkt` (JWK SHA-256 thumbprint) confirmation claim (`cnf.jkt`); the resource server **MUST** verify the presented proof key matches it.
- Resource servers **MUST** reject replayed proofs — enforce a `jti`/`iat` freshness window with a server-provided `nonce` where replay risk is high.
- Private keys **MUST** stay in non-exportable storage (WebCrypto non-extractable keys, OS keystore); never persist them where script can read them.

## mTLS requirements

- The client **MUST** present a TLS client certificate; the authorization server **MUST** record its SHA-256 fingerprint in the token's `cnf.x5t#S256` confirmation claim.
- The resource server **MUST** confirm the TLS connection's client certificate matches the bound fingerprint before honoring the token.
- Certificate rotation and revocation **MUST** be operationally handled; a constrained token outliving its certificate trust is a silent failure.

## Limits — do not over-trust

- Sender-constraining fails if the attacker steals **both** the token and the key material (e.g., full client compromise or XSS reading key storage); per RFC 9700 it is one layer, not a substitute for protecting the key.
- It does not replace short token lifetimes, refresh-token rotation, audience restriction, or PKCE — combine them.
- Performance and architecture (TLS-terminating CDNs, certificate provisioning) **MAY** block a mechanism in some deployments; choose the mechanism that fits the topology rather than forcing one.
