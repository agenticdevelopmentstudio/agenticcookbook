
- `must-return-only-needed-fields`: an API returning fields the client does not need, or serializing a database model directly instead of a response DTO, breaks it
- `must-classify-data-by-sensitivity`: data with no sensitivity tier (public, internal, PII, sensitive PII) breaks it; controls that do not scale with the tier
- `should-encrypt-sensitive-fields-at-application-level`: SSN, payment info or other highly sensitive fields stored with only database-level encryption, not KMS-backed field encryption
- `must-not-log-pii`: a token, password, credit card number or PII in any log output, debug included, breaks it; log output not masked or redacted
- `must-not-expose-internals-in-api-responses`: an internal ID, stack trace or database error message in a production response breaks it; an error without a generic message and correlation ID
- `should-set-no-store-on-sensitive-responses`: a response containing sensitive data without `Cache-Control: no-store`
