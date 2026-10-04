
- The client **MUST** present a TLS client certificate; the authorization server **MUST** record its SHA-256 fingerprint in the token's `cnf.x5t#S256` confirmation claim.
- The resource server **MUST** confirm the TLS connection's client certificate matches the bound fingerprint before honoring the token.
- Certificate rotation and revocation **MUST** be operationally handled; a constrained token outliving its certificate trust is a silent failure.

