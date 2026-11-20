
Storage limitation (GDPR Art. 5(1)(e), as of the 2016 regulation) requires that data be kept no longer than necessary for its purpose.

- Maintain a **retention schedule** as code or config that maps each **data category** (user profile, auth tokens, audit logs, analytics events, PII, derived ML features) to a maximum retention period and a disposition (delete vs. anonymize).
- Every category **MUST** have a defined retention period; absence of a period is itself a decision and **MUST** be justified (e.g., legal-hold or financial records with a statutory minimum).
- Each category **SHOULD** have **automated expiry** — a scheduled job, TTL index, or partition-drop — rather than manual cleanup.
- Record a `created_at` (and where relevant `expires_at`) timestamp on every retained record so expiry is computable and auditable.

