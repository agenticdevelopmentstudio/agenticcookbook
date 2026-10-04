
- **classify-fields** — every field holding personal data MUST carry a sensitivity tier:
  `public`, `internal`, `pii`, or `sensitive-pii`. Tag it in the schema (column comment,
  annotation, or data catalog), not in scattered application code.
- **sensitive-pii** — special categories (health, biometric, genetic, racial/ethnic,
  political, religious, sexual orientation; per GDPR Article 9 as in force 2026) MUST be
  tagged `sensitive-pii` and receive stricter access controls and audit logging.
- **propagate-tags** — classification SHOULD flow downstream so derived tables, exports, and
  caches inherit the tier and its controls automatically.

