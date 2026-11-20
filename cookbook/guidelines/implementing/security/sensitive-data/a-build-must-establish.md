
- `must-return-only-needed-fields`: each API response is an explicit DTO holding only the fields the client needs
- `must-classify-data-by-sensitivity`: every data field has a sensitivity tier, and its controls match that tier
- `should-encrypt-sensitive-fields-at-application-level`: highly sensitive fields are encrypted at the application level with a KMS, or the code says why not
- `must-not-log-pii`: no log output at any level holds a token, password, credit card number or PII
- `must-not-expose-internals-in-api-responses`: production errors return a generic message with a correlation ID and no internal IDs, stack traces or database errors
- `should-set-no-store-on-sensitive-responses`: sensitive responses carry `Cache-Control: no-store`, or the code says why not
