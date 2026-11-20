
- **collect-minimum** — services MUST collect only fields with a stated purpose. Drop a field
  rather than keep it "just in case" (YAGNI).
- **explicit-dtos** — APIs MUST return explicit response DTOs and MUST NOT serialize raw
  database models, which leaks PII by default. See `sensitive-data`.
- **separate-stores** — `sensitive-pii` SHOULD live in a dedicated, more tightly scoped store
  rather than alongside general application data.

