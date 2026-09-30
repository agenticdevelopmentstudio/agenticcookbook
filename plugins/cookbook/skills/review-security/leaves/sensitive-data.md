<!-- leaf: review-security/sensitive-data · source: guidelines/reviewing/security/sensitive-data.md -->

**Rules** (cite as `review-security/sensitive-data#<slug>`):

- `data-minimization` MUST — APIs MUST return only fields the client needs. Use explicit response DTOs, never dump database models directly.
- `pii-classification` MUST — data MUST be classified by sensitivity (public, internal, PII, sensitive PII). Apply controls proportional to tier.
- `no-pii-in-logs` MUST — tokens, passwords, credit card numbers, or PII MUST NOT be logged. Mask/redact in all log outputs, including debug …
- `no-internals-in-api-responses` MUST — internal IDs, stack traces, or database error messages MUST NOT be exposed in production. Return generic errors with …

# Sensitive Data

Minimize what you collect, encrypt what you keep, never log what you shouldn't.

- **Data minimization** — APIs MUST return only fields the client needs. Use explicit response DTOs,
  never dump database models directly.
- **PII classification** — data MUST be classified by sensitivity (public, internal, PII, sensitive PII).
  Apply controls proportional to tier.
- **Field-level encryption** — encrypt highly sensitive fields (SSN, payment info) at the
  application level with a KMS (AWS KMS, Azure Key Vault, GCP KMS). Separate from database-level
  encryption.
- **No PII in logs** — tokens, passwords, credit card numbers, or PII MUST NOT be logged. Mask/redact
  in all log outputs, including debug level. See agenticdevelopercookbook://guidelines/reviewing/security/privacy
- **No internals in API responses** — internal IDs, stack traces, or database
  error messages MUST NOT be exposed in production. Return generic errors with correlation IDs.
- **Cache-Control: no-store** on responses containing sensitive data.

References:
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST SP 800-122: PII Guide](https://csrc.nist.gov/publications/detail/sp/800-122/final)
