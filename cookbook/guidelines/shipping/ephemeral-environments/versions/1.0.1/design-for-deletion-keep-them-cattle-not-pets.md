
These environments are throwaway by design (per *design-for-deletion*). To prevent drift into long-lived "pets":

- All state MUST be recreatable from IaC plus seed scripts; manual hotfixes to a live preview are forbidden — change the code or the IaC and let the environment rebuild.
- Environments SHOULD be cheap and short-lived: prefer spot/preemptible compute, scale-to-zero when idle, and a TTL-based auto-shutdown.
- Tear-down MUST remove every namespaced resource (compute, DB, buckets, DNS, secrets). Leaked resources are the dominant cost and security failure mode.

