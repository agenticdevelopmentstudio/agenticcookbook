---
id: 647b7d54-41fc-4f31-96e4-3d23ae49f92b
title: "PII handling and classification"
domain: agenticdevelopercookbook://guidelines/implementing/security/pii-handling
type: guideline
version: 1.0.2
status: accepted
language: en
created: 2026-06-09
modified: 2026-07-23
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Classify PII at the schema level, minimize collection, encrypt at rest and in transit, and never write it to logs."
platforms: []
tags:
  - privacy
  - pii
  - security
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/security/pii-detection-and-redaction
  - agenticdevelopercookbook://guidelines/implementing/security/sensitive-data
  - agenticdevelopercookbook://guidelines/implementing/security/secure-storage
  - agenticdevelopercookbook://guidelines/implementing/data/data-retention-and-deletion
references:
  - https://gdpr-info.eu/art-9-gdpr/
  - https://gdpr-info.eu/art-4-gdpr/
  - https://www.iso.org/standard/27701
  - https://www.nist.gov/privacy-framework
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - data-modeling
  - logging
  - security-review
---

# PII handling and classification

Personally identifiable information (PII) MUST be classified at the schema level so controls
apply consistently. Minimize what you collect, encrypt it everywhere, and keep it out of logs.
This is engineering guidance and NOT legal advice; confirm obligations with counsel.

## Classify at the schema level

- **classify-fields** — every field holding personal data MUST carry a sensitivity tier:
  `public`, `internal`, `pii`, or `sensitive-pii`. Tag it in the schema (column comment,
  annotation, or data catalog), not in scattered application code.
- **sensitive-pii** — special categories (health, biometric, genetic, racial/ethnic,
  political, religious, sexual orientation; per GDPR Article 9 as in force 2026) MUST be
  tagged `sensitive-pii` and receive stricter access controls and audit logging.
- **propagate-tags** — classification SHOULD flow downstream so derived tables, exports, and
  caches inherit the tier and its controls automatically.

## Minimize and isolate

- **collect-minimum** — services MUST collect only fields with a stated purpose. Drop a field
  rather than keep it "just in case" (YAGNI).
- **explicit-dtos** — APIs MUST return explicit response DTOs and MUST NOT serialize raw
  database models, which leaks PII by default. See `sensitive-data`.
- **separate-stores** — `sensitive-pii` SHOULD live in a dedicated, more tightly scoped store
  rather than alongside general application data.

## Protect at rest and in transit

- **encrypt-at-rest** — PII MUST be encrypted at rest (database/disk encryption at minimum;
  application-layer or column encryption for `sensitive-pii`). See `secure-storage`.
- **encrypt-in-transit** — PII MUST travel over TLS 1.2+ (prefer 1.3); plaintext transport is
  prohibited.
- **tokenize** — where a downstream system needs a stable reference but not the value itself
  (e.g., payment data), the value SHOULD be tokenized so PII never enters that system.
- **residency** — when contracts or law require it, storage and processing MUST honor
  data-residency constraints; pin the region in infrastructure config, not in code comments.

## Keep PII out of logs and lower environments

- **no-pii-logs** — PII MUST NOT be written to logs, traces, error messages, or analytics
  events. Redact or hash identifiers at the logging boundary. See `sensitive-data`.
- **anonymize-analytics** — analytics SHOULD use anonymized or aggregated data; pseudonymized
  data still counts as personal data if re-identification is feasible.
- **non-prod-data** — development, test, and staging environments SHOULD use synthetic or
  anonymized data and MUST NOT contain production `sensitive-pii`.

## Retention and deletion

- **retention** — every PII field MUST have a defined retention period; expired records MUST be
  deleted or anonymized. See `data-retention-and-deletion`.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-07-23 | Mike Fullerton | Cross-link to new pii-detection-and-redaction guideline |
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add GDPR Art.4 pseudonymisation, ISO 27701:2025, NIST Privacy Framework |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
