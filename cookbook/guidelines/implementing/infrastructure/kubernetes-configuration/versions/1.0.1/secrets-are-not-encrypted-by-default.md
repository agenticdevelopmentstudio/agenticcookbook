
A Kubernetes Secret stores values base64-encoded in etcd. Base64 is reversible encoding, **not** encryption — anyone with read access to the Secret or to etcd can recover the plaintext.

- **encryption-at-rest**: Clusters using raw Secret objects **MUST** enable [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for etcd, preferring a KMS provider (KMS v2 is stable as of Kubernetes 1.29) over local `aescbc`/`secretbox` keys.
- **least-privilege-rbac**: RBAC **MUST** restrict `get`/`list`/`watch` on Secrets to the specific ServiceAccounts and subjects that need them; wildcard or namespace-wide secret read access **MUST NOT** be granted.
- **etcd-protection**: Access to etcd and to node disks **SHOULD** be tightly controlled, since either path exposes Secret contents directly.

