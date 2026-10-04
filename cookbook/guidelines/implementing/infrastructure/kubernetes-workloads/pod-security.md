
- Pods **SHOULD** run with a hardened `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, drop all Linux capabilities, and set a `seccompProfile` of `RuntimeDefault`.
- **SHOULD** enforce baseline guarantees at the namespace level with Pod Security Admission (`restricted` profile) as of Kubernetes 1.25+.
- **MUST NOT** mount the default ServiceAccount token unless the workload calls the API server.

