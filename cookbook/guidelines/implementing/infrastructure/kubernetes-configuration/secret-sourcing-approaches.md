
| Approach | Mechanism | When |
|----------|-----------|------|
| External Secrets Operator (ESO) | CNCF operator syncs from Vault / cloud manager into native Secrets | Default for most teams; secrets still land in etcd, so keep encryption-at-rest on |
| Secrets Store CSI Driver | Mounts secrets as files in the Pod's tmpfs, bypassing etcd | When you want to avoid persisting secrets in etcd |
| HashiCorp Vault / cloud KMS | Direct integration or sidecar/agent injection | High-compliance or dynamic/short-lived credentials |
