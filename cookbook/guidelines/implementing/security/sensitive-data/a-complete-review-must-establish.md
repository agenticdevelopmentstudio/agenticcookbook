
- `must-return-only-needed-fields`: whether every API returns only the fields its client needs, through explicit response DTOs
- `must-classify-data-by-sensitivity`: whether all data is classified by sensitivity tier, with controls proportional to tier
- `should-encrypt-sensitive-fields-at-application-level`: whether highly sensitive fields are encrypted at the application level with a KMS
- `must-not-log-pii`: whether any token, password, credit card number or PII reaches a log output at any level
- `must-not-expose-internals-in-api-responses`: whether any production response exposes internal IDs, stack traces or database error messages
- `should-set-no-store-on-sensitive-responses`: whether every response containing sensitive data sets `Cache-Control: no-store`
- `must-return-only-needed-fields`: API responses return only needed fields via explicit DTOs rather than raw database models;
