
For production, source secrets from a dedicated manager rather than managing raw Secret objects by hand. This adds audit logging, rotation, and a single source of truth.

| Approach | Mechanism | When |
|----------|-----------|------|
| External Secrets Operator (ESO) | CNCF operator syncs from Vault / cloud manager into native Secrets | Default for most teams; secrets still land in etcd, so keep encryption-at-rest on |
| Secrets Store CSI Driver | Mounts secrets as files in the Pod's tmpfs, bypassing etcd | When you want to avoid persisting secrets in etcd |
| HashiCorp Vault / cloud KMS | Direct integration or sidecar/agent injection | High-compliance or dynamic/short-lived credentials |

- **prefer-managed-store**: Production secrets **SHOULD** come from a managed secret store (Vault, a cloud secret manager via the Secrets Store CSI driver, or ESO), not hand-authored Secret objects.

