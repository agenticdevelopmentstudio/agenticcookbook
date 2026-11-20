
- A deploy MUST NOT imply 100% exposure. Ship the artifact dark, then control exposure separately.
- The exposure control plane (feature flags, traffic weights, or ring assignment) MUST be changeable without a redeploy. This keeps rollback to seconds, not a build cycle (`small-reversible-decisions`).
- Each progressive change MUST be observable on its own: tag metrics/logs/traces with the variant or cohort so canary and baseline are comparable side by side (`explicit-over-implicit`).

