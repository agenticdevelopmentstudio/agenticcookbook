
- **Drift** (out-of-band manual changes) MUST NOT become the source of truth. Reconcile it back into code, or revert it.
- Run scheduled drift detection (e.g. a periodic `plan`, `pulumi refresh` + preview, or a platform's drift feature) so manual changes are caught in hours, not at the next unrelated apply when a `destroy` appears unexpectedly.
- When drift is real and intended, encode it in the configuration and re-apply; do not leave the divergence in place.

