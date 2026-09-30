<!-- leaf: plan-security/data-privacy-regulations · source: guidelines/planning/security/data-privacy-regulations.md -->

**Rules** (cite as `plan-security/data-privacy-regulations#<slug>`):

- `you-not-assume-single-regime-covers` MUST — You MUST NOT assume a single regime covers all users — most products are multi-jurisdictional.
- `matrix-dated-revision-re-check-quarterly-federal` SHOULD — Treat the US state landscape as a moving target: pin your applicability matrix to a dated revision and SHOULD re-check …
- `lawful-basis` MUST — You MUST establish and record a lawful basis (GDPR) or required notice/opt-out posture (US) before collection.
- `data-minimization` MUST — You MUST collect only data needed for the stated purpose. Default to *not* collecting.
- `purpose-limitation` MUST — You MUST use data only for the purposes disclosed at collection. New purpose requires new basis/notice.
- `storage-limitation` MUST — You MUST define retention per data type and delete or anonymize when it expires.
- `transparency` MUST
- `data-subject-rights` SHOULD — You SHOULD design for access, correction, deletion, and opt-out from the start (see …
- `you-identify-role-system-plays` MUST — You MUST identify which role each system plays before design. Processor relationships MUST be governed by a written …
- `you-consult-counsel-binding-interpretation` MUST — You SHOULD consult counsel for binding interpretation; agents MUST NOT treat this guideline as legal sign-off.

# Data privacy regulations

This is engineering guidance for the obligations behind your privacy controls; it is **NOT** legal advice. Map which regimes apply from user geography and the data you collect, then confirm a lawful basis **before** any personal data is collected. Consult counsel for binding interpretation.

## Core regimes (as of 2026)

| Regime | Scope | Lawful-basis model |
|---|---|---|
| GDPR (EU/EEA) | EU/EEA residents' personal data | Requires one of six named bases (consent, contract, legal obligation, vital interests, public task, legitimate interests) |
| UK GDPR + DPA 2018 | UK residents | Mirrors GDPR post-Brexit |
| CCPA/CPRA (California) | CA residents; only state law also covering employees and B2B contacts | Notice-at-collection + opt-out of sale/share; no consent-first gate |
| Other US state laws | 19 states in effect as of Jan 1 2026 (e.g., VA, CO, TX, CT; IN/KY/RI live Jan 1 2026) | Mostly VA-template: opt-out + opt-in for sensitive data |

- You **MUST NOT** assume a single regime covers all users — most products are multi-jurisdictional.
- Treat the US state landscape as a moving target: pin your applicability matrix to a dated revision and **SHOULD** re-check quarterly. Federal court injunctions and new effective dates change the picture (forecast: more states will join through 2026–2027).

## Shared principles to encode

These appear across GDPR and most US state laws, so build to them once:

- **lawful basis**: You **MUST** establish and record a lawful basis (GDPR) or required notice/opt-out posture (US) before collection.
- **data minimization**: You **MUST** collect only data needed for the stated purpose. Default to *not* collecting.
- **purpose limitation**: You **MUST** use data only for the purposes disclosed at collection. New purpose requires new basis/notice.
- **storage limitation**: You **MUST** define retention per data type and delete or anonymize when it expires.
- **transparency**: You **MUST** disclose what is collected, why, and with whom it is shared, in plain language at the point of collection.
- **data subject rights**: You **SHOULD** design for access, correction, deletion, and opt-out from the start (see `agenticdevelopercookbook://guidelines/planning/security/privacy-by-design`).

## Controller vs processor

- **Controller** (GDPR) / **business** (CCPA): decides *why* and *how* data is processed; owns the lawful basis and most rights obligations.
- **Processor** (GDPR) / **service provider** (CCPA): acts only on documented instructions from the controller.
- You **MUST** identify which role each system plays before design. Processor relationships **MUST** be governed by a written data processing agreement (DPA).

## Before you collect

1. Determine applicable regimes from **user geography** and **data types** (special-category/sensitive data raises the bar).
2. Confirm a lawful basis or required notice/opt-out posture — and record it.
3. Confirm minimization, retention, and a deletion path exist for each field.
4. You **SHOULD** consult counsel for binding interpretation; agents **MUST NOT** treat this guideline as legal sign-off.
