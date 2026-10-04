
- High-value or public-client APIs **SHOULD** issue sender-constrained access tokens rather than plain bearer tokens.
- Tokens that traverse intermediaries (gateways, proxies, browser code) **SHOULD** be sender-constrained, because each hop is a leak surface.
- Low-value, short-lived, single-confidential-client flows **MAY** stay bearer when the threat model and operational cost do not justify constraint — this is a deliberate decision, not a default to skip.

