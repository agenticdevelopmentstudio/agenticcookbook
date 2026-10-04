---
id: 10c66228-2141-484c-9286-2d62d43c7b70
title: "Data privacy regulations"
domain: agenticdevelopercookbook://guidelines/planning/security/data-privacy-regulations
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Identify the privacy regimes that apply and confirm a lawful basis before collecting any personal data."
platforms: []
tags:
  - privacy
  - compliance
  - gdpr
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/security/privacy
  - agenticdevelopercookbook://guidelines/planning/security/privacy-by-design
references:
  - https://gdpr-info.eu/
  - https://oag.ca.gov/privacy/ccpa
  - https://iapp.org/resources/article/us-state-privacy-legislation-tracker/
  - https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - security-review
  - data-modeling
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Cite CCPA/IAPP/EUR-Lex; correct US state count to 19 (Jan 2026) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
