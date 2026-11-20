
- **must-have-explicit-conflict-strategy**: Every sync system MUST have an explicit conflict resolution strategy.
- **should-choose-strategy-per-entity-type**: SHOULD apply the simplest strategy that is correct for each entity type.
- **should-implement-lww-as-conditional-upsert**: LWW SHOULD be implemented on the server with an UPSERT that compares timestamps or version numbers.
- **should-use-hlc-for-lww**: SHOULD use Hybrid Logical Clock (HLC) timestamps rather than wall-clock time to avoid clock-skew errors.
- **must-not-use-lww-for-destructive-domains**: MUST NOT use LWW for collaborative editing, financial records, or inventory — silent overwrites are destructive in those domains.
- **must-store-base-version-for-field-merge**: Field-level merge MUST store the base version — the last-synced state — for three-way comparison.
- **must-merge-semantic-field-groups-atomically**: MUST identify fields that form semantic groups and resolve them atomically — for example, `quantity` and `unit_price` should not be independently merged if `total` depends on both.
- **should-use-crdts-for-offline-or-serverless**: SHOULD use CRDTs when devices may be offline for extended periods or when there is no reliable central server.
- **should-not-use-crdts-when-writes-need-validation**: SHOULD NOT use CRDTs when business-logic validation must happen before a write is accepted — CRDTs converge by definition and cannot reject writes after the fact.
- **should-use-ot-only-with-central-server**: SHOULD use OT only for text or sequence editing with a central server.
- **should-prefer-rga-crdts-offline**: For offline-first or peer-to-peer scenarios, SHOULD prefer RGA CRDTs — OT requires all operations to pass through a central coordinator for ordering.
- **should-queue-conflicts-automation-cannot-resolve**: When automated resolution is insufficient, SHOULD queue conflicts for a human to resolve.
- **must-queue-conflicts-for-regulated-records**: MUST use conflict queues for manual resolution for medical records, legal documents, and financial transactions.
- **should-detect-conflicts-against-base-version**: SHOULD detect conflicts by comparing the client's base version against the server's current version. If they differ, both sides changed since the last sync.
- **should-apply-server-version-while-pending**: SHOULD apply the server version as an interim state while the conflict is pending, and surface a notification to the user.

