
- Conflict resolution strategy chosen and documented for each entity type
- LWW implementation uses reliable timestamps (Hybrid Logical Clocks or server-assigned monotonic versions)
- Field-level merge strategy includes base version for three-way comparison when applicable
- Manual resolution queue exists for conflicts that cannot be automatically resolved
- Policy justification documented (why this strategy fits the data semantics)
- Every rule is kept, or the change says why not: `must-have-explicit-conflict-strategy`, `should-choose-strategy-per-entity-type`, `should-implement-lww-as-conditional-upsert`, `should-use-hlc-for-lww`, `must-not-use-lww-for-destructive-domains`, `must-store-base-version-for-field-merge`, `must-merge-semantic-field-groups-atomically`, `should-use-crdts-for-offline-or-serverless`, `should-not-use-crdts-when-writes-need-validation`, `should-use-ot-only-with-central-server`, `should-prefer-rga-crdts-offline`, `should-queue-conflicts-automation-cannot-resolve`, `must-queue-conflicts-for-regulated-records`, `should-detect-conflicts-against-base-version`, `should-apply-server-version-while-pending`


A review passes when it establishes every item above.
