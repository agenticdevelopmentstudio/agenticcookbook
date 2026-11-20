
- **created-automatically**: The environment MUST be provisioned on a PR `opened`/`synchronize` event, not by hand. Spin-up MUST be defined entirely in infrastructure-as-code (Compose, Helm, K8s manifests, Terraform, or a platform manifest) so it is reproducible.
- **isolated**: Each environment MUST own its services, datastore, and DNS, namespaced by the PR identifier (e.g. `pr-123.preview.example.com`, `app-pr-123-db`). The namespace is the isolation boundary; resources from different PRs MUST NOT collide.
- **destroyed-automatically**: Teardown MUST fire on the PR `closed` event (covers both merge and abandon). A scheduled reaper SHOULD also sweep orphans by age/TTL in case a teardown job fails. No environment may outlive its PR.

