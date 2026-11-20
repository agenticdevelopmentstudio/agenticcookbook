
- **must-return-only-needed-fields**: Data minimization: APIs **MUST** return only fields the client needs. You **SHOULD** use explicit response DTOs and **MUST NOT** ever dump database models directly.
- **must-classify-data-by-sensitivity**: PII classification: data **MUST** be classified by sensitivity (public, internal, PII, sensitive PII). You **SHOULD** apply controls proportional to tier.
- **should-encrypt-sensitive-fields-at-application-level**: Field-level encryption: you **SHOULD** encrypt highly sensitive fields (SSN, payment info) at the application level with a KMS (AWS KMS, Azure Key Vault, GCP KMS), separate from database-level encryption.
- **must-not-log-pii**: No PII in logs: tokens, passwords, credit card numbers, or PII **MUST NOT** be logged. You **SHOULD** mask/redact in all log outputs, including debug level.
- **must-not-expose-internals-in-api-responses**: No internals in API responses: internal IDs, stack traces, or database error messages **MUST NOT** be exposed in production. You **SHOULD** return generic errors with correlation IDs.
- **should-set-no-store-on-sensitive-responses**: You **SHOULD** set `Cache-Control: no-store` on responses containing sensitive data.
