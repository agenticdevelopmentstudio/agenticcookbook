
- **mount-choice**: Inject config as environment variables for simple scalars; mount as a volume when files, larger payloads, or live updates are needed. Volume-mounted ConfigMaps/Secrets update in place; env vars do **not** and require a Pod restart.
- **support-rotation**: Workloads **SHOULD** tolerate rotated credentials — watch mounted files or restart on change — so secrets can be rotated without a redeploy.
- **immutable-when-stable**: Mark ConfigMaps and Secrets `immutable: true` when their values are fixed for the release, reducing apiserver load and preventing accidental edits.

> Forecast: secret-management tooling and CSI/operator APIs evolve quickly — pin Helm charts and operator versions, and re-validate against the dated upstream docs before adopting new flows.

Privacy note: handling credentials and PII in clusters is engineering guidance, **not legal advice**; consult the relevant regulations and counsel for compliance obligations.

