
- **should-give-every-pr-a-preview**: Where feasible, every PR SHOULD get an ephemeral preview environment.
- **must-provision-on-pr-event**: The environment MUST be provisioned on a PR `opened`/`synchronize` event, not by hand.
- **must-define-spin-up-in-iac**: Spin-up MUST be defined entirely in infrastructure-as-code (Compose, Helm, K8s manifests, Terraform, or a platform manifest) so it is reproducible.
- **must-own-namespaced-resources**: Each environment MUST own its services, datastore, and DNS, namespaced by the PR identifier (e.g. `pr-123.preview.example.com`, `app-pr-123-db`).
- **must-not-collide-across-prs**: The namespace is the isolation boundary; resources from different PRs MUST NOT collide.
- **must-tear-down-on-pr-close**: Teardown MUST fire on the PR `closed` event (covers both merge and abandon).
- **should-reap-orphans-by-ttl**: A scheduled reaper SHOULD also sweep orphans by age/TTL in case a teardown job fails.
- **must-not-outlive-pr**: No environment may outlive its PR: an environment MUST NOT outlive it.

To prevent drift into long-lived "pets":

- **must-recreate-state-from-iac**: All state MUST be recreatable from IaC plus seed scripts; manual hotfixes to a live preview are forbidden — change the code or the IaC and let the environment rebuild.
- **should-keep-environments-cheap-and-short-lived**: Environments SHOULD be cheap and short-lived: prefer spot/preemptible compute, scale-to-zero when idle, and a TTL-based auto-shutdown.
- **must-remove-every-namespaced-resource**: Tear-down MUST remove every namespaced resource (compute, DB, buckets, DNS, secrets). Leaked resources are the dominant cost and security failure mode.

- **should-seed-with-synthetic-fixtures**: SHOULD seed each environment with synthetic or anonymized fixtures (per *test-data-management*).
- **must-not-copy-production-pii**: Production PII MUST NOT be copied into a preview.
- **should-default-to-fresh-provision**: SHOULD choose a database strategy deliberately: pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*).
- **should-include-real-backend**: Full-stack previews SHOULD include the real backend, not just a static frontend against shared staging — interaction bugs between front and back surface only when both run the PR's code.
- **should-run-e2e-against-live-url**: SHOULD run E2E/smoke suites and contract tests (see [adc.guideline.testing.contract-testing](cookbook:abdcd282-5b81-4ab2-ab1e-3ed288a4aee5)) against the live URL.
- **should-post-preview-link-and-results**: SHOULD post the preview link plus check results back as a PR comment for human review.
- **may-substitute-request-routing**: For changes too large to stand up a full stack per PR, a request-routing / intercept approach (e.g. Telepresence-style local interception into a shared cluster) MAY substitute — treat that as a deliberate decision, not the default.
- **must-not-write-to-production**: Preview environments MUST NOT have write access to production data stores, queues, or third-party prod accounts; point them at sandbox credentials.
- **should-make-spin-up-and-teardown-idempotent**: Spin-up and teardown jobs SHOULD be idempotent so a re-run or retried webhook does not duplicate or orphan resources.
- **should-verify-vendor-behavior**: Managed-platform feature names and DB-branching capabilities evolve quickly, so SHOULD verify current behavior against the vendor's docs before relying on a specific guarantee.
- **should-treat-vendor-claims-as-unverified**: FORECAST: SHOULD treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline.
