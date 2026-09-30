<!-- leaf: implement-infrastructure/kubernetes-configuration · source: guidelines/implementing/infrastructure/kubernetes-configuration.md -->

**Rules** (cite as `implement-infrastructure/kubernetes-configuration#<slug>`):

- `non-sensitive-config` MUST
- `sensitive-in-secrets` MUST
- `no-plaintext-in-vcs` MUST
- `encryption-at-rest` MUST
- `least-privilege-rbac` MUST
- `etcd-protection` SHOULD
- `prefer-managed-store` SHOULD
- `support-rotation` SHOULD

# Kubernetes configuration and secrets

Externalize all configuration from container images: use ConfigMaps for non-sensitive settings and Secrets for credentials. Treat a Kubernetes Secret as **base64-encoded, not encrypted** — protect it at the cluster level or source it from a dedicated secret manager.

> Adopt Kubernetes only when a measured operational need justifies it (per YAGNI). A single container, a serverless platform, or a managed PaaS is often the simpler default; the guidance below applies once you have committed to Kubernetes.

## Separate config from secrets

- **non-sensitive-config**: Non-sensitive configuration (feature flags, URLs, tuning values) **MUST** live in ConfigMaps, not baked into images.
- **sensitive-in-secrets**: Credentials, tokens, TLS keys, and connection strings **MUST** be stored as Secrets (or sourced from an external manager), never as ConfigMaps.
- **no-plaintext-in-vcs**: Plaintext secret values **MUST NOT** be committed to manifests, Helm values, or any file in version control, and **MUST NOT** be baked into image layers or build args.

## Secrets are not encrypted by default

A Kubernetes Secret stores values base64-encoded in etcd. Base64 is reversible encoding, **not** encryption — anyone with read access to the Secret or to etcd can recover the plaintext.

- **encryption-at-rest**: Clusters using raw Secret objects **MUST** enable [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for etcd, preferring a KMS provider (KMS v2 is stable as of Kubernetes 1.29) over local `aescbc`/`secretbox` keys.
- **least-privilege-rbac**: RBAC **MUST** restrict `get`/`list`/`watch` on Secrets to the specific ServiceAccounts and subjects that need them; wildcard or namespace-wide secret read access **MUST NOT** be granted.
- **etcd-protection**: Access to etcd and to node disks **SHOULD** be tightly controlled, since either path exposes Secret contents directly.

## Prefer an external secret manager (production)

For production, source secrets from a dedicated manager rather than managing raw Secret objects by hand. This adds audit logging, rotation, and a single source of truth.

| Approach | Mechanism | When |
|----------|-----------|------|
| External Secrets Operator (ESO) | CNCF operator syncs from Vault / cloud manager into native Secrets | Default for most teams; secrets still land in etcd, so keep encryption-at-rest on |
| Secrets Store CSI Driver | Mounts secrets as files in the Pod's tmpfs, bypassing etcd | When you want to avoid persisting secrets in etcd |
| HashiCorp Vault / cloud KMS | Direct integration or sidecar/agent injection | High-compliance or dynamic/short-lived credentials |

- **prefer-managed-store**: Production secrets **SHOULD** come from a managed secret store (Vault, a cloud secret manager via the Secrets Store CSI driver, or ESO), not hand-authored Secret objects.

## Mounting and rotation

- **mount-choice**: Inject config as environment variables for simple scalars; mount as a volume when files, larger payloads, or live updates are needed. Volume-mounted ConfigMaps/Secrets update in place; env vars do **not** and require a Pod restart.
- **support-rotation**: Workloads **SHOULD** tolerate rotated credentials — watch mounted files or restart on change — so secrets can be rotated without a redeploy.
- **immutable-when-stable**: Mark ConfigMaps and Secrets `immutable: true` when their values are fixed for the release, reducing apiserver load and preventing accidental edits.

> Forecast: secret-management tooling and CSI/operator APIs evolve quickly — pin Helm charts and operator versions, and re-validate against the dated upstream docs before adopting new flows.

Privacy note: handling credentials and PII in clusters is engineering guidance, **not legal advice**; consult the relevant regulations and counsel for compliance obligations.
