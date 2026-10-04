
- Every request **MUST** be logged with subject id, request type, timestamp, verifier, and completion — this audit trail is itself evidence of compliance.
- Erasure and export **SHOULD** be driven by a single deterministic job keyed by subject id, not ad-hoc queries, so coverage is testable.
- You **MUST** complete requests within the legal deadline (GDPR: one month, extendable to three for complex cases — confirm with counsel). Track per-request SLA and alert before breach.
- Tests **SHOULD** assert that a created-then-erased subject leaves no residue across mapped stores.

