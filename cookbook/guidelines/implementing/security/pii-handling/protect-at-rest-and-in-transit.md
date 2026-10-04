
- **encrypt-at-rest** — PII MUST be encrypted at rest (database/disk encryption at minimum;
  application-layer or column encryption for `sensitive-pii`). See `secure-storage`.
- **encrypt-in-transit** — PII MUST travel over TLS 1.2+ (prefer 1.3); plaintext transport is
  prohibited.
- **tokenize** — where a downstream system needs a stable reference but not the value itself
  (e.g., payment data), the value SHOULD be tokenized so PII never enters that system.
- **residency** — when contracts or law require it, storage and processing MUST honor
  data-residency constraints; pin the region in infrastructure config, not in code comments.

