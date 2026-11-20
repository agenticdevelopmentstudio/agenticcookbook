
- `treat-secret-as-encoded-not-encrypted`, `encryption-at-rest`, `least-privilege-rbac`, `etcd-protection`: A Kubernetes Secret stores values base64-encoded in etcd. Base64 is reversible encoding, **not** encryption — anyone with read access to the Secret or to etcd can recover the plaintext.
- `pin-and-revalidate-secret-tooling`: Forecast: secret-management tooling and CSI/operator APIs evolve quickly.
