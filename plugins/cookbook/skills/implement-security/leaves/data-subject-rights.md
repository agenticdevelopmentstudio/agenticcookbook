<!-- leaf: implement-security/data-subject-rights · source: guidelines/implementing/security/data-subject-rights.md -->

**Rules** (cite as `implement-security/data-subject-rights#<slug>`):

- `store-personal-data-enumerable-exportable-deletable-keyed` MUST — Design the system so it can answer "what do you hold about this person, and delete it" within the legal time limit. …
- `ccpa-cpra-agent-able-satisfy-request-type` MUST — Under GDPR Chapter 3 (and analogues such as CCPA/CPRA), an agent MUST be able to satisfy each request type:
- `cannot-find-you-maintain-data-map-enumerating` MUST — You cannot fulfill a request against data you cannot find. You MUST maintain a data map enumerating every place …
- `entry-record-store-subject-id` MUST — Every entry MUST record the store, the subject-id key (or join path), the data categories, the retention basis, and …
- `persist-personal-data-update-data-map-treat` MUST — New code paths that persist personal data MUST update the data map; treat an un-mapped store as a defect.
- `acting-request-you-verify-requester-subject-authorized` MUST — Before acting on any request, you MUST verify the requester is the subject (or an authorized agent). Authenticate …
- `deletion-reach-derived-copy-just` MUST — Deletion MUST reach every derived copy, not just the primary row:
- `request-logged-subject-id-request` MUST — Every request MUST be logged with subject id, request type, timestamp, verifier, and completion — this audit trail is …
- `erasure-export-driven-single-deterministic-job` SHOULD — Erasure and export SHOULD be driven by a single deterministic job keyed by subject id, not ad-hoc queries, so coverage …
- `you-complete-requests-within-legal` MUST — You MUST complete requests within the legal deadline (GDPR: one month, extendable to three for complex cases — confirm …
- `tests-assert-created-erased-subject` SHOULD — Tests SHOULD assert that a created-then-erased subject leaves no residue across mapped stores.

# Data subject rights (DSAR)

Design the system so it can answer "what do you hold about this person, and delete it" within the legal time limit. This is an architectural property, not a feature bolted on later: every store of personal data MUST be enumerable, exportable, and deletable keyed by a stable subject id.

> Engineering guidance only — NOT legal advice. Confirm rights, scope, exemptions, and deadlines with counsel for your jurisdictions.

## The rights to support

Under GDPR Chapter 3 (and analogues such as CCPA/CPRA), an agent **MUST** be able to satisfy each request type:

| Right | Obligation |
|-------|-----------|
| **Access** | Export everything held about the subject, including derived data. |
| **Erasure** ("right to be forgotten") | Delete across all stores and propagate to processors. |
| **Rectification** | Correct inaccurate data and propagate the correction. |
| **Portability** | Provide a structured, machine-readable export (e.g. JSON/CSV). |
| **Restriction** | Mark data as processing-suspended without deleting it. |
| **Objection** | Stop a specified processing activity. |

## Data map (prerequisite)

You cannot fulfill a request against data you cannot find. You **MUST** maintain a data map enumerating every place personal data lives:

- Primary databases, caches, search indexes (Elasticsearch/OpenSearch), object storage, message queues, event logs, application logs, analytics/warehouse, and backups.
- Every entry **MUST** record the store, the subject-id key (or join path), the data categories, the retention basis, and which third-party processors receive it.
- New code paths that persist personal data **MUST** update the data map; treat an un-mapped store as a defect.

## Identity verification

Before acting on any request, you **MUST** verify the requester is the subject (or an authorized agent). Authenticate against an existing session or a verified channel; **MUST NOT** disclose or delete data on an unverified claim, since the request itself is an attack surface for account takeover and data exfiltration.

## Erasure propagation

Deletion **MUST** reach every derived copy, not just the primary row:

- Caches, search indexes, denormalized read models, and analytics aggregates.
- Third-party processors — call their deletion APIs and record completion.
- Logs and event streams: prefer pseudonymization or crypto-shredding (delete the per-subject key) where immutable append-only logs make row deletion impractical.
- Backups: full purge is often infeasible; document the rotation window after which restored backups are re-scrubbed, and treat that window as part of the SLA.

## Operational requirements

- Every request **MUST** be logged with subject id, request type, timestamp, verifier, and completion — this audit trail is itself evidence of compliance.
- Erasure and export **SHOULD** be driven by a single deterministic job keyed by subject id, not ad-hoc queries, so coverage is testable.
- You **MUST** complete requests within the legal deadline (GDPR: one month, extendable to three for complex cases — confirm with counsel). Track per-request SLA and alert before breach.
- Tests **SHOULD** assert that a created-then-erased subject leaves no residue across mapped stores.
