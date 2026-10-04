---
id: dee58e49-84e7-4ba5-b0f0-a308b2568327
title: "Consent management"
domain: agenticdevelopercookbook://guidelines/implementing/security/consent-management
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Capture granular, versioned, withdrawable consent in an auditable log and gate all non-essential processing on it."
platforms: []
tags:
  - privacy
  - consent
  - gdpr
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/security/data-privacy-regulations
references:
  - https://gdpr-info.eu/art-7-gdpr/
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
  - https://gdpr-info.eu/art-4-gdpr/
  - https://oag.ca.gov/privacy/ccpa
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - authentication
  - ui-implementation
---

# Consent management

Capture consent that is freely given, specific, informed, granular, and withdrawable; record every grant and withdrawal as an auditable, append-only log; and gate all non-essential processing on it. This is engineering guidance for building consent flows, not legal advice — confirm obligations with counsel for each jurisdiction.

## Conditions for valid consent

Per GDPR Art. 7 (and similar regimes), consent **MUST** be:

- **Freely given**: not bundled with service access; refusal **MUST NOT** degrade core functionality that does not depend on the processing.
- **Specific and granular**: each distinct purpose (analytics, marketing, personalization, third-party sharing) **MUST** have its own toggle. A single blanket "I agree" **MUST NOT** cover unrelated purposes.
- **Informed**: present the purpose, controller identity, data categories, and the right to withdraw before capture.
- **Unambiguous**: require an affirmative action (an explicit opt-in). Pre-ticked boxes, implied consent, or "continue = consent" **MUST NOT** be used.

## Recording consent

- Persist each decision as an **append-only, immutable** record. **MUST NOT** overwrite or delete prior entries — withdrawal is a new event, not a mutation.
- Each record **MUST** capture: subject id, purpose(s), grant/withdraw action, timestamp (UTC), the **policy/notice version** shown, and the capture mechanism (e.g., banner, settings page).
- Store the exact consent-notice text or a content hash so you can prove what the user saw. Pin the policy to a dated, versioned revision.
- The log **SHOULD** be queryable to answer "does subject X currently consent to purpose Y?" without replaying history at read time (maintain a derived current-state view alongside the event log).

## Withdrawal

- Withdrawal **MUST** be as easy as granting — same number of clicks, same surface, no dark patterns or friction.
- On withdrawal you **MUST** propagate the change so processing actually stops: stop new collection, halt downstream jobs, and notify processors/third parties that received the data.
- Withdrawal is **prospective**: it does not invalidate processing already performed lawfully before withdrawal, but it **MUST** prevent further processing for that purpose.

## Gating and lifecycle

- Non-essential cookies, tracking, and analytics **MUST** be gated: do not load scripts, set tags, or send events until consent for that purpose is granted (consent-before-processing, not load-then-suppress).
- Strictly necessary processing (security, fraud prevention, delivering the requested service) does not require consent and **SHOULD NOT** be presented as optional.
- Re-request consent when the purpose changes, a new data category is added, or a new processor is introduced. A policy-version bump alone **SHOULD** trigger re-consent only when the change is material to the user's decision.
- Set a re-confirmation cadence for long-lived consent (commonly revisited at 12–24 months) per applicable guidance and risk.

## Anti-patterns

- **MUST NOT** infer consent from inactivity, scrolling, or continued use.
- **MUST NOT** make "reject all" harder to reach than "accept all".
- **MUST NOT** treat children's data without the heightened, age-appropriate consent and verifiable-parental-consent paths the relevant regime requires.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add EDPB consent guidelines, GDPR Art.4, CCPA |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
