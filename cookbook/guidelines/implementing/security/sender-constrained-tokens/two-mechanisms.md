
| Mechanism | Spec | Binds via | Best fit |
|-----------|------|-----------|----------|
| DPoP | RFC 9449 (Sep 2023) | Per-request signed proof header at the application layer | Public clients, SPAs, mobile, no TLS-layer control |
| mTLS-bound tokens | RFC 8705 (Feb 2021) | Client TLS certificate fingerprint bound into the token | Confidential clients in controlled infra, service-to-service |

- Pick **one** mechanism per API surface and apply it consistently; do not mix bearer and constrained acceptance on the same endpoint without an explicit migration plan.
- Present the choice as a deliberate trade-off: DPoP needs no PKI but adds per-request signing; mTLS reuses transport identity but needs certificate provisioning and TLS termination you control.

