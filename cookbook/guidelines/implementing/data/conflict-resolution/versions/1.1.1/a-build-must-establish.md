
- `must-have-explicit-conflict-strategy`: the sync system resolves conflicts by an explicit, named strategy
- `should-choose-strategy-per-entity-type`: each entity type has its own conflict strategy, the simplest that is correct for it, or the code says why not
- `should-implement-lww-as-conditional-upsert`: LWW is applied on the server by an UPSERT whose update is conditional on a newer timestamp or version, or the code says why not
- `should-use-hlc-for-lww`: LWW compares HLC timestamps, not wall-clock time, or the code says why not
- `must-not-use-lww-for-destructive-domains`: no collaborative-editing, financial or inventory data is resolved by LWW
- `must-store-base-version-for-field-merge`: every field-level merge has the stored last-synced base version to compare against
- `must-merge-semantic-field-groups-atomically`: fields that form a semantic group (such as `quantity`, `unit_price` and a dependent `total`) are resolved together, never field by field
- `should-use-crdts-for-offline-or-serverless`: data edited on devices offline for long periods, or with no reliable central server, uses CRDTs, or the code says why not
- `should-not-use-crdts-when-writes-need-validation`: no data whose writes need business-logic validation before acceptance uses CRDTs, or the code says why not
- `should-use-ot-only-with-central-server`: OT is used only for text or sequence editing with a central server, or the code says why not
- `should-prefer-rga-crdts-offline`: offline-first or peer-to-peer text and sequence editing uses RGA CRDTs, not OT, or the code says why not
- `should-queue-conflicts-automation-cannot-resolve`: conflicts that automated resolution cannot settle are queued for a human, or the code says why not
- `must-queue-conflicts-for-regulated-records`: conflicts on medical records, legal documents and financial transactions go to a manual-resolution queue
- `should-detect-conflicts-against-base-version`: conflicts are detected by comparing the client's base version with the server's current version, or the code says why not
- `should-apply-server-version-while-pending`: while a conflict is pending, the server version is applied as the interim state and the user is notified, or the code says why not

