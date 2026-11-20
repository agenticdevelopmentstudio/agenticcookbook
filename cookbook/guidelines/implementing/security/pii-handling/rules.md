
- **classify-fields**: Every field holding personal data MUST carry a sensitivity tier:
  `public`, `internal`, `pii`, or `sensitive-pii`. Tag it in the schema (column comment,
  annotation, or data catalog), not in scattered application code.
- **sensitive-pii**: Special categories (health, biometric, genetic, racial/ethnic,
  political, religious, sexual orientation; per GDPR Article 9 as in force 2026) MUST be
  tagged `sensitive-pii` and receive stricter access controls and audit logging.
- **propagate-tags**: Classification SHOULD flow downstream (propagate the tags) so derived tables, exports, and
  caches inherit the tier and its controls automatically.
- **collect-minimum**: Services MUST collect only the minimum: fields with a stated purpose. Drop a field
  rather than keep it "just in case" (YAGNI).
- **explicit-dtos**: APIs MUST return explicit response DTOs and MUST NOT serialize raw
  database models, which leaks PII by default. See `sensitive-data`.
- **separate-stores**: `sensitive-pii` SHOULD live in a dedicated, more tightly scoped store
  rather than alongside general application data.
- **encrypt-at-rest**: PII MUST be encrypted at rest (database/disk encryption at minimum;
  application-layer or column encryption for `sensitive-pii`). See `secure-storage`.
- **encrypt-in-transit**: PII MUST travel over TLS 1.2+ (prefer 1.3); plaintext transport is
  prohibited.
- **tokenize**: Where a downstream system needs a stable reference but not the value itself
  (e.g., payment data), the value SHOULD be tokenized so PII never enters that system.
- **residency**: When contracts or law require it, storage and processing MUST honor
  data-residency constraints; pin the region in infrastructure config, not in code comments.
- **no-pii-logs**: PII MUST NOT be written to logs, traces, error messages, or analytics
  events. Redact or hash identifiers at the logging boundary. See `sensitive-data`.
- **anonymize-analytics**: Analytics SHOULD use anonymized or aggregated data; pseudonymized
  data still counts as personal data if re-identification is feasible.
- **non-prod-data**: Development, test, and staging environments SHOULD use synthetic or
  anonymized data and MUST NOT contain production `sensitive-pii`.
- **retention**: Every PII field MUST have a defined retention period; expired records MUST be
  deleted or anonymized. See `data-retention-and-deletion`.
