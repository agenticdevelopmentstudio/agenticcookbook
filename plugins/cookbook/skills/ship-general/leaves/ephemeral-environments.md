<!-- leaf: ship-general/ephemeral-environments · source: guidelines/shipping/ephemeral-environments.md -->

**Rules** (cite as `ship-general/ephemeral-environments#<slug>`):

- `where-feasible-pr-get-one` SHOULD — An ephemeral preview environment is an isolated, fully disposable stack provisioned automatically when a PR opens and …
- `created-automatically` MUST
- `isolated` MUST
- `destroyed-automatically` MUST
- `state-recreatable-from-iac-plus` MUST — All state MUST be recreatable from IaC plus seed scripts; manual hotfixes to a live preview are forbidden — change the …
- `environments-cheap-short-lived-prefer` SHOULD — Environments SHOULD be cheap and short-lived: prefer spot/preemptible compute, scale-to-zero when idle, and a TTL-based …
- `tear-down-remove-namespaced-resource-compute` MUST — Tear-down MUST remove every namespaced resource (compute, DB, buckets, DNS, secrets). Leaked resources are the dominant …
- `management-production-pii-not-copied-into-preview` MUST — Seed each environment with synthetic or anonymized fixtures (per *test-data-management*). Production PII MUST NOT be …
- `full-stack-previews-include-real-backend-just` SHOULD — Full-stack previews SHOULD include the real backend, not just a static frontend against shared staging — interaction …
- `into-shared-cluster-substitute-treat-deliberate-decision` MAY — For changes too large to stand up a full stack per PR, a request-routing / intercept approach (e.g. Telepresence-style …
- `preview-environments-not-have-write-access-production` MUST — Preview environments MUST NOT have write access to production data stores, queues, or third-party prod accounts; point …
- `up-teardown-jobs-idempotent-so-re-run` SHOULD — Spin-up and teardown jobs SHOULD be idempotent so a re-run or retried webhook does not duplicate or orphan resources.

# Ephemeral preview environments

An ephemeral preview environment is an isolated, fully disposable stack provisioned automatically when a PR opens and destroyed automatically when it merges or closes. It exists to give reviewers and CI a realistic place to exercise the change end-to-end. Where feasible, every PR SHOULD get one.

## Lifecycle (three invariants)

- **created-automatically**: The environment MUST be provisioned on a PR `opened`/`synchronize` event, not by hand. Spin-up MUST be defined entirely in infrastructure-as-code (Compose, Helm, K8s manifests, Terraform, or a platform manifest) so it is reproducible.
- **isolated**: Each environment MUST own its services, datastore, and DNS, namespaced by the PR identifier (e.g. `pr-123.preview.example.com`, `app-pr-123-db`). The namespace is the isolation boundary; resources from different PRs MUST NOT collide.
- **destroyed-automatically**: Teardown MUST fire on the PR `closed` event (covers both merge and abandon). A scheduled reaper SHOULD also sweep orphans by age/TTL in case a teardown job fails. No environment may outlive its PR.

## Design for deletion — keep them cattle, not pets

These environments are throwaway by design (per *design-for-deletion*). To prevent drift into long-lived "pets":

- All state MUST be recreatable from IaC plus seed scripts; manual hotfixes to a live preview are forbidden — change the code or the IaC and let the environment rebuild.
- Environments SHOULD be cheap and short-lived: prefer spot/preemptible compute, scale-to-zero when idle, and a TTL-based auto-shutdown.
- Tear-down MUST remove every namespaced resource (compute, DB, buckets, DNS, secrets). Leaked resources are the dominant cost and security failure mode.

## Test data — disposable, never production

- Seed each environment with synthetic or anonymized fixtures (per *test-data-management*). Production PII MUST NOT be copied into a preview.
- Choose a database strategy: **fresh provision** (blank DB + run migrations + seed) is simplest and works anywhere; **copy-on-write branching** (e.g. Neon/PlanetScale-style branches, or a snapshot restore) is faster when the engine supports it natively. Pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*).

## What to run against it

- Full-stack previews SHOULD include the real backend, not just a static frontend against shared staging — interaction bugs between front and back surface only when both run the PR's code.
- Run E2E/smoke suites and contract tests (see `agenticdevelopercookbook://guidelines/testing/contract-testing`) against the live URL, and post the preview link plus check results back as a PR comment for human review.
- For changes too large to stand up a full stack per PR, a request-routing / intercept approach (e.g. Telepresence-style local interception into a shared cluster) MAY substitute — treat that as a deliberate decision, not the default.

## Guardrails

- Preview environments MUST NOT have write access to production data stores, queues, or third-party prod accounts; point them at sandbox credentials.
- Spin-up and teardown jobs SHOULD be idempotent so a re-run or retried webhook does not duplicate or orphan resources.
- Note: managed-platform feature names and DB-branching capabilities evolve quickly — verify current behavior against the vendor's docs before relying on a specific guarantee. FORECAST: treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline.
